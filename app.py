
import tkinter as tk
from tkinter import messagebox, ttk
import database


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("700x500")

        database.init_db()

        # -- LAYOUT FOR UI GOES HERE --
        input_frame = tk.LabelFrame(
            self.root,
            text="Item Details",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10)
        
        input_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(input_frame, text="Name:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.name_entry = tk.Entry(input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Quantity:").grid(
            row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.quantity_entry = tk.Entry(input_frame, width=10)
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Price:").grid(
            row=0, column=4, padx=5, pady=5, sticky="w")
        
        self.price_entry = tk.Entry(input_frame, width=10)
        self.price_entry.grid(row=0, column=5, padx=5, pady=5)

        # ---- Buttons ----
        button_frame = tk.Frame(self.root, pady=5)
        button_frame.pack()

        tk.Button(
            button_frame, text="Add Item", command=self.add_item).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame, text="Update Item", command=self.update_item).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame, text="Delete Item", command=self.delete_item).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame, text="Clear Fields", command=self.clear_fields).grid(row=0, column=3, padx=5)

        # ---- Table ----
        table_frame = tk.Frame(self.root, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Quantity", "Price"),
            show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=200)
        self.tree.column("Quantity", width=100)
        self.tree.column("Price", width=100)

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<ButtonRelease-1>", self.on_item_select)

        self.load_data()

    # ---- DATABASE INTEGRATION ----
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in database.get_all_items():
            self.tree.insert("", "end", values=item)

    def add_item(self):
        name = self.name_entry.get()
        qty = self.quantity_entry.get()
        price = self.price_entry.get()

        if not name or not qty or not price:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            database.add_item(name, int(qty), float(price))
            self.load_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Item added successfully.")

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Quantity must be an integer and Price must be a number.")

    def on_item_select(self, event):
        selected_row = self.tree.focus()

        if selected_row:
            values = self.tree.item(selected_row, "values")
            self.selected_id = values[0]

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])

            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, values[2])

            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, values[3])

    def update_item(self):
        if not hasattr(self, "selected_id"):
            messagebox.showerror(
                "Selection Error",
                "Please select an item to update")
            return

        name = self.name_entry.get()
        qty = self.quantity_entry.get()
        price = self.price_entry.get()

        if not name or not qty or not price:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            database.update_item(
                self.selected_id, name, int(qty), float(price))
            self.load_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Item updated successfully.")

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Quantity must be an integer and Price must be a number.")

    def delete_item(self):
        if not hasattr(self, "selected_id"):
            messagebox.showerror(
                "Selection Error",
                "Please select an item to delete.")
            return

        if messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this item?"):
            database.delete_item(self.selected_id)

            self.load_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Item deleted successfully.")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

        if hasattr(self, "selected_id"):
            del self.selected_id


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
