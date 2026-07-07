from scripts.scanner.repository import EquityRepository


class BaseScanner:

    def __init__(self):

        self.repo = EquityRepository()

    def latest_date(self):

        return self.repo.get_latest_date()

    def symbols(self):

        return self.repo.get_symbols()
    
    def get_market_data(self):

        df = self.repo.get_all_data()

        df = df[df["series"] == "EQ"].copy()

        df = df.sort_values(
        ["symbol", "trade_date"]
    )

        return df