class House:
    area: str
    cost: int

    def __init__(self, area, cost):
        self.area = area
        self.cost = cost


class Home(House):
    discount = 0

    def __init__(self, area, cost):
        super().__init__(area, cost)

    def apply_discount(self, discount):
        if 0 < discount <= 100:
            self.discount = discount
        else:
            raise ValueError("Invalid discount value. Discount must be in range 1 - 100%.")

    def count_price(self):
        if self.discount == 0:
            return self.cost
        else:
            return self.cost - self.cost/self.discount
