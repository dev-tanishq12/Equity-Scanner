from scripts.scanner.scanners.gap import GapScanner


def main():

    scanner = GapScanner()

    print("=" * 60)
    print("GAP UP SCANNER")
    print("=" * 60)

    gap_up = scanner.gap_up()

    print(
        gap_up[
            [
                "symbol",
                "trade_date",
                "open_price",
                "previous_high",
                "gap_percentage"
            ]
        ].head(20)
    )

    print()

    print(f"Gap Up Stocks : {len(gap_up)}")

    print()

    print("=" * 60)
    print("GAP DOWN SCANNER")
    print("=" * 60)

    gap_down = scanner.gap_down()

    print(
        gap_down[
            [
                "symbol",
                "trade_date",
                "open_price",
                "previous_low",
                "gap_percentage"
            ]
        ].head(20)
    )

    print()

    print(f"Gap Down Stocks : {len(gap_down)}")


if __name__ == "__main__":
    main()