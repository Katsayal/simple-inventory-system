import customtkinter as ctk
from src.inventory import Inventory

class App(ctk.CTk):
    def __init__(self, inventory):
        super().__init__()
        
        self.inventory = inventory

        self.title("Simple Inventory System")
        self.geometry("800x600")

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="x", padx=10, pady=5)
        
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Define placeholder commands BEFORE creating buttons
        self.add_product_dialog = lambda: print("Add Product Dialog called!")
        self.adjust_stock_dialog = lambda: print("Adjust Stock Dialog called!")
        self.show_low_stock = lambda: print("Show Low Stock called!")

        self.add_button = ctk.CTkButton(self.button_frame, text="Add Product", command=self.add_product_dialog)
        self.add_button.pack(side="left", padx=5, pady=5)

        self.adjust_stock_button = ctk.CTkButton(self.button_frame, text="Adjust Stock", command=self.adjust_stock_dialog)
        self.adjust_stock_button.pack(side="left", padx=5, pady=5)

        self.low_stock_button = ctk.CTkButton(self.button_frame, text="View Low Stock", command=self.show_low_stock)
        self.low_stock_button.pack(side="left", padx=5, pady=5)

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
            