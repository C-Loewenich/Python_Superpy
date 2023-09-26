# SuperPy - Userguide

## Introduction

With Superpy it is easy to keep control over your inventory as well as your sales. It is easy to withdraw information in reports with specific focus such as revenue and and profit reports. These reports can either be created with aggregated data or detailed data and summary report. All reports can additionally be filtered to only include a specific item, data from a specific time period or both.

Additionally an advisor report can be drawn which helps you to make the right inventory purchage decissions. This repport gives you an overview of the average shelftime, how long the produchts could have stayed in stock before expireing as well as sales history of the last 4 weeks showing which days were the bussiest. This report can thereby all in present the Key Purchase Indicators ether for all produchts or more commenly used for a specific item. Helping you to predict future demand and thereby assist you in your inventory purchase.

Lastly the date persived to be todays date by the system can also be be changed.

## Dependencies

### Python

Superpy is build and tested in Python v. 3.10.7 and it is therefore advised to use this version. Other versions may however also work as well but this can not be guaranteed.

### Rich

The Rich libary (external) is needed in order to present the report tables correctly. Please ensure that the correct Rich version for your Python version is installed.

### Argpars

SuperPy uses the standard libary argparse. This enables the user to enter all commands direcly in the Comand line (CLI) Below the specific commands are explained.

## Working with SuperPy

In order to use superpy open your prefered comand line interface and navigate to the SuperPy directory where ever you have stored this.

In general the following command `python superpy.py` is used to run the different parts of the program.

**This Should be entered before all of the below command** and will in below examples be displaied as **-->**

```
C:\superpy> python superpy.py
```

SuperPy is split up in to 4 main parts depending on what you want to work with.

