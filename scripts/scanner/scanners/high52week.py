from scripts.scanner.base import BaseScanner


class High52WeekScanner(BaseScanner):

    def fifty_two_week_high(
        self,
        window=252
    ):

        print("Loading historical market data...")

        df = self.get_market_data()

        # ----------------------------------
        # Previous 52-Week High
        # ----------------------------------

        df["previous_52w_high"] = (

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

        latest_df = self.latest_dataframe(df)

        # ----------------------------------
        # Breakout Percentage
        # ----------------------------------

        latest_df["breakout_percentage"] = (

            (

                latest_df["close_price"]

                -

                latest_df["previous_52w_high"]

            )

            /

            latest_df["previous_52w_high"]

        ) * 100

        # ----------------------------------
        # 52-Week High Scanner
        # ----------------------------------

        result = latest_df[

            latest_df["close_price"]

            >=

            latest_df["previous_52w_high"]

        ]

        return result.sort_values(

            by=[
                "breakout_percentage",
                "turnover_lacs"
            ],

            ascending=[
                False,
                False
            ]

        )