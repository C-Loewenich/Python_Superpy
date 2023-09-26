import sys
import csv

from datetime import datetime
from rich.table import Table

from utilities import date_format, sales_path, console, search_advise
from utilities import todays_date
from inventory_classes import Inventory
from sales_classes import SalesItem

# This file focus on the reporting and modeling of the different data.
class Report():
    def __init__(self, request_detailed_report=False):
        self.report_data = self.get_sales_data()
        self.search_item = "all products"
        self.time_frame_filter = ""

    def get_sales_data(self):
        sales_data = []
        try:
            with open(sales_path, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # excludes the header row.
                for row in reader:
                    sales_data.append(SalesItem(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
            return sales_data
        except:
            console.log(f"[red]UPS!!! There seems to be problems to find the sales file \nPlease contact your system admin to report the error.[/red]")
            sys.exit()

    def filter_item(self, filter_item, internal_use=False): 
        # can both be used internally to return the result or externaly to alter report data and set serch item data 
        output = []
        for data_row in self.report_data:
            if filter_item.lower() in data_row.item.lower():
                output.append(data_row)
        if internal_use == True:
            return output
        else:
            self.report_data = output
            self.search_item = filter_item #sets the item being filtered to display correct discription of the data

    def filter_sales_date(self, start_date_str, end_date_str):
        # returns the dates between two datas given.
        output = []
        self.time_frame_filter = f"{start_date_str} - {end_date_str}"
        for data_row in self.report_data:
            start_date = datetime.strptime(start_date_str, date_format)
            end_date = datetime.strptime(end_date_str, date_format)
            if start_date <= data_row.sales_date <= end_date: 
                output.append(data_row)
        self.report_data = output

    def get_items_in_data(self): 
        # return an list without dublications of the items in the data set.
        items = []
        for data_row in self.report_data:
            if data_row.item.lower() not in items:
                items.append(data_row.item.lower())
        return items

    def get_sales_history(self):
        # returns a dict with the number of sold items pr. weekday
        history = {
            "Monday": 0,
            "Tuesday": 0,
            "Wednesday": 0,
            "Thursday": 0,
            "Friday": 0,
            "Saturday": 0,
            "Sunday": 0
        }

        weekdays = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

        for record in self.report_data:
            weekday_numeric = record.sales_date.weekday()
            weekday_str = weekdays.get(
                weekday_numeric, lambda: console.log("[red]Weekday not found[/red]"))
            history[weekday_str] += record.count
        return history

    def check_for_no_items(self):
        if len(self.report_data) < 1:
            console.log(f"[red]No items to display[/red]\n{search_advise}")
            sys.exit() 

    def display_table(self, title, columns, rows):
        # Creates and displays the tables
        table = Table(title=title, style="blue")
        for column in columns:
            table.add_column(column[0], style=column[1], justify=column[2])
        for row in rows:
            table.add_row(*row)    
        console.log(table)

    def output_purchase_advisor_report(self, search_item):
        # Models the data for the advisor repport and displays both the KPI's as well as the history.

        kpi_rows = []
        kpi_columns = [
            ["KPI,s", "blue", "left"],
            ["", "grey37", "right"],
        ]

        total_quantity = sum(item.count for item in self.report_data)
        if total_quantity == 0:
            console.log("[red]No items found[/red]")
            sys.exit(2)
        total_shelftime = sum(
            item.shelftime*item.count for item in self.report_data)
        total_days_to_expiratoin = sum(
            item.days_until_expiration*item.count for item in self.report_data)
        total_cost = sum(item.buying_price_pr_piece *
                         item.count for item in self.report_data)
        total_profit = sum(item.profit_pr_piece *
                           item.count for item in self.report_data)

        kpi_rows.append([
            "Currently in stock",
            str(round(Inventory().get_inventory_count(search_item)))
        ])
        kpi_rows.append([
            "Average shelftime",
            "{:.1f}".format(total_shelftime/total_quantity),
        ])
        kpi_rows.append([
            "Average days to expiraton",
            "{:.1f}".format(total_days_to_expiratoin/total_quantity),
        ])
        kpi_rows.append([
            "profit to cost ratio %",
            "{:.1f}".format((total_profit/total_cost)*100), 
        ])
        self.display_table(
            f"Key product indicators for {self.search_item} in the last 4 weeks", kpi_columns, kpi_rows)

        # Sectoin Hisotry
        history_rows = []
        history_columns = [
            ["Weekday", "blue", "left"],
            ["Average pr. day", "grey37", "right"],
            ["Percentage", "grey37", "right"]
        ]

        chart = []

        history = self.get_sales_history()
        for key, value in history.items():
            history_rows.append([
                key,
                str(round(value/4)),
                str(round((value/total_quantity)*100))
            ])

        self.display_table(
            f"Sales history for {self.search_item} in the last 4 weeks", history_columns, history_rows)
        

    def output_financial_report(self, highlight, request_detailed_report=False):
        # Prepares the profit repport with aggregated data as standard or with detailed data if requested. 
        self.check_for_no_items()
        rows = []
        if request_detailed_report is True:
            # Displays detailed information with a summary of the data in a seperate table
            columns_full_report = [
                ["item", "blue bold", "left"],
                ["Quantity", "grey37", "right"],
                ["Buying price pr. piece", "grey37", "right"],
                ["sales price pr. piece", "blue bold" if highlight == "revenue" else "grey37", "right"],
                ["Profit pr. piece", "blue bold " if highlight == "profit" else "grey37", "right"],
                ["Profit for this sales", "blue bold" if highlight == "profit" else "grey37", "right"]
            ]
            columns_summary_report = [
                [" ", "blue bold", "left"],
                ["Quantity", "grey37", "right"],
                ["Buying price", "grey37", "right"],
                ["Revenue", "blue bold" if highlight == "revenue" else "grey37", "right"],
                ["Profit", "blue bold " if highlight == "profit" else "grey37", "right"]
            ]
            report_summaries = []
            total_count = 0
            total_buying_price = 0
            total_sales_price = 0
            total_profit = 0

            for data_row in self.report_data:
                record_total_profit = int(
                    data_row.count) * float(data_row.profit_pr_piece)
                rows.append([
                    data_row.item,
                    str(data_row.count),
                    # Makes sure that prices are displaied with two decimals after the comma and .
                    "{:.2f}".format(data_row.buying_price_pr_piece),
                    "{:.2f}".format(data_row.sales_price_pr_piece),
                    "{:.2f}".format(data_row.profit_pr_piece),
                    "{:.2f}".format(record_total_profit)
                ])
                total_count = total_count + int(data_row.count)
                total_buying_price += (int(data_row.count)
                                       * float(data_row.buying_price_pr_piece))
                total_sales_price += (int(data_row.count)
                                      * float(data_row.sales_price_pr_piece))
                total_profit += record_total_profit

            report_summaries.append([
                "Total",
                str(total_count),
                "{:.2f}".format(total_buying_price),
                "{:.2f}".format(total_sales_price),
                "{:.2f}".format(total_profit),
            ])
            report_summaries.append([  # preparing average pr. item
                "Average pr. item",
                # the average pr. quantity does not create an added value as it would of course be one, it is therefore not displaied.
                "-",
                # calcute the average, round it to two decimals and make it in to a string to be read by rich.
                "{:.2f}".format(total_buying_price / total_count),
                "{:.2f}".format(total_sales_price / total_count),
                "{:.2f}".format(total_profit / total_count)
            ])

            self.display_table(
                f"Detailed profit report for {self.search_item} sold {self.time_frame_filter}", columns_full_report, rows)
            self.display_table(
                f"Sumary of profit report for {self.search_item} sold {self.time_frame_filter}", columns_summary_report, report_summaries)
 
        else:  # aggregates the data for each type of item and displays this with calculated totals and averages.
            columns = [
                ["item", "blue bold", "left"],
                ["Quantity", "grey37", "right"],
                ["Average purchasing costs", "grey37", "right"],
                ["Toatl purchasing costs", "grey37", "right"],
                ["Average revenue", "blue bold" if highlight == "revenue" else "grey37", "right"],
                ["Total revenue", "blue bold" if highlight == "revenue" else "grey37", "right"],
                ["Average profit", "blue bold" if highlight == "profit" else "grey37", "right"],
                ["Total profit", "blue bold" if highlight == "profit" else "grey37", "right"]
            ]

            items_in_data = self.get_items_in_data()
            for item in items_in_data:  
                
                data_to_aggregate = self.filter_item(item, internal_use=True)
                item_total_count = 0
                item_total_purchasing_cost = 0
                item_total_sales_revenue = 0
                item_total_profit = 0

                for i in data_to_aggregate:  # iterate over the data set for the item to calculate count, costs and revenue
                    item_total_count += i.count
                    item_total_purchasing_cost += (i.count *
                                                   i.buying_price_pr_piece)
                    item_total_sales_revenue += (i.count *
                                                 i.sales_price_pr_piece)
                    item_total_profit += (i.count * i.profit_pr_piece)
                item_average_purchasing_costs = item_total_purchasing_cost / item_total_count
                item_average_revenue = item_total_sales_revenue / item_total_count
                item_average_profit = item_total_profit / item_total_count

                rows.append([
                    item,
                    str(item_total_count),
                    "{:.2f}".format(item_average_purchasing_costs),
                    "{:.2f}".format(item_total_purchasing_cost),
                    "{:.2f}".format(item_average_revenue),
                    "{:.2f}".format(item_total_sales_revenue),
                    "{:.2f}".format(item_average_profit),
                    "{:.2f}".format(item_total_profit),
                ])
            self.display_table(
                f"Aggregated repport of {self.search_item} sold {self.time_frame_filter}", columns, rows)
