import os
import csv
import sys
import re
from datetime import datetime, timedelta
from rich.console import Console

# Path variables
script_directory = os.getcwd()
inventory_path = os.path.join(script_directory, "inventory.csv")
sales_path = os.path.join(script_directory, "sales.csv")
current_date_path = os.path.join(script_directory, "current_date.csv")
inventory_id_path = os.path.join(script_directory, "inventory_id.csv")
user_guide_path = os.path.join(script_directory, "user_guide.md")

# Other variables
date_format = '%d.%m.%Y'
console = Console()
search_advise = f"[orange1]User advice: We suggest to check the entered data for accuracy. Alternatively to enter the item as singular. This may give another result![/orange1]"

def set_date(day_change):
    # sets the date percieved by the program and saves this to the file current_data.csv file
    new_date = None
    if re.match(r'^\d{2}\.\d{2}\.\d{4}$', day_change): #check if it is a string in date format (dd.mm.yyyy)
        check_data_format([day_change])
        new_date = day_change
    elif re.match(r'^[+-]?\d+$', day_change): #check if it is an int in str format 
        day_change = int(day_change)
        date = datetime.now().date()
        new_date = (date + timedelta(days= day_change)).strftime(date_format)
    else: #In case somethings else is entered an error message is shown with guidens.
        console.print(f"[red][blue]{day_change}[/blue] is not a valid date format or full number of days. \nPlease enter a date in the format dd.mm.yyyy or a full number of days to move a hole number of days in the past(-) or future(+) of todays date or enter '?' to se the date set as todays date.[/red]")
        sys.exit()
    with open(current_date_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow([new_date])
    
def new_id():
    # creates a new item Id, from the inventory_id file. Making sure that no two id's will be the same, even as items are removed from the inventory
    with open(inventory_id_path, 'r') as file:
        reader = csv.reader(file)
        new_id = int(next(reader)[0])
    new_id += 1
    with open(inventory_id_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow([new_id])
    return new_id

def todays_date(type = "str"):
    # retuns the date percieved as todays date by the program
    with open(current_date_path, 'r') as file:
        reader = csv.reader(file)
        if type == "str":
            return next(reader)[0] #The 0 takes the date in the first row only, so in this case the date as str.
        elif type == "date":
            return datetime.strptime(next(reader)[0], date_format) # Here the date is returned as a date for the set data format.

def check_data_format(date_list):
    for date in date_list:
        error_triggered = False
        try:
            date_str = datetime.strptime(date, date_format)
        except ValueError:
            if re.match(r'^\d{2}\.\d{2}\.\d{4}$', date):
                console.log(f"[orange1]Notice! [/orange1]{date}[orange1] is not a date in the Gregorian calendar.[/orange1]")
            else:
                console.log(f"[red]invalid date format: [/red]{date}")

            error_triggered = True
            # exits the program after printed error message with the error status of 1 (Invalid date)
    if error_triggered == True:
        sys.exit(1)

def convert_list_to_string(variable):
    if isinstance(variable, list):
        return variable[0]
    else:
        return variable