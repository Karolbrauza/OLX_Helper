class MarketplaceOffer:
    def __init__(self, ID, name, price, description = None):
        self.ID = ID
        self.name = name
        self.price = price
        self.description = description