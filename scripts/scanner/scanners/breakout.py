import pandas as pd

from scripts.scanner.base import BaseScanner


class BreakoutScanner(BaseScanner):

    def price_breakout(
        self,
        window=20
    ):

        print("Loading historical market data...")

        df = self.repo.get_all_data()

        # ----------------------------------
        # Equity only
        # ----------------------------------

        df = df[
            df["series"] == "EQ"
        ].copy()

        # ----------------------------------
        # Sort
        # ----------------------------------

        df = df.sort_values(
            [
                "symbol",
                "trade_date"
            ]
        )

        # ----------------------------------
        # Previous 20-Day High
        # ----------------------------------

        df["previous_high"] = (

            df.groupby("symbol")["high_price"]

            .transform(

                lambda x:

                x.shift(1)

                .rolling(
                    window=window,
                    min_periods=window
                )

                .max()

            )

        )

        # ----------------------------------
        # Latest Trading Day
        # ----------------------------------

        latest = self.repo.get_latest_date()

        latest_df = df[
            df["trade_date"] == latest
        ].copy()

        # ----------------------------------
        # Breakout
        # ----------------------------------

        result = latest_df[

            latest_df["close_price"]

            >

            latest_df["previous_high"]

        ]

        return result.sort_values(

            "close_price",

            ascending=False

        )