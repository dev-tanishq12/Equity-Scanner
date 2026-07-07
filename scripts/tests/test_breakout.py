from scripts.scanner.scanners.breakout import BreakoutScanner


def main():

    scanner = BreakoutScanner()

    result = scanner.price_breakout()

    print()

    print("=" * 60)
    print("PRICE BREAKOUT SCANNER")
    print("=" * 60)

    print()

    print(result[
        [
            "symbol",
            "trade_date",
            "close_price",
            "previous_high"
        ]
    ].head(30))

    print()

    print("Stocks Found :", len(result))


if __name__ == "__main__":
    main()