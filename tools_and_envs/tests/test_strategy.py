from patterns_lab.strategy_pricing import Order, NormalPricing, DiscountPricing

def test_normal_pricing():
    order = Order(base_price=100.0, strategy=NormalPricing())
    assert order.checkout() == 100.0

def test_discount_pricing():
    order = Order(base_price=100.0, strategy=DiscountPricing())
    assert order.checkout() == 80.0