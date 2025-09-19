import customtkinter as ctk
import tkinter.filedialog as filedialog
#from src.inventory import Inventory

class App(ctk.CTk):

    def add_product_dialog(self):
        AddProductDialog(self, self.inventory, self.refresh_table)

    def adjust_stock_dialog(self):
        AdjustStockDialog(self, self.inventory, self.refresh_table)
    
    def delete_product_dialog(self):
        DeleteProductDialog(self, self.inventory, self.refresh_table)

    def show_low_stock(self):
        for widget in self.table_frame.winfo_children():
            if widget.grid_info()["row"] > 0:
                widget.destroy()

        products = self.inventory.get_low_stock_products()
        for i, product in enumerate(products):
            sku_label = ctk.CTkLabel(self.table_frame, text=product.sku)
            sku_label.grid(row=i+1, column=0, padx=10, pady=2)
            name_label = ctk.CTkLabel(self.table_frame, text=product.name)
            name_label.grid(row=i+1, column=1, padx=10, pady=2)
            quantity_label = ctk.CTkLabel(self.table_frame, text=str(product.quantity), text_color="red")
            quantity_label.grid(row=i+1, column=2, padx=10, pady=2)
            supplier_label = ctk.CTkLabel(self.table_frame, text=product.supplier_id)
            supplier_label.grid(row=i+1, column=3, padx=10, pady=2)
        
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
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Success", "Inventory data imported successfully.")
        except Exception as e:
            import tkinter.messagebox as messagebox
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
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Success", "Inventory data exported successfully.")
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Failed to export data: {e}")
    
    def reset_view(self):
        self.refresh_table()

    def setup_buttons(self):
        self.add_button = ctk.CTkButton(self.button_frame, text="Add Product", command=self.add_product_dialog, fg_color="green", hover_color="darkgreen")
        self.add_button.pack(side="left", padx=5, pady=5)

        self.adjust_stock_button = ctk.CTkButton(self.button_frame, text="Adjust Stock", command=self.adjust_stock_dialog)
        self.adjust_stock_button.pack(side="left", padx=5, pady=5)

        self.delete_product_button = ctk.CTkButton(self.button_frame, text="Delete Product", command=self.delete_product_dialog, fg_color="red", hover_color="darkred")
        self.delete_product_button.pack(side="left", padx=5, pady=5)

        self.low_stock_button = ctk.CTkButton(self.button_frame, text="View Low Stock", command=self.show_low_stock)
        self.low_stock_button.pack(side="left", padx=5, pady=5)
        
        self.view_all_products_button = ctk.CTkButton(self.button_frame, text="View All Products", command=self.refresh_table)
        self.view_all_products_button.pack(side="left", padx=5, pady=5)
        
        self.import_button = ctk.CTkButton(self.button_frame, text="Open File", command=self.import_from_file)
        self.import_button.pack(side="right", padx=5, pady=5)
        
        self.export_button = ctk.CTkButton(self.button_frame, text="Save File", command=self.export_to_file)
        self.export_button.pack(side="right", padx=5, pady=5)

    # Call setup_buttons and table creation in __init__
    def __init__(self, inventory):
        super().__init__()
        
        self.inventory = inventory

        self.title("Simple Inventory System")
        self.geometry("1111x601")

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="x", padx=10, pady=5)
        
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.setup_buttons()
        self.create_product_table()
        self.refresh_table()


    def create_product_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        headers = ["SKU", "Name", "Quantity", "Supplier ID"]
        for i, header_text in enumerate(headers):
            label = ctk.CTkLabel(self.table_frame, text=header_text, font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=i, padx=10, pady=5)

    def refresh_table(self):
        for widget in self.table_frame.winfo_children():
            if widget.grid_info()["row"] > 0:
                widget.destroy()

        products = self.inventory.list_all_products()
        for i, product in enumerate(products):
            sku_label = ctk.CTkLabel(self.table_frame, text=product.sku)
            sku_label.grid(row=i+1, column=0, padx=10, pady=2)

            name_label = ctk.CTkLabel(self.table_frame, text=product.name)
            name_label.grid(row=i+1, column=1, padx=10, pady=2)

            if product.quantity <= self.inventory.LOW_STOCK_THRESHOLD:
                quantity_label = ctk.CTkLabel(self.table_frame, text=f"{product.quantity} ⚠️", text_color="red")
            else:
                quantity_label = ctk.CTkLabel(self.table_frame, text=str(product.quantity))
            quantity_label.grid(row=i+1, column=2, padx=10, pady=2)

            supplier_label = ctk.CTkLabel(self.table_frame, text=product.supplier_id)
            supplier_label.grid(row=i+1, column=3, padx=10, pady=2)

            self.table_frame.grid_columnconfigure(i, weight=1)
           
class AddProductDialog(ctk.CTkToplevel):
    def __init__(self, master, inventory, callback):
        super().__init__(master)
        self.inventory = inventory
        self.callback = callback
        
        self.title("Add New Product")
        self.geometry("300x350")
        
        self.transient(master)
        self.grab_set()

        # Labels and Entry fields
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

        # Buttons
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

        # Labels and Entry fields
        ctk.CTkLabel(self, text="SKU").pack(padx=10, pady=5)
        self.sku_entry = ctk.CTkEntry(self)
        self.sku_entry.pack(padx=10, pady=2)
        
        ctk.CTkLabel(self, text="Amount to Add/Subtract").pack(padx=10, pady=5)
        self.amount_entry = ctk.CTkEntry(self)
        self.amount_entry.pack(padx=10, pady=2)

        # Buttons
        ctk.CTkButton(self, text="Adjust Stock", command=self.adjust_stock).pack(padx=10, pady=10)
    
    def adjust_stock(self):
        try:
            sku = self.sku_entry.get()
            amount = int(self.amount_entry.get())

            self.inventory.adjust_product_stock(sku, amount)
            
            # Close the dialog and refresh the main table
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