- [Inventory](#inventory) add or search the inventory.
- [Sales](#sales) record sales
- [Reports](#reports) create reports
- [Time](#time) change the date percieved as the current date

### Inventory <a id="inventory"></a>

The command `inventory` enables you to either add purchased items to the invenotry or search the inventory to see how much is currently in stock of a specific item.

```
--> inventory
```

#### Add item to the inventory

by adding `add` to the `inventory` command you can add new item to the inventory.
The following information should be entered in the correct order.

- **item** The name of the item you want to add (Please enter this in singular! Example: Apple. NOT Apples)
- **count** How many pieces there should be added to the inventor
- **buying price** Buyig price pr piece for the specific item
- **expiration date** The expiration date of the specific item (format: dd.mm.yyyy)

_Example_

```
--> inventory add apple 10 1.20 01.01.2024
Added 10 apple to the inventory
```

#### Search item in inventory

by adding `search` to the `inventory` command you can search for an item in the inventory.
The following information should be entered in the correct order.

- **item** The name of the item you want to search for in the inventory

_Example_

```
--> inventory search apple
Currently 10 apple in stock
```

### Sales <a id="sales"></a>

The command `sales` enables you to record a sales. Thereby the inventory is automatically updated.
The following information should be entered in the correct order.

- **item** The name of the item being sold
- **amount needed** How many pieces of the item there has ben sold
- **selling price** Price pr. piece of the specific item.

```
--> sales apple 2 1.99
2 apple recorded as sold
```

### Reports <a id="reports"></a>

The `report` command enables you to create financial reports with focus on either revneue or profit. An advisor report can also be created to assist with the purchase of new inventory

```
--> report
```

#### Financial reports

by adding `revenue` or `profit` to the `report` command you can create a finaisial report with focus on either the revenues or the profits (Thereby the respective data will be highlighted).

Thereby one of the following comands are _required_.

- **profit** Displays a financial report with focus on profit
- **revenue** Displays a financial report with focus on revenue

The following _optional_ comands can be used to spefify or change the layout of your report. Thereby more then one optional command can be entered.

- **--detailed** Displays a report of every sold item as well as a summary report
- **-i or --item** Filters the data, to specify the report for only one item
- **-d or --dates** Set a time frame for the report in dates (format: dd.mm.yyyy dd.mm.yyyy)

_Examples_

```
--> report profit -i apple -d 01.09.2023 30.09.2023

                                                    Aggregated repport of apple sold
┏━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ item  ┃ Quantity ┃ Average purchasing costs ┃ Toatl purchasing costs ┃ Average revenue ┃ Total revenue ┃ Average profit ┃ Total profit ┃
┡━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ apple │      152 │                     1.21 │                 183.92 │            2.01 │        305.23 │           0.80 │       121.31 │
└───────┴──────────┴──────────────────────────┴────────────────────────┴─────────────────┴───────────────┴────────────────┴──────────────┘
```

<ANNOTATION! - As default an aggrigated report will be displayed unless the --detailed command is used to overwrite this.

_Examples_

```
--> report profit -i apple -d 01.09.2023 02.09.2023 --detailed
                        Detailed profit report for apple sold 01.09.2023 - 02.09.2023
┏━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ item  ┃ Quantity ┃ Buying price pr. piece ┃ sales price pr. piece ┃ Profit pr. piece ┃ Profit for this sales ┃
┡━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ apple │        2 │                   1.21 │                  1.99 │             0.78 │                  1.56 │
│ apple │        5 │                   1.21 │                  1.99 │             0.78 │                  3.90 │
│ apple │        5 │                   1.21 │                  2.10 │             0.89 │                  4.45 │
│ apple │        3 │                   1.21 │                  1.99 │             0.78 │                  2.34 │
│ apple │        2 │                   1.21 │                  1.99 │             0.78 │                  1.56 │
│ apple │        5 │                   1.21 │                  1.99 │             0.78 │                  3.90 │
│ apple │        5 │                   1.21 │                  1.99 │             0.78 │                  3.90 │
└───────┴──────────┴────────────────────────┴───────────────────────┴──────────────────┴───────────────────────┘
 Sumary of profit report for apple sold 01.09.2023 - 02.09.2023
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┓
┃                  ┃ Quantity ┃ Buying price ┃ Revenue ┃ Profit ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━┩
│ Total            │       27 │        32.67 │   54.28 │  21.61 │
│ Average pr. item │        - │         1.21 │    2.01 │   0.80 │
└──────────────────┴──────────┴──────────────┴─────────┴────────┘
```

#### Advisor report

The Advisor report showins you the key purchase indicators (KPI's) for the last 4 weeks. Information crucial for making the currect purchasing decissions. Thereby the following is important

- _Currently in stock_
- _Average shelftime_
- _Average days to expiraton_
- _profit to cost ratio %_
- _Sales history_

_Background Information_:
even if there might be alot of an item in stock it might still be a good idea to order additional in stock. If the average shelftime is low and the items in general are sold way before they expire. Then the risk af purchasing additional in stock is low. If the item thereby has a high profit to cost ratio it could directly effect your revenue and profit if you should run out of this item. For items there the shelftime is long and the items are sold just shorly before they expire it is important to limit the risk for writing of items. Here the sales history can be important to see how many items might be sold on a given day and thereby ensure that you have enough to sell without having to write of to many items.

by adding `advisor` to the `report` command you can see the KPI's either for all produchts sold or more commonly used by item.

The following _optional_ comands can be used to spefify the report.

- **-i or --item** Creates an advisor report for a specific item.

_Example_

```
--> report advisor -i apple
Key product indicators for apple in
          the last 4 weeks
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
│ Currently in stock        │   11 │
│ Average shelftime         │  0.4 │
│ Average days to expiraton │ 29.1 │
│ profit to cost ratio %    │ 66.0 │
└───────────────────────────┴──────┘
Sales history for apple in the last 4 weeks
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Weekday   ┃ Average pr. day ┃ Percentage ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ Monday    │               1 │          3 │
│ Tuesday   │              11 │         30 │
│ Wednesday │               4 │          9 │
│ Thursday  │               4 │         11 │
│ Friday    │               7 │         18 │
│ Saturday  │               9 │         23 │
│ Sunday    │               2 │          6 │
└───────────┴─────────────────┴────────────┘
```

### Change time <a id="time"></a>

The command `time` enables you to set another date to be percieved by the program as the current date.

- **-d or --date** Both a integer number or a date can be given.

  - _Option1:_ Enter a integer number to move x amount of days back(-) or forward(+) in comparison to the actual current date.
  - _Option2:_ Set specific date by entering the date you want to set a current date (format: dd.mm.yyyy).
  - _Option3:_ enter '?' to se the date set as todays date.

- **Default:** If no optional parameter is given the actual current date is set.

_Example_ - Default.

```
--> time
Todays date set to 24.09.2023
```

_Example_ - Integer enterd as optional parameter.

```
--> time -d 2
Todays date set to 26.09.2023
```

_Example_ - Date enterd as optional parameter.

```
--> time -d 20.09.2023
Todays date set to 20.09.2023
```

_Example_ - See the date set as todays date.

```
--> time -d ?
Date percieved as todays date: 20.09.2023
```

---
