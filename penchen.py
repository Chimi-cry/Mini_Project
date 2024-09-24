import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# ----------------------- Database Helper Functions -----------------------

def register_user(username, password):
    """Register a new user with username and password."""
    conn = sqlite3.connect('food_delivery.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    """Authenticate user credentials."""
    conn = sqlite3.connect('food_delivery.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_menu_items():
    """Retrieve all menu items from the database."""
    conn = sqlite3.connect('food_delivery.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MenuItems")
    items = cursor.fetchall()
    conn.close()
    return items

def place_order(user_id, cart):
    """Place an order with the selected cart items."""
    conn = sqlite3.connect('food_delivery.db')
    cursor = conn.cursor()
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Pending"
    cursor.execute("INSERT INTO Orders (user_id, order_date, status) VALUES (?, ?, ?)", (user_id, order_date, status))
    order_id = cursor.lastrowid
    for item_id, quantity in cart.items():
        cursor.execute("INSERT INTO OrderItems (order_id, menu_item_id, quantity) VALUES (?, ?, ?)", (order_id, item_id, quantity))
    conn.commit()
    conn.close()
    return order_id

# ----------------------- GUI Classes -----------------------

class LoginWindow:
    """Login Window Class"""
    def __init__(self, master):
        self.master = master
        master.title("Food Delivery - Login")
        master.geometry("600x500")  # Larger window size for laptop
        master.configure(bg="#f0f8ff")  # AliceBlue background
        master.resizable(False, False)  # Fixed size

        # Main Frame
        self.frame = tk.Frame(master, bg="#f0f8ff")
        self.frame.pack(expand=True)

        # Logo or Title
        self.title_label = tk.Label(self.frame, text="Welcome to FoodExpress", font=("Helvetica", 24, "bold"), bg="#f0f8ff", fg="#2e8b57")
        self.title_label.pack(pady=30)

        # Login Label
        self.label = tk.Label(self.frame, text="Login", font=("Helvetica", 18), bg="#f0f8ff")
        self.label.pack(pady=10)

        # Username
        self.username_label = tk.Label(self.frame, text="Username", font=("Helvetica", 14), bg="#f0f8ff")
        self.username_label.pack(pady=(20, 5))
        self.username_entry = tk.Entry(self.frame, font=("Helvetica", 14), width=30)
        self.username_entry.pack(pady=5)

        # Password
        self.password_label = tk.Label(self.frame, text="Password", font=("Helvetica", 14), bg="#f0f8ff")
        self.password_label.pack(pady=(20, 5))
        self.password_entry = tk.Entry(self.frame, show="*", font=("Helvetica", 14), width=30)
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_button = tk.Button(self.frame, text="Login", command=self.login, bg="#2e8b57", fg="white", font=("Helvetica", 14), width=20)
        self.login_button.pack(pady=30)

        # Register Button
        self.register_button = tk.Button(self.frame, text="Register", command=self.open_register_window, bg="#4682b4", fg="white", font=("Helvetica", 14), width=20)
        self.register_button.pack()

    def login(self):
        """Handle user login."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        user = login_user(username, password)
        if user:
            messagebox.showinfo("Success", "Logged in successfully!")
            self.master.destroy()
            root = tk.Tk()
            app = MenuWindow(root, user)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def open_register_window(self):
        """Open the registration window."""
        register_root = tk.Toplevel(self.master)
        RegisterWindow(register_root)

class RegisterWindow:
    """Registration Window Class"""
    def __init__(self, master):
        self.master = master
        master.title("Register")
        master.geometry("600x500")  # Larger window size for laptop
        master.configure(bg="#fffaf0")  # FloralWhite background
        master.resizable(False, False)  # Fixed size

        # Main Frame
        self.frame = tk.Frame(master, bg="#fffaf0")
        self.frame.pack(expand=True)

        # Register Label
        self.label = tk.Label(self.frame, text="Register", font=("Helvetica", 18), bg="#fffaf0")
        self.label.pack(pady=10)

        # Username
        self.username_label = tk.Label(self.frame, text="Username", font=("Helvetica", 14), bg="#fffaf0")
        self.username_label.pack(pady=(20, 5))
        self.username_entry = tk.Entry(self.frame, font=("Helvetica", 14), width=30)
        self.username_entry.pack(pady=5)

        # Password
        self.password_label = tk.Label(self.frame, text="Password", font=("Helvetica", 14), bg="#fffaf0")
        self.password_label.pack(pady=(20, 5))
        self.password_entry = tk.Entry(self.frame, show="*", font=("Helvetica", 14), width=30)
        self.password_entry.pack(pady=5)

        # Register Button
        self.register_button = tk.Button(self.frame, text="Register", command=self.register, bg="#2e8b57", fg="white", font=("Helvetica", 14), width=20)
        self.register_button.pack(pady=30)

    def register(self):
        """Handle user registration."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        if register_user(username, password):
            messagebox.showinfo("Success", "Registered successfully!")
            self.master.destroy()
        else:
            messagebox.showerror("Error", "Username already exists.")

class MenuWindow:
    """Menu Window Class"""
    def __init__(self, master, user):
        self.master = master
        self.user = user
        master.title("Menu")
        master.geometry("1000x700")  # Significantly larger window size
        master.configure(bg="#f5f5dc")  # Beige background
        master.resizable(True, True)  # Allow resizing

        # Main Frame
        self.frame = tk.Frame(master, bg="#f5f5dc")
        self.frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Welcome Label
        self.welcome_label = tk.Label(self.frame, text=f"Welcome, {self.user[1]}!", font=("Helvetica", 16), bg="#f5f5dc", fg="#8b4513")
        self.welcome_label.pack(pady=(0, 20))

        # Menu Label
        self.label = tk.Label(self.frame, text="Our Menu", font=("Helvetica", 24, "bold"), bg="#f5f5dc", fg="#8b4513")
        self.label.pack(pady=10)

        # Treeview Frame
        self.tree_frame = tk.Frame(self.frame, bg="#f5f5dc")
        self.tree_frame.pack(fill='both', expand=True)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.tree_frame)
        self.scrollbar.pack(side='right', fill='y')

        # Treeview for Menu Items
        self.tree = ttk.Treeview(self.tree_frame, columns=("Name", "Description", "Price"), show='headings', yscrollcommand=self.scrollbar.set)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Price", text="Price")
        self.tree.column("Name", anchor='center', width=250)
        self.tree.column("Description", anchor='w', width=600)
        self.tree.column("Price", anchor='center', width=150)
        self.tree.pack(fill='both', expand=True)
        self.scrollbar.config(command=self.tree.yview)

        self.populate_menu()

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.frame, bg="#f5f5dc")
        self.buttons_frame.pack(pady=30)

        # Add to Cart Button
        self.add_button = tk.Button(self.buttons_frame, text="Add to Cart", command=self.add_to_cart, bg="#8b4513", fg="white", font=("Helvetica", 14), width=20)
        self.add_button.pack(side='left', padx=20)

        # View Cart Button
        self.view_cart_button = tk.Button(self.buttons_frame, text="View Cart", command=self.view_cart, bg="#a0522d", fg="white", font=("Helvetica", 14), width=20)
        self.view_cart_button.pack(side='left', padx=20)

        # Logout Button
        self.logout_button = tk.Button(self.buttons_frame, text="Logout", command=self.logout, bg="#dc143c", fg="white", font=("Helvetica", 14), width=20)
        self.logout_button.pack(side='left', padx=20)

    def populate_menu(self):
        """Populate the Treeview with menu items."""
        items = get_menu_items()
        for item in items:
            self.tree.insert('', 'end', iid=item[0], values=(item[1], item[2], f"${item[3]:.2f}"))

    def add_to_cart(self):
        """Add selected item to the cart."""
        selected = self.tree.focus()
        if selected:
            item_id = int(selected)
            if item_id in self.cart:
                self.cart[item_id] += 1
            else:
                self.cart[item_id] = 1
            messagebox.showinfo("Cart", "Item added to cart.")
        else:
            messagebox.showerror("Error", "No item selected.")

    def view_cart(self):
        """Open the cart window."""
        if not self.cart:
            messagebox.showinfo("Cart", "Your cart is empty.")
            return
        cart_window = tk.Toplevel(self.master)
        CartWindow(cart_window, self.cart, self.user)

    def logout(self):
        """Logout the current user."""
        self.master.destroy()
        root = tk.Tk()
        app = LoginWindow(root)
        root.mainloop()

class CartWindow:
    """Cart Window Class"""
    def __init__(self, master, cart, user):
        self.master = master
        self.cart = cart
        self.user = user
        master.title("Your Cart")
        master.geometry("800x600")  # Larger window size for cart
        master.configure(bg="#e6e6fa")  # Lavender background
        master.resizable(False, False)  # Fixed size

        # Main Frame
        self.frame = tk.Frame(master, bg="#e6e6fa")
        self.frame.pack(fill='both', expand=True, padx=30, pady=30)

        # Cart Label
        self.label = tk.Label(self.frame, text="Your Cart", font=("Helvetica", 24, "bold"), bg="#e6e6fa", fg="#4b0082")
        self.label.pack(pady=10)

        # Treeview Frame
        self.tree_frame = tk.Frame(self.frame, bg="#e6e6fa")
        self.tree_frame.pack(fill='both', expand=True)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self.tree_frame)
        self.scrollbar.pack(side='right', fill='y')

        # Treeview for Cart Items
        self.tree = ttk.Treeview(self.tree_frame, columns=("Name", "Quantity", "Price"), show='headings', yscrollcommand=self.scrollbar.set)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.column("Name", anchor='center', width=350)
        self.tree.column("Quantity", anchor='center', width=150)
        self.tree.column("Price", anchor='center', width=150)
        self.tree.pack(fill='both', expand=True)
        self.scrollbar.config(command=self.tree.yview)

        self.populate_cart()

        # Total Price Label
        self.total_label = tk.Label(self.frame, text=f"Total: ${self.calculate_total():.2f}", font=("Helvetica", 16, "bold"), bg="#e6e6fa", fg="#4b0082")
        self.total_label.pack(pady=20)

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.frame, bg="#e6e6fa")
        self.buttons_frame.pack(pady=20)

        # Place Order Button
        self.order_button = tk.Button(self.buttons_frame, text="Place Order", command=self.place_order, bg="#4b0082", fg="white", font=("Helvetica", 14), width=20)
        self.order_button.pack(side='left', padx=20)

        # Close Button
        self.close_button = tk.Button(self.buttons_frame, text="Close", command=self.master.destroy, bg="#696969", fg="white", font=("Helvetica", 14), width=20)
        self.close_button.pack(side='left', padx=20)

    def populate_cart(self):
        """Populate the Treeview with cart items."""
        for item_id, quantity in self.cart.items():
            conn = sqlite3.connect('food_delivery.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name, price FROM MenuItems WHERE id=?", (item_id,))
            item = cursor.fetchone()
            conn.close()
            if item:
                name, price = item
                total_price = price * quantity
                self.tree.insert('', 'end', values=(name, quantity, f"${total_price:.2f}"))

    def calculate_total(self):
        """Calculate the total price of items in the cart."""
        total = 0
        for item_id, quantity in self.cart.items():
            conn = sqlite3.connect('food_delivery.db')
            cursor = conn.cursor()
            cursor.execute("SELECT price FROM MenuItems WHERE id=?", (item_id,))
            item = cursor.fetchone()
            conn.close()
            if item:
                price = item[0]
                total += price * quantity
        return total

    def place_order(self):
        """Place the order and clear the cart."""
        order_id = place_order(self.user[0], self.cart)
        messagebox.showinfo("Success", f"Order #{order_id} placed successfully!")
        self.master.destroy()

# ----------------------- Database Initialization -----------------------

def initialize_database():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect('food_delivery.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Create MenuItems table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MenuItems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        )
    ''')

    # Create Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            order_date TEXT,
            status TEXT,
            FOREIGN KEY(user_id) REFERENCES Users(id)
        )
    ''')

    # Create OrderItems table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OrderItems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            menu_item_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY(order_id) REFERENCES Orders(id),
            FOREIGN KEY(menu_item_id) REFERENCES MenuItems(id)
        )
    ''')

    # Check if MenuItems is empty, then populate
    cursor.execute("SELECT COUNT(*) FROM MenuItems")
    count = cursor.fetchone()[0]
    if count == 0:
        populate_menu_items(cursor)

    conn.commit()
    conn.close()

def populate_menu_items(cursor):
    """Populate the MenuItems table with sample data."""
    menu = [
        ("Pizza Margherita", "Classic delight with 100% real mozzarella cheese", 8.99),
        ("Veggie Burger", "Loaded with fresh veggies and sauces", 5.49),
        ("Pasta Alfredo", "Creamy Alfredo sauce with fettuccine", 7.99),
        ("Caesar Salad", "Crisp romaine lettuce with Caesar dressing", 4.99),
        ("Grilled Chicken Sandwich", "Juicy grilled chicken with fresh lettuce and tomato", 6.99),
        ("French Fries", "Crispy golden fries", 2.99),
        ("Chocolate Milkshake", "Rich and creamy chocolate shake", 3.99),
        ("Spaghetti Bolognese", "Spaghetti with hearty meat sauce", 7.49),
        ("Tacos", "Spicy beef tacos with fresh toppings", 5.99),
        ("Sushi Platter", "Assorted sushi rolls with wasabi and soy sauce", 12.99),
        ("BBQ Ribs", "Tender ribs with smoky barbecue sauce", 14.99),
        ("Chicken Wings", "Spicy buffalo wings with blue cheese dip", 9.99),
        ("Ice Cream Sundae", "Vanilla ice cream with chocolate syrup and nuts", 4.49),
        ("Steak", "Grilled sirloin steak with garlic butter", 19.99),
        ("Fish and Chips", "Battered fish with crispy fries and tartar sauce", 11.99)
    ]
    cursor.executemany("INSERT INTO MenuItems (name, description, price) VALUES (?, ?, ?)", menu)

# ----------------------- Main Application -----------------------

if __name__ == "__main__":
    initialize_database()
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
