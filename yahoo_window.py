import tkinter as tk
from tkinter import ttk
import yahoo_fin.stock_info as si
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class YahooWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Yahoo Finance Data")
        
        # Create label and entry for entering stock symbol for Yahoo Finance data
        yahoo_label = ttk.Label(self.root, text="Enter Stock Symbol for Yahoo Finance Data:")
        yahoo_label.pack()
        self.yahoo_entry = ttk.Entry(self.root)
        self.yahoo_entry.pack()
        
        # Create button to fetch Yahoo Finance data
        yahoo_button = ttk.Button(self.root, text="Fetch Yahoo Data", command=self.fetch_yahoo_data)

        yahoo_button.pack()

    # Function to fetch Yahoo Finance data and display in a new window
    def fetch_yahoo_data(self):
        # Get the stock symbol entered by the user
        stock_symbol = self.yahoo_entry.get()

        # Fetch historical stock data
        try:
            stock_data = si.get_data(stock_symbol)
        except Exception as e:
            print("Error fetching stock data:", e)
            return
    
        # Filter data for the past 6 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=6*30)
        stock_data = stock_data[(stock_data.index >= start_date) & (stock_data.index <= end_date)]

        # Create a new Tkinter window for displaying the graph
        yahoo_window = tk.Toplevel()
        yahoo_window.title(f"Stock Price Graph for {stock_symbol}")
    
        # Plot the stock prices for the past 6 months
        fig, ax = plt.subplots(figsize=(8, 4))
        stock_data['adjclose'].plot(ax=ax, legend=True)
        ax.set_xlabel('Date')
        ax.set_ylabel('Stock Price')
        ax.set_title(f'Stock Price for {stock_symbol} (Past 6 Months)')
        plt.xticks(rotation=45)
    
        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=yahoo_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH,)
