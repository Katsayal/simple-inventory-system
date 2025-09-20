import customtkinter as ctk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
from src.inventory import Inventory, Product
from PIL import Image

class App(ctk.CTk):
    def __init__(self, inventory):
        super().__init__()
        
        self.inventory = inventory
        self.current_sort_column = None
        self.sort_ascending = True

        self.title("Simple Inventory System")
        self.geometry("1151x601")

        self.dashboard_frame = ctk.CTkFrame(self)
        self.dashboard_frame.pack(fill="x", padx=10, pady=5)
        
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="x", padx=10, pady=5)
        
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(fill="x", padx=10, pady=5)

        self.table_scroll_frame = ctk.CTkScrollableFrame(self)
        self.table_scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.setup_icons()
        self.setup_dashboard()
        self.setup_buttons()
        self.setup_search_bar()
        self.create_product_table()
        self.refresh_table()
        
    def setup_icons(self):
        icon_path = "assets/"
        self.add_icon = ctk.CTkImage(Image.open(f"{icon_path}add_icon.png"), size=(20, 20))
        self.delete_icon = ctk.CTkImage(Image.open(f"{icon_path}delete_icon.png"), size=(20, 20))
        self.save_icon = ctk.CTkImage(Image.open(f"{icon_path}save_icon.png"), size=(20, 20))
        self.open_icon = ctk.CTkImage(Image.open(f"{icon_path}open_icon.png"), size=(20, 20))
        self.adjust_icon = ctk.CTkImage(Image.open(f"{icon_path}adjust_icon.png"), size=(20, 20))
        self.search_icon = ctk.CTkImage(Image.open(f"{icon_path}search_icon.png"), size=(20, 20))
        
    def setup_dashboard(self):
        self.total_products_label = ctk.CTkLabel(self.dashboard_frame, text="Total Products: 0", font=ctk.CTkFont(size=16, weight="bold"))
        self.total_products_label.pack(side="left", padx=20, pady=5)
        
        self.low_stock_label = ctk.CTkLabel(self.dashboard_frame, text="Low Stock: 0", font=ctk.CTkFont(size=16, weight="bold"))
        self.low_stock_label.pack(side="left", padx=20, pady=5)
        
    def setup_buttons(self):
        self.add_button = ctk.CTkButton(self.button_frame, text="Add Product", command=self.add_product_dialog, fg_color="green", hover_color="darkgreen", image=self.add_icon)
        self.add_button.pack(side="left", padx=5, pady=5)

        self.adjust_stock_button = ctk.CTkButton(self.button_frame, text="Adjust Stock", command=self.adjust_stock_dialog, image=self.adjust_icon)
        self.adjust_stock_button.pack(side="left", padx=5, pady=5)
        
        self.delete_product_button = ctk.CTkButton(self.button_frame, text="Delete Product", command=self.delete_product_dialog, fg_color="red", hover_color="darkred", image=self.delete_icon)
        self.delete_product_button.pack(side="left", padx=5, pady=5)

        self.low_stock_button = ctk.CTkButton(self.button_frame, text="View Low Stock", command=self.show_low_stock)
        self.low_stock_button.pack(side="left", padx=5, pady=5)
        
        self.view_all_products_button = ctk.CTkButton(self.button_frame, text="View All Products", command=self.refresh_table)
        self.view_all_products_button.pack(side="left", padx=5, pady=5)
        
        self.import_button = ctk.CTkButton(self.button_frame, text="Open File", command=self.import_from_file, image=self.open_icon)
        self.import_button.pack(side="right", padx=5, pady=5)
        
        self.export_button = ctk.CTkButton(self.button_frame, text="Save File", command=self.export_to_file, image=self.save_icon)
        self.export_button.pack(side="right", padx=5, pady=5)

    def setup_search_bar(self):
        self.search_label = ctk.CTkLabel(self.search_frame, text="Search:")
        self.search_label.pack(side="left", padx=5, pady=5)
        
        search_input_frame = ctk.CTkFrame(self.search_frame, fg_color="transparent")
        search_input_frame.pack(side="left", padx=5, pady=5, fill="x", expand=True)
        
        self.search_icon_label = ctk.CTkLabel(search_input_frame, text="", image=self.search_icon)
        self.search_icon_label.pack(side="left", padx=(0, 5))
        
        self.search_entry = ctk.CTkEntry(search_input_frame, placeholder_text="Search by SKU or Name...")
        self.search_entry.pack(side="left", fill="x", expand=True)
        
        self.search_entry.bind("<KeyRelease>", self.search_products)
    
    def search_products(self, event=None):
        query = self.search_entry.get().lower()
        self.refresh_table(search_query=query)

    def create_product_table(self):
        headers = ["SKU", "Name", "Quantity", "Supplier ID"]
        for i, header_text in enumerate(headers):
            header_button = ctk.CTkButton(self.table_scroll_frame, text=header_text, 
                                          command=lambda col=header_text: self.sort_table(col),
                                          fg_color=("gray75", "gray25"),
                                          hover_color=("gray70", "gray30"))
            header_button.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            self.table_scroll_frame.grid_columnconfigure(i, weight=1)

    def sort_table(self, column):
        if self.current_sort_column == column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.current_sort_column = column
            self.sort_ascending = True

        self.refresh_table()

    def refresh_table(self, products=None, search_query=None):
        for widget in self.table_scroll_frame.winfo_children():
            if widget.grid_info()["row"] > 0:
                widget.destroy()

        if products is None:
            products = self.inventory.list_all_products()

        if search_query:
            products = [p for p in products if search_query in p.sku.lower() or search_query in p.name.lower()]

        if self.current_sort_column:
            sort_key_map = {
                "SKU": lambda p: p.sku,
                "Name": lambda p: p.name,
                "Quantity": lambda p: p.quantity,
                "Supplier ID": lambda p: p.supplier_id
            }
            products.sort(key=sort_key_map[self.current_sort_column], reverse=not self.sort_ascending)

        for i, product in enumerate(products):
            bg_color = ("#F0F0F0", "#303030") if i % 2 == 0 else ("white", "gray15")
            
            sku_label = ctk.CTkLabel(self.table_scroll_frame, text=product.sku, fg_color=bg_color)
            sku_label.grid(row=i+1, column=0, padx=10, pady=2, sticky="ew")

            name_label = ctk.CTkLabel(self.table_scroll_frame, text=product.name, fg_color=bg_color)
            name_label.grid(row=i+1, column=1, padx=10, pady=2, sticky="ew")

            if product.quantity <= self.inventory.LOW_STOCK_THRESHOLD:
                if product.quantity <= self.inventory.CRITICAL_STOCK_THRESHOLD:
                    quantity_label = ctk.CTkLabel(self.table_scroll_frame, text=f"{product.quantity} 🚨", text_color="orange", fg_color=bg_color)
                else:
                    quantity_label = ctk.CTkLabel(self.table_scroll_frame, text=f"{product.quantity} ⚠️", text_color="red", fg_color=bg_color)
            else:
                quantity_label = ctk.CTkLabel(self.table_scroll_frame, text=str(product.quantity), fg_color=bg_color)
            
            quantity_label.grid(row=i+1, column=2, padx=10, pady=2, sticky="ew")
            quantity_label.bind("<Button-1>", lambda event, row=i+1, col=2, sku=product.sku: self.on_quantity_click(event, row, col, sku))
            
            supplier_label = ctk.CTkLabel(self.table_scroll_frame, text=product.supplier_id, fg_color=bg_color)
            supplier_label.grid(row=i+1, column=3, padx=10, pady=2, sticky="ew")

        self.total_products_label.configure(text=f"Total Products: {len(self.inventory.products)}")
        low_stock_count = len(self.inventory.get_low_stock_products())
        self.low_stock_label.configure(text=f"Low Stock: {low_stock_count}")
            
    def on_quantity_click(self, event, row, col, sku):
        label_to_replace = event.widget
        current_quantity = int(label_to_replace.cget("text").split()[0])
        
        entry = ctk.CTkEntry(self.table_scroll_frame, width=50)
        entry.insert(0, str(current_quantity))
        entry.grid(row=row, column=col, padx=10, pady=2)
        entry.focus_set()
        
        def save_and_refresh(event=None):
            try:
                new_quantity = int(entry.get())
                current_quantity = self.inventory.products[sku].quantity
                amount = new_quantity - current_quantity
                self.inventory.adjust_product_stock(sku, amount)
                self.refresh_table()
            except ValueError:
                messagebox.showerror("Invalid Input", "Quantity must be a number.")
                self.refresh_table()
            except KeyError:
                messagebox.showerror("Error", "Product not found.")
                self.refresh_table()
        
        entry.bind("<Return>", save_and_refresh)
        entry.bind("<FocusOut>", save_and_refresh)
        
    def show_low_stock(self):
        low_stock_products = self.inventory.get_low_stock_products()
        self.refresh_table(products=low_stock_products)

    def import_from_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".csv",
            filetypes=[("Spreadsheet Files", "*.csv *.xlsx")],
            title="Select Inventory File"
        )
        if not file_path:
            return
            
        try:
            self.inventory.load_from_file(file_path)
            self.refresh_table()
            messagebox.showinfo("Success", "Inventory data imported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data: {e}")

    def export_to_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Spreadsheet Files", "*.csv *.xlsx")],
            title="Save Inventory File"
        )
        if not file_path:
            return
            
        try:
            self.inventory.save_to_file(file_path)
            messagebox.showinfo("Success", "Inventory data exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}")

    def add_product_dialog(self):
        AddProductDialog(self, self.inventory, self.refresh_table)

    def adjust_stock_dialog(self):
        AdjustStockDialog(self, self.inventory, self.refresh_table)

    def delete_product_dialog(self):
        DeleteProductDialog(self, self.inventory, self.refresh_table)

