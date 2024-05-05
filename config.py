# Define lists of tickers and stock information
tickers = ["RDW", "SKX", "ZS", "GMS", "AVGO", "CAH", "AMD", "FXAIX", "MSFT", "TCMD", "OXY", "META", "NVDA"]
avgcost = [100, 50, 75, 80, 120, 90, 110, 150, 200, 85, 70, 105, 180]  # Example average cost
quantity = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]  # Example quantity

# Function to add a new entry to the lists
def add_entry(ticker, avg_cost, qty):
    tickers.append(ticker)
    avgcost.append(avg_cost)
    quantity.append(qty)

# Function to remove an entry from the lists
def remove_entry(index):
    if 0 <= index < len(tickers):
        del tickers[index]
        del avgcost[index]
        del quantity[index]

# Function to update an existing entry in the lists
def update_entry(index, new_ticker, new_avg_cost, new_qty):
    if 0 <= index < len(tickers):
        tickers[index] = new_ticker
        avgcost[index] = new_avg_cost
        quantity[index] = new_qty
