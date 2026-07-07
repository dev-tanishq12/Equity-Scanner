from scripts.scanner.scanners.delivery import DeliveryScanner


def main():

    scanner = DeliveryScanner()

    result = scanner.high_delivery(60)

    print("=" * 60)
    print("HIGH DELIVERY SCANNER")
    print("=" * 60)

    print(f"Stocks Found: {len(result)}")
    print()

    print(result.head(20))


if __name__ == "__main__":
    main()