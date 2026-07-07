import pandas as pd

from scripts.scanner.repository import EquityRepository
from scripts.scanner.base import BaseScanner


class VolumeScanner(BaseScanner):

    def volume_breakout(
        self,
        multiplier=2,
        window=20
    ):

        print("Loading historical market data...")

        df = self.repo.get_all_data()

        # ----------------------------------
        # Keep only Equity shares
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
        # Rolling Average Volume
        # ----------------------------------

        df["avg_volume"] = (

            df.groupby("symbol")["ttl_trd_qnty"]

            .transform(

                lambda x:

                x.rolling(
                    window=window,
                    min_periods=window
                ).mean()

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
        # Relative Volume
        # ----------------------------------

        latest_df["volume_ratio"] = (

            latest_df["ttl_trd_qnty"]

            /

            latest_df["avg_volume"]

        )

        # ----------------------------------
        # Scanner
        # ----------------------------------

        
        result = latest_df[
                    (latest_df["volume_ratio"] >= multiplier)
                    & (latest_df["ttl_trd_qnty"] >= 100000)
                    & (latest_df["no_of_trades"] >= 500)
                ]

        

        return result.sort_values(

            "volume_ratio",

            ascending=False

        )