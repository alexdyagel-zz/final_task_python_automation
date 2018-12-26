# CoffeeForMe App
This app is a commandline utility that will be used by salesmen and managers of the “CoffeeForMe” company.

Script allows passing commandline arguments with :
  - User name.
  - User position. (Salesman or Manager are available).
  - Beverage type. Available for salesmen position only.
  - Additional beverage ingredients (sugar, cream, cinnamon…). Available for salesmen position only.
  - Get the beverage price. Available for salesmen position only.
  - Save the sale details in additional separate bill (file). Available for salesmen position only.
  - Show the summary of all the sales records, in case the utility is started by manager.

# Examples of running script

    python coffee_for_me.py --name Alex --position salesman --beverage latte    --ingredient milk --save_bill report.txt
    
    python coffee_for_me.py --name Artem --position manager
        
    python coffee_for_me.py
