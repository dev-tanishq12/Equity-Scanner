import pandas as pd

from scripts.scanner.base import BaseScanner


class SmartMoneyScanner(BaseScanner):

    def scan(
        self,
        delivery=60,
        volume_ratio=2,
        breakout_percent=0
    ):

        print("Loading historical market data...")

        df = self.get_market_data()

        # ----------------------------------
        # Average Volume
        # ----------------------------------

        df["avg_volume"] = (

            df.groupby("symbol")["ttl_trd_qnty"]

            .transform(

                lambda x:

                x.rolling(
                    window=20,
                    min_periods=20
                ).mean()

            )

        )

        # ----------------------------------
        # Previous High
        # ----------------------------------

        df["previous_high"] = (

            df.groupby("symbol")["high_price"]

            .transform(

                lambda x:

                x.shift(1)

                .rolling(
                    window=20,
                    min_periods=20
                )

                .max()

            )

        )

        latest = self.latest_date()

        latest_df = df[
            df["trade_date"] == latest
        ].copy()

        # ----------------------------------
        # Indicators
        # ----------------------------------

        latest_df["volume_ratio"] = (
            latest_df["ttl_trd_qnty"]
            /
            latest_df["avg_volume"]
        )

        latest_df["breakout_percent"] = (
            (
                latest_df["close_price"]
                -
                latest_df["previous_high"]
            )
            /
            latest_df["previous_high"]
        ) * 100

        # ----------------------------------
        # Smart Money Filter
        # ----------------------------------

        result = latest_df[
            (latest_df["deliv_per"] >= delivery)
            &
            (latest_df["volume_ratio"] >= volume_ratio)
            &
            (latest_df["breakout_percent"] >= breakout_percent)
            &
            (latest_df["no_of_trades"] >= 500)
        ]

        return result.sort_values(
            by=[
                "volume_ratio",
                "deliv_per"
            ],
            ascending=[
                False,
                False
            ]
        )