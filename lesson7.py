import pytest
from order_manager import OrderManager, Item


def test_total_empty():
    manager = OrderManager()
    assert manager.total() == 0


def test_total_with_items():
    items = [
        Item(name="Laptop", price=1000.0),
        Item(name="Mouse", price=50.0),
        Item(name="Keyboard", price=150.0)
    ]
    manager = OrderManager(items=items)
    assert manager.total() == 1200.0


def test_total_single_item():
    manager = OrderManager(items=[Item(name="Phone", price=500.0)])
    assert manager.total() == 500.0


def test_most_expensive_empty():
    manager = OrderManager()
    assert manager.most_expensive() is None


def test_most_expensive_valid():
    item1 = Item(name="Book", price=15.0)
    item2 = Item(name="Monitor", price=300.0)
    item3 = Item(name="Pen", price=2.0)
    
    manager = OrderManager(items=[item1, item2, item3])
    assert manager.most_expensive() == item2


def test_most_expensive_same_prices():
    item1 = Item(name="A", price=100.0)
    item2 = Item(name="B", price=100.0)
    manager = OrderManager(items=[item1, item2])
    assert manager.most_expensive() in [item1, item2]


@pytest.mark.parametrize("discount", [0, 10, 50, 100])
def test_apply_discount_valid(discount):
    item1 = Item(name="Item1", price=100.0)
    item2 = Item(name="Item2", price=200.0)
    manager = OrderManager(items=[item1, item2])
    
    manager.apply_discount(discount)
    
    expected_p1 = 100.0 * (1 - discount / 100)
    expected_p2 = 200.0 * (1 - discount / 100)
    
    assert item1.price == pytest.approx(expected_p1)
    assert item2.price == pytest.approx(expected_p2)
    assert manager.total() == pytest.approx(expected_p1 + expected_p2)


@pytest.mark.parametrize("invalid_discount", [-10, -0.01, 100.1, 150, "10%"])
def test_apply_discount_invalid(invalid_discount):
    manager = OrderManager(items=[Item(name="Test", price=100.0)])
    with pytest.raises((ValueError, TypeError)):
        manager.apply_discount(invalid_discount)


def test_apply_discount_empty_items():
    manager = OrderManager()
    manager.apply_discount(20)
    assert manager.total() == 0


def test_repr():
    items = [Item(name="Item1", price=50.0)]
    manager = OrderManager(items=items)
    repr_str = repr(manager)
    
    assert isinstance(repr_str, str)
    assert "OrderManager" in repr_str or "Item1" in repr_str