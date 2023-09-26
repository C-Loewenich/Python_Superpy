import csv
import sys
from utilities import inventory_path, console

# This file focus on the inventory. Either inventory items or the full inventory here split in to two different classes.  

class InventoryItem():
    # Creates an inventory item and adds this item to the inventory
    def __init__(self, id, item, count, buying_price, buying_date, expiration_date):
        self.id = id
        self.item = item
        self.count = int(count)
        self.buying_price = buying_price
        self.buying_date = buying_date
        self.expiration_date = expiration_date

    def add_inventory(self):
        with open(inventory_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.id, self.item, self.count,
                            self.buying_price, self.buying_date, self.expiration_date])

class Inventory():
    # This class gets, changes, saves or in other ways works with the inventory file
    def __init__(self, sales_item_instance=None):
        self.copy_of_inventory = self.get_copy_of_inventory()
        self.sales_item_instance = sales_item_instance

    def get_copy_of_inventory(self):
        inventory_records = []
        try:
            with open(inventory_path, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # excludes the header row.
                for row in reader:
                    id = row[0]
                    item = row[1]
                    count = row[2]
                    buying_price = row[3]
                    buying_date = row[4]
                    expiration_date = row[5]
                    inventory_record = InventoryItem(
                        id, item, count, buying_price, buying_date, expiration_date)
                    inventory_records.append(inventory_record)
            return inventory_records
        except:
            console.log(f"[red]UPS!!! There seems to be problems to find the inventory file \nPlease contact your system admin to report the error.[/red]")
            sys.exit()

    def find_items_in_inventory(self, search_item):
        # returns a list of records with a specefic item name
        found_records = []
        for record in self.copy_of_inventory:
            if search_item.lower() == record.item.lower():
                found_records.append(record)
        return found_records

    def get_inventory_count(self, search_item):
        # gets the total amount for a speceic item if given, if the seach_item is None it will return the full inventory.
        if search_item == None:
            return sum(record.count for record in self.copy_of_inventory)
        else:
            return sum(record.count for record in self.find_items_in_inventory(search_item))

    def remove_zeroed_records(self):
        # Remove the records in the copy_of_inventory if thre is nothing left of this item (count = 0)
        temp_inventory = []
        for record in self.copy_of_inventory:
            if record.count != 0:
                temp_inventory.append(record)
        self.copy_of_inventory = temp_inventory

    def save_inventory_to_CSVfile(self):
        # saves the changed invntory to the inventory CSV file.
        inventory = []
        for record in self.copy_of_inventory:
            inventory.append([record.id, record.item, record.count,
                             record.buying_price, record.buying_date, record.expiration_date])
        with open(inventory_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # adding the header to the inventory file.
            writer.writerow(
                ['ID', 'Item', 'Count', 'Buying Price', 'Buying Date', 'Expiration Date'])
            writer.writerows(inventory)
