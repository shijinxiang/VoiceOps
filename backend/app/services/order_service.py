import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from backend.app.config import BASE_DIR

class OrderService:
    """
    Simulated Enterprise Order System (Read-Only).
    Provides order status, delivery history, warranty eligibility.
    """

    def __init__(self):
        self.orders: Dict[str, Dict[str, Any]] = {}
        self._load_mock_orders()

    def _load_mock_orders(self):
        orders_path = BASE_DIR / "dataset" / "orders" / "mock_orders.json"
        if orders_path.exists():
            with open(orders_path, "r", encoding="utf-8") as f:
                order_list = json.load(f)
                for order in order_list:
                    self.orders[order["order_id"]] = order

    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        if order_id not in self.orders:
            self._load_mock_orders()
        return self.orders.get(order_id)

    def search_by_phone(self, phone: str) -> List[Dict[str, Any]]:
        return [o for o in self.orders.values() if o.get("customer_phone") == phone]

    def list_all(self) -> List[Dict[str, Any]]:
        return list(self.orders.values())

order_service = OrderService()
