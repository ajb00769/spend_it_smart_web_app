class CategorySums:
    def __init__(self, purchase=0, debt=0, income=0, invest=0, sell=0):
        self.purchase = purchase
        self.debt = debt
        self.income = income
        self.invest = invest
        self.sell = sell

    def increment(self, category, amount):
        if hasattr(self, category):
            setattr(self, category, getattr(self, category) + amount)
