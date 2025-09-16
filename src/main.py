from inventory import Inventory, Product

def main():
    inventory = Inventory()
    inventory.load_from_csv("data/inventory.csv")
    
    print("All products:")
    for p in inventory.list_all_products():
        print(f"{p.sku} | {p.name} | Qty: {p.quantity} | Supplier: {p.supplier_id}")
    
    print("\nLow stock products:")
    for p in inventory.get_low_stock_products():
        print(f"{p.sku} | {p.name} | Qty: {p.quantity}")

if __name__ == "__main__":
    main()
