# SuperPy - Report

During this project I have taken some decisions and here I explain my reasoning and reflections for some of them.

### Classes

For this assignment I have decided to use classes, The Main reason for this was simply that I find classes an important part of Python and I wanted to dig more in depth into this subject. As this is a learning environment it was the perfect opportunity to do so. Thereby it was clear to me from the beginning that I would use classes to some extend for this project.

With classes I like that you can create instances. For this project I find it gives a clear structure to split the different parts of working with inventory, sales, or the reports into different files but also into different classes. So, for instance the creation of a new inventory item is done in one class and the modification of the inventory is done in a different class.

When working with the data I also find it a very positive aspect that this can be done in the classes which also stores the report data. Filters can be set up as build in methods. As these are applied it automatically save the filtered data within that instance of the class. Thereby it becomes as easy as giving a command. “Do this” instead of having to working with variables and thereby having to saving the filtered data back to the variable again and again.

### Data structure

In this project I have chosen to save the inventory ID and what is perceived as the current data, in separate CSV files. I have done so to ensure that this information is saved and reused every time the program is used. This was especially important as I have chosen a structure where the inventory is being altered as sales has been recorded. Thereby passing on the inventory ID into the sales data.

Currently the id is not being used for anything, but could the future be used to see which sales record comes from which inventory record.  
As the inventory is being altered simply getting a new ID by looking at the number of records in the inventory list would not work. Thereby the ID is stored in a separate file to ensure that it will always be incremented by one.

### Discarding external data analysis libaries.

For this assignment I have also chosen to simply work with the standard CSV library. I am aware that an external library such as Pandas does have advantages especially when it comes to handling, cleaning or analysis of data but I felt that it was a bit out of scope of this project. As this is also a learning experience I wanted to first learn and understand the build in CSV library before getting into other external libraries.
