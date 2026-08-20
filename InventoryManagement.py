class InventoryError(Exception):
    pass


class Warehouse:
    def __init__(self, name):
        self.name = name
        self.stock = {}
        self.reorder_threshold = {}

    def add_product(self, product_id, quantity, threshold=10):
        if quantity < 0:
            raise InventoryError("Quantity cannot be negative")
        self.stock[product_id] = self.stock.get(product_id, 0) + quantity
        if product_id not in self.reorder_threshold:
            self.reorder_threshold[product_id] = threshold

    def remove_product(self, product_id, quantity):
        if product_id not in self.stock:
            raise InventoryError("Product not found")
        if quantity < 0:
            raise InventoryError("Quantity cannot be negative")
        if self.stock[product_id] < quantity:
            raise InventoryError("Insufficient inventory")
        self.stock[product_id] -= quantity

    def get_quantity(self, product_id):
        return self.stock.get(product_id, 0)

    def is_low_stock(self, product_id):
        threshold = self.reorder_threshold.get(product_id, 10)
        return self.get_quantity(product_id) <= threshold


class Supplier:
    def __init__(self, supplier_id, name, products_supplied):
        self.supplier_id = supplier_id
        self.name = name
        self.products_supplied = products_supplied


class InventoryManagement:
    def __init__(self):
        self.warehouses = {
            "A": Warehouse("Warehouse A"),
            "B": Warehouse("Warehouse B"),
            "C": Warehouse("Warehouse C")
        }
        self.suppliers = {}

    def _validate_warehouse(self, warehouse_code):
        if warehouse_code not in self.warehouses:
            raise InventoryError("Invalid warehouse")

    def add_product(self, warehouse_code, product_id, quantity, threshold=10):
        self._validate_warehouse(warehouse_code)
        self.warehouses[warehouse_code].add_product(product_id, quantity, threshold)

    def remove_product(self, warehouse_code, product_id, quantity):
        self._validate_warehouse(warehouse_code)
        self.warehouses[warehouse_code].remove_product(product_id, quantity)

    def transfer_stock(self, from_code, to_code, product_id, quantity):
        self._validate_warehouse(from_code)
        self._validate_warehouse(to_code)
        self.warehouses[from_code].remove_product(product_id, quantity)
        self.warehouses[to_code].add_product(product_id, quantity)

    def register_supplier(self, supplier_id, name, products_supplied):
        self.suppliers[supplier_id] = Supplier(supplier_id, name, products_supplied)

    def reorder(self, warehouse_code, product_id, supplier_id, quantity):
        self._validate_warehouse(warehouse_code)
        if supplier_id not in self.suppliers:
            raise InventoryError("Supplier not found")
        supplier = self.suppliers[supplier_id]
        if product_id not in supplier.products_supplied:
            raise InventoryError("Supplier does not supply this product")
        self.warehouses[warehouse_code].add_product(product_id, quantity)
        return quantity

    def low_stock_report(self):
        report = {}
        for code, warehouse in self.warehouses.items():
            low_items = [pid for pid in warehouse.stock if warehouse.is_low_stock(pid)]
            if low_items:
                report[code] = low_items
        return report

    def select_warehouse_for_order(self, product_id, quantity):
        candidates = [
            (code, warehouse.get_quantity(product_id))
            for code, warehouse in self.warehouses.items()
            if warehouse.get_quantity(product_id) >= quantity
        ]
        if not candidates:
            raise InventoryError("No warehouse has sufficient inventory")
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]

    def fulfill_order(self, product_id, quantity):
        warehouse_code = self.select_warehouse_for_order(product_id, quantity)
        self.warehouses[warehouse_code].remove_product(product_id, quantity)
        return warehouse_code


def main():
    inventory = InventoryManagement()
    inventory.add_product("A", "P100", 50, threshold=10)
    inventory.add_product("B", "P100", 5, threshold=10)
    inventory.add_product("C", "P100", 20, threshold=10)
    inventory.register_supplier("S1", "TechSupplies", ["P100"])
    print("Low stock report:", inventory.low_stock_report())
    warehouse_used = inventory.fulfill_order("P100", 15)
    print("Order fulfilled from:", warehouse_used)
    inventory.transfer_stock("A", "B", "P100", 10)
    reordered = inventory.reorder("B", "P100", "S1", 30)
    print("Reordered quantity:", reordered)


if __name__ == "__main__":
    main()
