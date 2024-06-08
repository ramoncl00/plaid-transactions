class Transaction:
    def __init__(
            self,
            amount: float,
            iso_currency_code: str,
            category: [str],
            date: str,
            authorized_date: str,
            name: str,
            merchant_name: str,
            pending: bool):
        self.amount = amount
        self.iso_currency_code = iso_currency_code
        self.category = category
        self.date = date
        self.authorized_date = authorized_date
        self.name = name
        self.merchant_name = merchant_name
        self.pending = pending