class AddProductDialog(ctk.CTkToplevel):
    def __init__(self, master, inventory, callback):
        super().__init__(master)
        self.inventory = inventory
        self.callback = callback
        
        self.title("Add New Product")
        self.geometry("300x350")
        
        self.transient(master)
        self.grab_set()

        ctk.CTkLabel(self, text="SKU").pack(padx=10, pady=5)
        self.sku_entry = ctk.CTkEntry(self)
        self.sku_entry.pack(padx=10, pady=2)
        
        ctk.CTkLabel(self, text="Name").pack(padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(padx=10, pady=2)

        ctk.CTkLabel(self, text="Quantity").pack(padx=10, pady=5)
        self.quantity_entry = ctk.CTkEntry(self)
        self.quantity_entry.pack(padx=10, pady=2)

        ctk.CTkLabel(self, text="Supplier ID").pack(padx=10, pady=5)
        self.supplier_entry = ctk.CTkEntry(self)
        self.supplier_entry.pack(padx=10, pady=2)

        ctk.CTkButton(self, text="Add Product", command=self.add_product).pack(padx=10, pady=10)

    def add_product(self):
        try:
            sku = self.sku_entry.get()
            name = self.name_entry.get()
            quantity = int(self.quantity_entry.get())
            supplier_id = self.supplier_entry.get()
            
            if not name.strip():
                raise ValueError("Product name cannot be empty.")
            
            if not supplier_id.strip():
                raise ValueError("Supplier ID cannot be empty.")

            from src.inventory import Product
            new_product = Product(sku, name, quantity, supplier_id)
            self.inventory.add_product(new_product)
            
            self.destroy()
            self.callback()
            
        except ValueError as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Input Error: {e}")
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

class AdjustStockDialog(ctk.CTkToplevel):
    def __init__(self, master, inventory, callback):
        super().__init__(master)
        self.inventory = inventory
        self.callback = callback
        
        self.title("Adjust Product Stock")
        self.geometry("300x200")

        self.transient(master)
        self.grab_set()

        ctk.CTkLabel(self, text="SKU").pack(padx=10, pady=5)
        self.sku_entry = ctk.CTkEntry(self)
        self.sku_entry.pack(padx=10, pady=2)
        
        ctk.CTkLabel(self, text="Amount to Add/Subtract").pack(padx=10, pady=5)
        self.amount_entry = ctk.CTkEntry(self)
        self.amount_entry.pack(padx=10, pady=2)

        ctk.CTkButton(self, text="Adjust Stock", command=self.adjust_stock).pack(padx=10, pady=10)
    
    def adjust_stock(self):
        try:
            sku = self.sku_entry.get()
            amount = int(self.amount_entry.get())

            self.inventory.adjust_product_stock(sku, amount)
            
            self.destroy()
            self.callback()

        except KeyError:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Product with SKU '{sku}' not found.")
        except ValueError as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Input Error", f"Invalid input: {e}")
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

class DeleteProductDialog(ctk.CTkToplevel):
    def __init__(self, master, inventory, callback):
        super().__init__(master)
        self.inventory = inventory
        self.callback = callback

        self.title("Delete Product")
        self.geometry("300x150")

        self.transient(master)
        self.grab_set()

        ctk.CTkLabel(self, text="SKU").pack(padx=10, pady=5)
        self.sku_entry = ctk.CTkEntry(self)
        self.sku_entry.pack(padx=10, pady=2)

        ctk.CTkButton(self, text="Delete Product", command=self.delete_product).pack(padx=10, pady=10)

    def delete_product(self):
        try:
            sku = self.sku_entry.get()

            self.inventory.delete_product(sku)

            self.destroy()
            self.callback()

            import tkinter.messagebox as messagebox
            messagebox.showinfo("Success", f"Product with SKU '{sku}' deleted successfully.")
        except KeyError as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Deletion failed: {e}")
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")