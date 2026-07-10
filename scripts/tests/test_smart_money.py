from scripts.scanner.scanners.smart_money import SmartMoneyScanner


def main():

    scanner = SmartMoneyScanner()

    result = scanner.scan()

    print("=" * 60)
    print("SMART MONEY SCANNER")
    print("=" * 60)

    print()

    print(
        result[
            [
                "symbol",
                "trade_date",
                "close_price",
                "deliv_per",
                "volume_ratio",
                "breakout_percent"
            ]
        ].head(30)
    )

    print()

    print("Stocks Found :", len(result))


if __name__ == "__main__":
    main()