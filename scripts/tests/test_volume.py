from scripts.scanner.scanners.volume import VolumeScanner


def main():

    scanner = VolumeScanner()

    result = scanner.volume_breakout()

    print()

    print("=" * 60)

    print("VOLUME BREAKOUT")

    print("=" * 60)

    print()

    print(result[[
        "symbol",
        "trade_date",
        "ttl_trd_qnty",
        "avg_volume",
        "volume_ratio"
    ]].head(25))

    print()

    print("Stocks Found :", len(result))


if __name__ == "__main__":

    main()