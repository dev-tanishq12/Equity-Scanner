from scripts.scanner.repository import EquityRepository


class BaseScanner:

    def __init__(self):

        self.repo = EquityRepository()

    # ----------------------------------
    # Latest Trading Date
    # ----------------------------------

    def latest_date(self):

        return self.repo.get_latest_date()

    # ----------------------------------
    # Symbol List
    # ----------------------------------

    def symbols(self):

        return self.repo.get_symbols()

    # ----------------------------------
    # Standard Market Dataset
    # ----------------------------------

    def get_market_data(self):

        df = self.repo.get_all_data()

        df = df[
            df["series"] == "EQ"
        ].copy()

        df = df.sort_values(
            [
                "symbol",
                "trade_date"
            ]
        )

        df.reset_index(
            drop=True,
            inplace=True
        )

        return df