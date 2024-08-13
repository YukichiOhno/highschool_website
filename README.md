# restful api: highschool
Most entities have the usual get, post, put, and delete functions. The associative entities, on the other hand, only involve post, put, and delete functions, except for invoice_line.
All entities have restrictions in the payload and only accept attributes that are actually present in the database for security and authorization. 

There are triggers created in the database as well, for the purpose of automating real-life updates. The most prominent one is the student gpa. Whenever a student receives a grade, who did not the drop the class, their gpa would be automatically updated in the STUD_GPA attribute of the STUDENT entity. Another trigger is a simple one. There's two attributes in the BUDGET entity that store a monetary value: BUD_ALLOCATED and BUD_REMAIN. The former represents the original value that was allocated to that budget entity row, whereas the former represents the remaining amount of budget in that same entity row. 

There's also an item trigger that takes place when a department uses or takes an item from inventory and use them for whatever means necessary. Everytime they take out an item from inventory, the amount they took would automatically be reduced from the inventory based on the amount they took. There's also rare cases where they return the same amount of item back in case of the mistakes taking place; otherwise, if the item is already used, they can no longer return it back. 

In terms of transactions, "/api/pay_invoice" is the only route that involves these actions. They involve the BUDGET, INVOICE, INVOICE_LINE, and INVENTORY entities. Everytime an admin places an order on our supplier, that order automatically translates to the invoice our suppliers give us, since we can count the amount of items we need and we usually ask for the price of each items. This order is in a pending state, so any quantities in the INVOICE_LINE does not immediately include in the total of INVT_QTY in the INVENTORY entity. Only when the transaction is completed, meaning we receive and pay the orders in real life, do the quantities in the invoice_line add up to the total amount in the inventory of the particular item. 

# setting up the application
the database server is my computer, so hopefully the api can run while my PC is on. 
set these commands up in the terminal: 
pip install mysql-connector-python

pip install --upgrade pip

pip install flask

pip install flask_cors
