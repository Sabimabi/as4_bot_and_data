from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import csv
import os

# --- Bot Identification ---
bot_token: Final = '7914440539:AAFRUPqaJDeC1qW3DIpDLf4nDLmdWngH4VY'
bot_user_name: Final = '@financial_planner_pal_bot'

# Creates a folder to store user data
data_folder = 'user_data'
os.makedirs(data_folder, exist_ok=True)

#Gives the file path to a user's CSV file using their Telegram user ID

def get_user_file(user_id):
    return os.path.join(data_folder, f'{user_id}.csv')

#Loads user data from their CSV file.
#Gives a dictionary that includes the user's budgets, transactions, and notification setting.

def load_user_data(user_id):
    file_path = get_user_file(user_id)
    data = {'budgets': {}, 'transactions': [], 'notify': True}
    if os.path.exists(file_path):
        with open(file_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['type'] == 'budget':
                    data['budgets'][row['category']] = float(row['amount'])
                else:
                    data['transactions'].append({
                        'type': row['type'],
                        'category': row['category'],
                        'amount': float(row['amount'])
                    })
    return data

#Saves user data (budgets and transactions) to their CSV file.

def save_user_data(user_id, data):
    file_path = get_user_file(user_id)
    with open(file_path, 'w', newline='') as f:
        fieldnames = ['type', 'category', 'amount']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for cat, amt in data['budgets'].items():
            writer.writerow({'type': 'budget', 'category': cat, 'amount': amt})
        for t in data['transactions']:
            writer.writerow(t)

# Commands & bot functions in menu

#START, sends a welcome message when the user starts the bot.
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi, Buddy! I'm your Financial Planner Pal — here to help you track your money. \nUse /help to see what I can do!")

#HELP, lists all available commands

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        " Available Commands:\n"
        "/start – Start the bot\n"
        "/help – Show this help message\n"
        "/config <category> <amount> – Set a budget\n"
        "/log <income|expense> <category> <amount> – Log a transaction\n"
        "/summary – Show your financial summary\n"
        "/notifyon – Enable daily notifications\n"
        "/notifyoff – Disable daily notifications\n"
        "/clear – Delete all your data"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

#CONFIG,Sets budget limits for each category.

async def config_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if len(args) < 2:
        await update.message.reply_text("Usage: /config <category> <amount>")
        return
    category = args[0].lower()
    try:
        amount = float(args[1])
    except ValueError:
        await update.message.reply_text("Amount must be a number.")
        return
    data = load_user_data(user_id)
    data['budgets'][category] = amount
    save_user_data(user_id, data)
    await update.message.reply_text(f" Budget for '{category}' set to {amount}")

#LOG, tracks transactions 
async def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("Usage: /log <income|expense> <category> <amount>")
        return
    await handle_log(update, context.args)

#SUMMARY, Shows the user their income, expenses, balance, and budget status.
async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_user_data(user_id)
    if not data['transactions']:
        await update.message.reply_text("No data available.")
        return
    income = sum(t['amount'] for t in data['transactions'] if t['type'] == 'income')
    expenses = sum(t['amount'] for t in data['transactions'] if t['type'] == 'expense')
    balance = income - expenses

    summary = f"\U0001F4B0 Income: {income}\n"
    income_by_cat = {}
    expense_by_cat = {}
    for t in data['transactions']:
        if t['type'] == 'income':
            income_by_cat[t['category']] = income_by_cat.get(t['category'], 0) + t['amount']
        elif t['type'] == 'expense':
            expense_by_cat[t['category']] = expense_by_cat.get(t['category'], 0) + t['amount']
    for cat, amt in income_by_cat.items():
        summary += f"• {cat.capitalize()} Income: {amt}\n"
    summary += f"\n\U0001F4B8 Expenses: {expenses}\n"
    for cat, amt in expense_by_cat.items():
        summary += f"• {cat.capitalize()} Expense: {amt}\n"
    summary += f"\n\U0001F4CA Balance: {balance}\n\n\U0001F9FE Budgets:\n"
    for cat, limit in data['budgets'].items():
        spent = expense_by_cat.get(cat, 0)
        remaining = limit - spent
        if remaining < 0:
            status = "ATTENTION! Over budget!!!"
        elif remaining < 0.25 * limit:
            status = " Near limit!"
        else:
            status = "Done"
        summary += f"• {cat.capitalize()}: Budgeted {limit}, Spent {spent}, Remaining {remaining} {status}\n"
    await update.message.reply_text(summary, parse_mode='Markdown')

#NOTIFY ON
async def notifyon_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_user_data(user_id)
    data['notify'] = True
    save_user_data(user_id, data)
    await update.message.reply_text(" Daily notifications turned ON.")
    await send_daily_summary(context, user_id=user_id)

#NOTIFY OFF
async def notifyoff_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_user_data(user_id)
    data['notify'] = False
    save_user_data(user_id, data)
    await update.message.reply_text(" Notifications turned OFF.")

# CLEAR

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    file_path = get_user_file(user_id)
    if os.path.exists(file_path):
        os.remove(file_path)
        await update.message.reply_text(" All your data has been cleared. Start fresh anytime!")
    else:
        await update.message.reply_text("No data found to clear.")

# NATURAL TEXT HUNDLER, helps to accept answers without "/" sign

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    words = text.split()

    if not words:
        return await update.message.reply_text(" Please enter a valid command or use /help.")

    if words[0] == 'log':
        args = words[1:]
        await handle_log(update, args)
    elif words[0] == 'config':
        context.args = words[1:]
        await config_command(update, context)
    elif words[0] == 'clear':
        await clear_command(update, context)
    else:
        await update.message.reply_text("I did not understand that. Use /help to see available commands.")

async def handle_log(update: Update, args):
    user_id = update.effective_user.id
    if len(args) < 3:
        await update.message.reply_text("Usage: log <income|expense> <category> <amount>")
        return
    entry_type = args[0]
    category = args[1].lower()
    try:
        amount = float(args[2])
    except ValueError:
        await update.message.reply_text("Amount must be a number.")
        return
    data = load_user_data(user_id)
    data['transactions'].append({'type': entry_type, 'category': category, 'amount': amount})
    save_user_data(user_id, data)
    await update.message.reply_text(f" {entry_type.capitalize()} of {amount} logged under '{category}'.")

# === Daily Summary Scheduler ===

async def send_daily_summary(context: ContextTypes.DEFAULT_TYPE, user_id=None):
    user_ids = [int(f.split('.')[0]) for f in os.listdir(data_folder)] if user_id is None else [user_id]
    for uid in user_ids:
        data = load_user_data(uid)
        if not data.get('notify'):
            continue
        income = sum(t['amount'] for t in data['transactions'] if t['type'] == 'income')
        expenses = sum(t['amount'] for t in data['transactions'] if t['type'] == 'expense')
        balance = income - expenses
        budget_alerts = ""
        for category, limit in data.get('budgets', {}).items():
            spent = sum(t['amount'] for t in data['transactions'] if t['type'] == 'expense' and t['category'] == category)
            if spent >= limit:
                budget_alerts += f"ALERT! Budget exceeded in '{category}': {spent}/{limit}\n"
            elif spent >= 0.9 * limit:
                budget_alerts += f" ATTENTION! Nearing budget in '{category}': {spent}/{limit}\n"
        summary = (
            f"\U0001F4C5 *Daily Summary:*\n"
            f"\U0001F4B0 Income: {income}\n"
            f"\U0001F4B8 Expenses: {expenses}\n"
            f"\U0001F4CA Balance: {balance}\n\n" + budget_alerts
        )
        await context.bot.send_message(chat_id=uid, text=summary, parse_mode='Markdown')

# === Main App Entry Point ===

if __name__ == '__main__':
    print('Starting bot...')#to understand if the code started running 


    # Register bot commands
    app = Application.builder().token(bot_token).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('config', config_command))
    app.add_handler(CommandHandler('log', log_command))
    app.add_handler(CommandHandler('summary', summary_command))
    app.add_handler(CommandHandler('notifyon', notifyon_command))
    app.add_handler(CommandHandler('notifyoff', notifyoff_command))
    app.add_handler(CommandHandler('clear', clear_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # Schedule daily summary at 9 AM
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_daily_summary, 'cron', hour=9, args=[app])
    scheduler.start()

    print('Polling...')
    app.run_polling(poll_interval=3)

