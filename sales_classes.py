import csv
import sys
from datetime import datetime
from utilities import date_format, sales_path
from utilities import todays_date, console, search_advise
from inventory_classes import Inventory

# This file focus on the Sales side. Either sales items or the full sales data here split in to two different classes. 

class SalesItem:
    # Template for creating a new sales item
    def __init__(self, id, item, count, buying_price, buying_date, expiration_date, sales_date, sales_price_pr_piece, profit_pr_piece, shelftime, days_until_expiration):
        self.id = id
        self.item = str(item)
        self.count = int(count)
        self.buying_price_pr_piece = float(buying_price)
        self.buying_date = datetime.strptime(buying_date, date_format)
        self.expiration_date = datetime.strptime(expiration_date, date_format)
        self.sales_date = datetime.strptime(sales_date, date_format)
        self.sales_price_pr_piece = float(sales_price_pr_piece)
        self.profit_pr_piece = float(profit_pr_piece)
        self.shelftime = int(shelftime)
        self.days_until_expiration = int(days_until_expiration)


class Sales():
    # crating the sale of an item, initiate the update of the invnetory calculate key data in connection with the sale. 
    def __init__(self, item, count_requested, price):
        self.item = item
        self.count_needed = int(count_requested)
        self.price = price
        self.inventory = Inventory()
        self.copy_of_inventory = self.inventory.get_copy_of_inventory()
        self.found_items_in_inventory = self.inventory.find_items_in_inventory(item)
        self.inventory_count = self.inventory.get_inventory_count(item)

    def record_sales_and_update_inventory(self):
        if self.inventory_count >= self.count_needed:
            # Changes the records for the found items until the amount needed has been reached.
            total_sold_count = 0
            for item in self.found_items_in_inventory:
                if total_sold_count >= self.count_needed:
                    break
                remaining_to_sell = self.count_needed - total_sold_count
                # takes what ever number is the lowest of what is still needed and the count of the item.
                items_to_sell = min(remaining_to_sell, item.count)
                self.save_sold_item_to_CSVfile(item, items_to_sell)
                item.count -= items_to_sell
                total_sold_count += items_to_sell
            self.inventory.remove_zeroed_records()
            self.inventory.save_inventory_to_CSVfile()
        else:
            console.log(f"[grey37]sorry! - We currently have [blue]{self.inventory_count} {self.item}[/blue] left in stock[/grey37]")
            if self.inventory_count == 0:
                console.log(search_advise)
            sys.exit()

    def save_sold_item_to_CSVfile(self, item, count_sold):
        with open(sales_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([item.id, item.item, count_sold, item.buying_price, item.buying_date, item.expiration_date, todays_date(
            ), self.price, self.get_profit_pr_piece(item), self.get_shelftime(item), self.get_days_until_expiration(item)])

    def get_profit_pr_piece(self, item):  # returns the profit
        return round(self.price - float(item.buying_price), 2)

    # return the number of days between the buying date and the sales date.
    def get_shelftime(self, item):
        return (datetime.strptime(todays_date(), date_format) - datetime.strptime(item.buying_date, date_format)).days

    # return the number of days between the sales date and the expiration date.
    def get_days_until_expiration(self, item):
        return (datetime.strptime(item.expiration_date, date_format) - datetime.strptime(todays_date(), date_format)).days
    
