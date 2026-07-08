from scripts.scanner.scanners.high52week import High52WeekScanner


def main():

    scanner = High52WeekScanner()

    result = scanner.fifty_two_week_high()

    print("=" * 60)
    print("52 WEEK HIGH SCANNER")
    print("=" * 60)

    print(
        result[
            [
                "symbol",
                "trade_date",
                "close_price",
                "previous_52w_high",
                "breakout_percentage"
            ]
        ].head(20)
    )

    print()

    print(f"Stocks Found : {len(result)}")


if __name__ == "__main__":
    main()