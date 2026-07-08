from scripts.scanner.base import BaseScanner


class GapScanner(BaseScanner):

    # --------------------------------------------------
    # Gap Up Scanner
    # --------------------------------------------------

    def gap_up(
        self,
        gap_percent=1.0,
        min_trades=500
    ):

        print("Loading historical market data...")

        df = self.get_market_data()

        # ----------------------------------
        # Previous Day High
        # ----------------------------------

        df["previous_high"] = (
            df.groupby("symbol")["high_price"]
            .shift(1)
        )

        latest = self.latest_date()

        latest_df = df[
            df["trade_date"] == latest
        ].copy()

        # ----------------------------------
        # Gap Percentage
        # ----------------------------------

        latest_df["gap_percentage"] = (
            (
                latest_df["open_price"]
                - latest_df["previous_high"]
            )
            / latest_df["previous_high"]
        ) * 100

        # ----------------------------------
        # Scanner
        # ----------------------------------

        result = latest_df[
            (latest_df["gap_percentage"] >= gap_percent)
            &
            (latest_df["no_of_trades"] >= min_trades)
        ]

        return result.sort_values(
            by=[
                "gap_percentage",
                "turnover_lacs"
            ],
            ascending=[
                False,
                False
            ]
        )

    # --------------------------------------------------
    # Gap Down Scanner
    # --------------------------------------------------

    def gap_down(
        self,
        gap_percent=1.0,
        min_trades=500
    ):

        print("Loading historical market data...")

        df = self.get_market_data()

        # ----------------------------------
        # Previous Day Low
        # ----------------------------------

        df["previous_low"] = (
            df.groupby("symbol")["low_price"]
            .shift(1)
        )

        latest = self.latest_date()

        latest_df = df[
            df["trade_date"] == latest
        ].copy()

        # ----------------------------------
        # Gap Percentage
        # ----------------------------------

        latest_df["gap_percentage"] = (
            (
                latest_df["open_price"]
                - latest_df["previous_low"]
            )
            / latest_df["previous_low"]
        ) * 100

        # ----------------------------------
        # Scanner
        # ----------------------------------

        result = latest_df[
            (latest_df["gap_percentage"] <= -gap_percent)
            &
            (latest_df["no_of_trades"] >= min_trades)
        ]

        return result.sort_values(
            by=[
                "gap_percentage",
                "turnover_lacs"
            ],
            ascending=[
                True,
                False
            ]
        )