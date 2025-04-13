# as4_bot_and_data
Task 4.1 and 4.2

Contributors: Rakhat Sabina and Kozhakhmet Aruzhan
from MNU University

TASK 4.1 Financial Planner Pal Bot

A personal Telegram bot to help you plan your budget, track expenses and income – right inside your chat! Built with Python and `python-telegram-bot`.

Main Functions 

- Set budgets by category (`/config <category> <amount>`)
-  Log income and expenses (`/log income|expense <category> <amount>`)
-  Get financial summaries (`/summary`), calculates Total balance, income and expenses and divides them into categories.
-  Daily budget notifications (`/notifyon` / `/notifyoff`), when you turn notifications on you can see your daily transactions and also will recieve budget alerts
  in ase if your spendings exceed budget.
-  Clear all your data easily (`/clear`)
  

All data is stored per-user in simple `.csv` files using a lightweight persistent storage method.

All screenshots are available in the reposiroty.

How to run?

Requiered packages:
pip install requests python-telegram-bot 
pip install APScheduler

Take bot token and name from Bot Father
bot_token: Final = 'YOUR_BOT_TOKEN'
bot_user_name: Final = '@name_bot'

Run code from:
 main.py

 Notes
 
This bot stores data in .csv files, one per user, for simple and easy access.

It runs locally and uses a background scheduler for sending daily summaries.





 
