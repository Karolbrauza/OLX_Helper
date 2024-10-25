class MarketplaceOffer:
    def __init__(self, ID, name, price, description = None):
        self.ID = ID
        self.name = name
        self.price = price
        self.description = description
        
    def to_dict(self):
        return {
            'ID': self.ID,
            'Name': self.name,
            'Price': self.price,
            'Description': self.description
        }