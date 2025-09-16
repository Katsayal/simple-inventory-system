import csv
import re
from typing import List

class Product:
    SKU_PATTERN = r"^[A-Z]{3}-\d{4}$"

    def __init__(self, sku: str, name: str, quantity: int, supplier_id: str):
        if not re.match(self.SKU_PATTERN, sku):
            raise ValueError(f"Invalid SKU format '{sku}'. Expected format: ABC-1234")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative on product creation")
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.supplier_id = supplier_id

    def adjust_stock(self, amount: int):
        if self.quantity + amount < 0:
            raise ValueError(f"Cannot reduce stock below zero for product {self.sku}")
        self.quantity += amount

    def to_dict(self):
        return {
            "sku": self.sku,
            "name": self.name,
            "quantity": str(self.quantity),
            "supplier_id": self.supplier_id,
        }

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact: str = ""):
        self.supplier_id = supplier_id
        self.name = name
        self.contact = contact

class Inventory:
    LOW_STOCK_THRESHOLD = 5

    def __init__(self):
        self.products = {}  # sku -> Product
        self.suppliers = {}  # supplier_id -> Supplier

    def load_from_csv(self, filepath: str):
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product = Product(
                    sku=row["sku"],
                    name=row["name"],
                    quantity=int(row["quantity"]),
                    supplier_id=row["supplier_id"]
                )
                self.products[product.sku] = product

    def save_to_csv(self, filepath: str):
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ["sku", "name", "quantity", "supplier_id"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products.values():
                writer.writerow(product.to_dict())

    def add_product(self, product: Product):
        if product.sku in self.products:
            raise ValueError(f"Product with SKU {product.sku} already exists.")
        self.products[product.sku] = product

    def adjust_product_stock(self, sku: str, amount: int):
        if sku not in self.products:
            raise KeyError(f"No product with SKU {sku}")
        self.products[sku].adjust_stock(amount)

    def get_low_stock_products(self) -> List[Product]:
        return [p for p in self.products.values() if p.quantity <= self.LOW_STOCK_THRESHOLD]

    def list_all_products(self) -> List[Product]:
        return list(self.products.values())
