import tkinter as tk
from tkinter import ttk, messagebox
import json
import matplotlib.pyplot as plt
from datetime import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Stock Trading Platform")
        self.geometry("800x600")  # Set initial size
        self.minsize(600, 400)    # Set minimum size

        self.frames = {}

        for F in (LoginPage, UserPage, AdminPage):
            frame = F(self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def load_stocks(self):
        try:
            with open("stocks.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_stocks(self, stocks):
        with open("stocks.json", "w") as f:
            json.dump(stocks, f)

class LoginPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ttk.Label(self, text="Login Page", font=("Helvetica", 18, "bold"))
        self.label.pack(pady=20)

        self.username_label = ttk.Label(self, text="Username:")
        self.username_label.pack()

        self.username_entry = ttk.Entry(self)
        self.username_entry.pack()

        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.pack()

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = ttk.Button(self, text="Login", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Assuming simple hardcoded authentication for demonstration
        if username == "admin" and password == "admin":
            self.master.show_frame("AdminPage")
        elif username == "user" and password == "user":
            self.master.show_frame("UserPage")
        else:
            messagebox.showerror("Error", "Invalid username or password")

class UserPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user_stocks = {}

        self.label = ttk.Label(self, text="User Page", font=("Helvetica", 18, "bold"))
        self.label.pack(pady=20)

        self.buy_frame = ttk.Frame(self)
        self.buy_frame.pack(side="left", padx=20)

        self.buy_label = ttk.Label(self.buy_frame, text="Available Stocks:")
        self.buy_label.pack()

        self.stocks = self.master.load_stocks()
        self.stock_vars = {}

        for symbol, data in self.stocks.items():
            stock_frame = ttk.Frame(self.buy_frame)
            stock_frame.pack(pady=5)

            stock_label = ttk.Label(stock_frame, text=f"{symbol}: {data['company_name']} - ${data['price']:.2f}")
            stock_label.pack(side="left")

            volume_var = tk.IntVar()
            volume_var.set(1)
            volume_entry = ttk.Entry(stock_frame, textvariable=volume_var, width=5)
            volume_entry.pack(side="left")

            buy_button = ttk.Button(stock_frame, text="Buy", command=lambda s=symbol: self.buy_stock(s, volume_var))
            buy_button.pack(side="left")

            self.stock_vars[symbol] = volume_var

        self.owned_frame = ttk.Frame(self)
        self.owned_frame.pack(side="right", padx=20)

        self.owned_label = ttk.Label(self.owned_frame, text="Your Stocks:")
        self.owned_label.pack()

        self.owned_stock_listbox = tk.Listbox(self.owned_frame)
        self.owned_stock_listbox.pack(fill="both", expand=True)

        self.chart_label = ttk.Label(self, text="Chart:")
        self.chart_label.pack()

        self.chart_canvas = tk.Canvas(self, bg="white", width=600, height=300)
        self.chart_canvas.pack()

        self.stock_selection_label = ttk.Label(self, text="Select Stock:")
        self.stock_selection_label.pack()

        self.selected_stock = tk.StringVar()
        self.stock_dropdown = ttk.Combobox(self, textvariable=self.selected_stock, state="readonly")
        self.stock_dropdown.pack()
        self.stock_dropdown.bind("<<ComboboxSelected>>", self.view_chart)

        self.update_stock_dropdown()
        self.view_chart()  # Initial chart display

        self.bind("<Visibility>", self.view_chart)  # Automatically display chart when page becomes visible
        self.owned_stock_listbox.bind("<<ListboxSelect>>", self.view_chart)  # Automatically display chart when stock is selected

        self.update_owned_stock_list()

        self.back_button = ttk.Button(self, text="Back to Login", command=self.go_to_login)
        self.back_button.pack(pady=20)

    def update_stock_dropdown(self):
        stocks = list(self.stocks.keys())
        self.stock_dropdown["values"] = stocks
        if stocks:
            self.selected_stock.set(stocks[0])

    def update_owned_stock_list(self):
        self.owned_stock_listbox.delete(0, tk.END)

        for symbol, quantity in self.user_stocks.items():
            self.owned_stock_listbox.insert(tk.END, f"{symbol}: {quantity}")

    def buy_stock(self, symbol, volume_var):
        volume = volume_var.get()
        stocks = self.master.load_stocks()

        if symbol not in stocks:
            messagebox.showerror("Error", f"Stock {symbol} not found.")
            return

        available_volume = stocks[symbol]["volume"]
        if available_volume < volume:
            messagebox.showerror("Error", "Not enough stocks available.")
            return

        # Calculate the price change ratio
        price_change_ratio = volume / available_volume * 0.1

        # Update the price
        stocks[symbol]["price"] *= (1 + price_change_ratio)

        # Update the prices in the graph
        for date, price in stocks[symbol]["prices"].items():
            stocks[symbol]["prices"][date] *= (1 + price_change_ratio)

        # Deduct the purchased volume from available volume
        stocks[symbol]["volume"] -= volume

        if symbol in self.user_stocks:
            self.user_stocks[symbol] += volume
        else:
            self.user_stocks[symbol] = volume

        self.master.save_stocks(stocks)
        self.update_owned_stock_list()
        self.view_chart()

        messagebox.showinfo("Buy Order", f"Successfully bought {volume} shares of {symbol}.")

    def view_chart(self, event=None):
        selected_stock = self.selected_stock.get()
        if selected_stock not in self.stocks:
            return

        prices = self.stocks[selected_stock].get("prices", {})
        dates = [datetime.strptime(date, "%Y-%m-%d") for date in prices.keys()]
        prices = list(prices.values())

        self.chart_canvas.delete("all")  # Clear previous chart
        fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
        ax.plot(dates, prices)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price ($)")
        ax.set_title(f"Stock Prices for {selected_stock}")
        fig.tight_layout()

        chart_img = fig2img(fig)
        self.chart_canvas.image = chart_img
        self.chart_canvas.create_image(0, 0, anchor="nw", image=chart_img)

    def go_to_login(self):
        self.master.show_frame("LoginPage")


class AdminPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ttk.Label(self, text="Admin Page", font=("Helvetica", 18, "bold"))
        self.label.pack(pady=20)

        self.symbol_label = ttk.Label(self, text="Symbol:").pack()
        self.symbol_entry = ttk.Entry(self)
        self.symbol_entry.pack()

        ttk.Label(self, text="Company Name:").pack()
        self.company_name_entry = ttk.Entry(self)
        self.company_name_entry.pack()

        ttk.Label(self, text="Price:").pack()
        self.price_entry = ttk.Entry(self)
        self.price_entry.pack()

        ttk.Label(self, text="Volume:").pack()
        self.volume_entry = ttk.Entry(self)
        self.volume_entry.pack()

        ttk.Button(self, text="Add Stock", command=self.add_stock).pack(pady=10)

        self.stocks_label = ttk.Label(self, text="Registered Stocks:", font=("Helvetica", 12, "bold"))
        self.stocks_label.pack()

        self.stocks_listbox = tk.Listbox(self)
        self.stocks_listbox.pack(fill="both", expand=True)

        self.update_stocks_list()

        ttk.Button(self, text="Back to Login", command=self.go_to_login).pack(pady=20)

    def add_stock(self):
        symbol = self.symbol_entry.get()
        company_name = self.company_name_entry.get()
        price = float(self.price_entry.get())
        volume = int(self.volume_entry.get())

        stocks = self.master.load_stocks()

        if symbol in stocks:
            messagebox.showerror("Error", f"Stock {symbol} already exists.")
            return

        stocks[symbol] = {
            "company_name": company_name,
            "price": price,
            "volume": volume,
            "prices": {}
        }

        self.master.save_stocks(stocks)
        messagebox.showinfo("Success", f"Stock {symbol} added successfully.")

        self.update_stocks_list()

    def update_stocks_list(self):
        self.stocks_listbox.delete(0, tk.END)
        stocks = self.master.load_stocks()

        for symbol, data in stocks.items():
            self.stocks_listbox.insert(tk.END, f"{symbol}: {data['company_name']}")

    def go_to_login(self):
        self.master.show_frame("LoginPage")


def fig2img(fig):
    """Convert matplotlib figure to Tkinter PhotoImage."""
    import io
    from PIL import Image, ImageTk

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img = Image.open(buf)
    return ImageTk.PhotoImage(img)


if __name__ == "__main__":
    app = App()
    app.mainloop()

