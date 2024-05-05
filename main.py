import tkinter as tk
from tkinter import ttk
import requests
from yahoo_window import YahooWindow  # Import the YahooWindow class from the module
import config  # Import the lists from config.py

# Function to fetch stock data from Financial Modeling Prep API
def get_stock_data(symbols):
    api_key = ""  # Replace with your API key
    url = f"https://financialmodelingprep.com/api/v3/quote/{','.join(symbols)}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to stop the scheduled updates and exit the program
def stop_updates():
    root.after_cancel(update_id)
    root.destroy()

# Function to update stock data and display in GUI
def update_stock_data():
    try:
        # Fetch stock data using lists from config.py
        stock_data = get_stock_data(config.tickers)
        if not stock_data:
            # Handle empty stock data
            return

        # Clear previous data from treeview
        for row in treeview.get_children():
            treeview.delete(row)

        total_profit_loss = 0

        # Insert new data into treeview
        for stock, avg, qty in zip(stock_data, config.avgcost, config.quantity):
            current_price = stock['price']
            profit_loss = round((current_price - avg) * qty, 2)
            total_profit_loss += profit_loss
            profit_loss_color = "green" if profit_loss >= 0 else "red"  # Set color based on profit or loss
            treeview.insert("", "end", values=(stock['symbol'], f"{current_price:.2f}", f"{profit_loss:.2f}"), tags=("profit" if profit_loss >= 0 else "loss",))

        # Insert separator line below the "Profit/Loss" column heading
        treeview.insert("", "end", values=("----------------", "", ""), tags="separator")

        # Insert total profit/loss at the bottom
        treeview.insert("", "end", values=("Total", "", f"{total_profit_loss:.2f}"), tags=("profit" if total_profit_loss >= 0 else "loss",))

        # Schedule the next update after 5 seconds
        global update_id
        update_id = root.after(5000, update_stock_data)
    except Exception as e:
        print("Error updating stock data:", e)

# Create tkinter window
root = tk.Tk()
root.title("Portfolio Visualization")

# Create treeview to display stock information
treeview = ttk.Treeview(root, columns=("Symbol", "Price", "Profit/Loss"), show="headings")
treeview.heading("Symbol", text="Symbol")
treeview.heading("Price", text="Price")
treeview.heading("Profit/Loss", text="Profit/Loss")
treeview.pack(fill="both", expand=True)

# Set column widths
treeview.column("Symbol", width=100, anchor="center")
treeview.column("Price", width=100, anchor="center")
treeview.column("Profit/Loss", width=100, anchor="center")

# Create tag for profit and loss rows
treeview.tag_configure("profit", foreground="green")
treeview.tag_configure("loss", foreground="red")

# Insert separator line below the "Profit/Loss" column heading
treeview.insert("", "end", values=("----------------", "", ""), tags="separator")

# Create instance of YahooWindow
yahoo_window = YahooWindow(root)

# Update stock data initially
update_stock_data()

# Bind the protocol for window close to stop the updates and exit the program
root.protocol("WM_DELETE_WINDOW", stop_updates)

# Run the tkinter event loop
root.mainloop()
