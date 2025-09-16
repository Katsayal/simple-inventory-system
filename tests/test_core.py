import sys
print("PYTHONPATH sys.path =", sys.path)
import pytest
from src.inventory import Product, Inventory

def test_product_adjust_stock_positive():
    """Test that adjusting stock with a positive amount works correctly."""
    product = Product(sku="ABC-1001", name="Test Product", quantity=10, supplier_id="SUP1")
    product.adjust_stock(5)
    assert product.quantity == 15, "Stock quantity should be 15 after adding 5"

def test_product_adjust_stock_negative_raises_error():
    """Test that adjusting stock to a negative quantity raises a ValueError."""
    product = Product(sku="ABC-1001", name="Test Product", quantity=10, supplier_id="SUP1")
    with pytest.raises(ValueError):
        product.adjust_stock(-11)

def test_get_low_stock_products():
    """Test that the get_low_stock_products method correctly identifies low-stock items."""
    inventory = Inventory()
    # Update SKUs to match the regex: three letters and four digits
    inventory.add_product(Product("HIG-0010", "High Stock Item", 10, "SUP1"))
    inventory.add_product(Product("LOW-0020", "Low Stock Item", 3, "SUP2"))
    inventory.add_product(Product("MID-0030", "Mid Stock Item", 5, "SUP3"))

    low_stock_items = inventory.get_low_stock_products()
    low_stock_skus = {p.sku for p in low_stock_items}

    assert len(low_stock_items) == 2, "There should be exactly 2 low-stock items"
    assert "LOW-0020" in low_stock_skus, "LOW-0020 should be in the low-stock list"
    assert "MID-0030" in low_stock_skus, "MID-0030 should be in the low-stock list"
    assert "HIG-0010" not in low_stock_skus, "HIG-0010 should not be in the low-stock list"