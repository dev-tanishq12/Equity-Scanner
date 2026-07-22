from scripts.scanner.base import BaseScanner


class VolumeScanner(BaseScanner):

    def volume_breakout(
        self,
        multiplier=2,
        window=20
    ):

        print("Loading historical market data...")

        df = self.get_market_data()

        # ----------------------------------
        # Calculate Average Volume
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

        latest_df = self.latest_dataframe(df)

        # ----------------------------------
        # Volume Ratio
        # ----------------------------------

        latest_df["volume_ratio"] = (

            latest_df["ttl_trd_qnty"]

            /

            latest_df["avg_volume"]

        )

        # ----------------------------------
        # Volume Breakout Filter
        # ----------------------------------

        result = latest_df[

            (latest_df["volume_ratio"] >= multiplier)

            &

            (latest_df["ttl_trd_qnty"] >= 100000)

            &

            (latest_df["no_of_trades"] >= 500)

        ]

        return result.sort_values(

            by=[
                "volume_ratio",
                "turnover_lacs"
            ],

            ascending=[
                False,
                False
            ]

        )