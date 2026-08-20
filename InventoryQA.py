import unittest
from InventoryManagement import InventoryManagement, InventoryError


class InventoryQA(unittest.TestCase):
    def setUp(self):
        self.inventory = InventoryManagement()
        self.inventory.add_product("A", "P100", 50, threshold=10)
        self.inventory.add_product("B", "P100", 5, threshold=10)
        self.inventory.register_supplier("S1", "TechSupplies", ["P100"])

    def test_stock_availability(self):
        self.assertEqual(self.inventory.warehouses["A"].get_quantity("P100"), 50)

    def test_insufficient_inventory(self):
        with self.assertRaises(InventoryError):
            self.inventory.remove_product("B", "P100", 100)

    def test_warehouse_transfer(self):
        self.inventory.transfer_stock("A", "B", "P100", 10)
        self.assertEqual(self.inventory.warehouses["A"].get_quantity("P100"), 40)
        self.assertEqual(self.inventory.warehouses["B"].get_quantity("P100"), 15)

    def test_concurrent_orders(self):
        warehouse1 = self.inventory.fulfill_order("P100", 10)
        warehouse2 = self.inventory.fulfill_order("P100", 10)
        self.assertIn(warehouse1, ["A", "B", "C"])
        self.assertIn(warehouse2, ["A", "B", "C"])

    def test_reorder_threshold(self):
        self.assertTrue(self.inventory.warehouses["B"].is_low_stock("P100"))
        self.assertFalse(self.inventory.warehouses["A"].is_low_stock("P100"))

    def test_invalid_product(self):
        with self.assertRaises(InventoryError):
            self.inventory.remove_product("A", "P999", 1)

    def test_negative_inventory(self):
        with self.assertRaises(InventoryError):
            self.inventory.add_product("A", "P100", -10)

    def test_multiple_warehouses(self):
        self.inventory.add_product("C", "P100", 20)
        warehouse_used = self.inventory.select_warehouse_for_order("P100", 15)
        self.assertEqual(warehouse_used, "A")


if __name__ == "__main__":
    unittest.main()
