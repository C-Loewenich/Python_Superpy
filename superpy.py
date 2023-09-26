from utilities import set_date, new_id, todays_date, check_data_format, convert_list_to_string, console, search_advise, date_format, user_guide_path
from inventory_classes import Inventory, InventoryItem
from sales_classes import Sales
from report_classes import Report

from argparse import *
from datetime import timedelta


parser = ArgumentParser(description="Welcome to SuperPy, This program can help you to organize or inventory as well as sales, Furthermore you can create reports and find stastics of your inventory and sales.")
subparsers = parser.add_subparsers(dest="command")

# create user_guide parser
user_guide_parser = subparsers.add_parser("user_guide", help="open the user guide file.")

# create inventory parser
inventory_parser = subparsers.add_parser("inventory", help="Allow you to add an items or search the Inventory")
inventory_subparser = inventory_parser.add_subparsers(title="Inventory", dest="inventory_command")

## create the add parser under inventory
add_parser = inventory_subparser.add_parser("add", help="Adds an item to the inventory")
add_parser.add_argument(
    "item", 
    type=str, 
    help="The name of the item you want to add (Please enter this in singular! Example: Apple. NOT Apples)")
add_parser.add_argument(
    "count", 
    type=int, 
    help="How many pieces there should be added to the inventor")
add_parser.add_argument(
    "buying_price", 
    type=float, 
    help="Buyig price pr piece for the specefic item")
add_parser.add_argument(
    "expiration_date", 
    type=str, 
    help="The expiration date of the specefic item (format: dd.mm.yyyy)")

##create the search parser under inventory
search_parser = inventory_subparser.add_parser("search", help="Search the inventory for an item.")
search_parser.add_argument(
    "item", 
    type=str, 
    help="The name of the item you want to search for in the inventory")

# create sales parser
sales_parser = subparsers.add_parser("sales", help="Make record of your sales. This will automatically alter your current inventory")
sales_parser.add_argument(
    "item", 
    type=str, 
    help="The name of the item being sold")
sales_parser.add_argument(
    "amount_needed", 
    type=int, 
    help="How many pieces of the item there has ben sold")
sales_parser.add_argument(
    "selling_price", 
    type=float, 
    help="Price pr. piece of the specefic item.")

# create report parser
report_parser = subparsers.add_parser("report", help="Create an profit and revenue report or a purchace advisor report")
report_subparser = report_parser.add_subparsers(title="Report", dest="report_command")

## create profit report parser
profit_parser = report_subparser.add_parser("profit", help="Displays a financial report with focus on profit")
profit_parser.add_argument(
    "--detailed", 
    action="store_true", 
    help="Displays a report of every sold item as well as a summary report")
profit_parser.add_argument(
    "-i", "--item", 
    type=str, 
    nargs=1, 
    help="Filters the data, to specify the report for only one item", metavar="")
profit_parser.add_argument(
    "-d", "--dates", 
    type=str, nargs=2, 
    help="Set a time frame for the report in dates (format: dd.mm.yyyy dd.mm.yyyy)", metavar="")

## create revenue report parser
revenue_parser = report_subparser.add_parser("revenue", help="Displays a financial report with focus on revenue")
revenue_parser.add_argument(
    "--detailed", 
    action="store_true", 
    help="Displays a report of every sold item as well as a summary report")
revenue_parser.add_argument(
    "-i", "--item", 
    type=str, 
    nargs=1, 
    help="Filters the data, to specify the report for only one item", metavar="")
revenue_parser.add_argument(
    "-d", "--dates", 
    type=str, 
    nargs=2, 
    help="Set a time frame for the report in dates", metavar="") 

## create purchase advisor report parser
advisor_parser = report_subparser.add_parser("advisor", help="Displays an advisory repoart for new purchases of inventory with key figures and forcast")
advisor_parser.add_argument(
    "-i", "--item", 
    type=str,
    nargs=1,
    help="Creates an advisor report for a specefic item", metavar="")

# crate time parser
time = subparsers.add_parser("time", help="Change the date which is seen as todays date of the system")
time.add_argument(
    "-d", "--date",
    type=str, 
    default="0",
    help="Option1: Enter a integer number to move x amount of days back(-) or forward(+) in comparison to the reallife current date -- Option2: Set specefic date by entering the date (format: dd.mm.yyyy)", metavar="")


# parse arguments
args = parser.parse_args()
if args.command == None:
    console.print(f"Welcome to SuperPy")
    console.print(f"Todays date: {todays_date()}")
    console.print(f"Please enter 'python superpy.py' followed by the command you want to execute.")
    console.print(f"TIP: You can use the '-h' command to get help or open the full user guide with the command 'user_guide'")

if args.command == "user_guide":
    try:
        with open(user_guide_path, 'r', encoding='utf-8') as md_file:
            markdown_content = md_file.read()
            console.log(markdown_content)
    except FileNotFoundError:
        console.log(f"[red]Error: File not found - {user_guide_path}[/red]")

if args.command == "inventory":
    if args.inventory_command == "add":
        #adds item to Inventory
        check_data_format([args.expiration_date])
        InventoryItem(new_id(), args.item, args.count, args.buying_price, todays_date(), args.expiration_date).add_inventory()
        console.log(f"[green]Added [blue]{args.count} {args.item}[/blue] to the inventory[/green]")
    elif args.inventory_command == "search":
        #Displays the current stoch for the item
        count = Inventory().get_inventory_count(args.item)
        console.log(f"[grey37]Currently [blue]{count} {args.item}[/blue] in stock[/grey37]")
        if count == 0:
            console.log(search_advise)

if args.command == "sales":
    # creates a sales and write it to CSV file
    Sales(args.item, args.amount_needed, args.selling_price).record_sales_and_update_inventory()
    console.log(f"[green][blue]{args.amount_needed} {args.item}[/blue] recorded as sold[/green]")

if args.command == "report":
    report = Report()
    if args.item != None:
        # If an item is given then filter for this item.
        report.filter_item(args.item[0])
    #if args.report_command == "profit" or "revenue":
    if args.report_command != "advisor":
        if args.dates != None:
            # If dates are given then filter data for dates
            check_data_format(args.dates)
            report.filter_sales_date(args.dates[0], args.dates[1]) 
        report.output_financial_report(args.report_command, args.detailed) # Displaying detailed report if difined othwerweise agrigated report is displayed as standard.
    elif args.report_command == "advisor":
        start_date = todays_date("date") - timedelta(days = 28) #gets the start date 28 days (4weeks) from current date (as seen by the application)
        report.filter_sales_date(start_date.strftime(date_format), todays_date())
        report.output_purchase_advisor_report(convert_list_to_string(args.item)) #If item is None the full list is shown

if args.command == "time":
    if args.date == "?":
        console.log(f"Date percieved as todays date: {todays_date()}")
    else:
        # changes the date percieved as todays day by the program
        set_date(args.date)
        console.log(f"[green]Todays date set to [blue]{todays_date()}[/blue][/green]")
