from scripts.scanner.scanners.delivery import DeliveryScanner
from scripts.scanner.scanners.volume import VolumeScanner
from scripts.scanner.scanners.breakout import BreakoutScanner
from scripts.scanner.scanners.gap import GapScanner
from scripts.scanner.scanners.high52week import High52WeekScanner
from scripts.scanner.scanners.smart_money import SmartMoneyScanner


def print_menu():

    print()
    print("=" * 60)
    print("        EQUITY SCANNER")
    print("=" * 60)
    print("1. High Delivery Scanner")
    print("2. Volume Breakout Scanner")
    print("3. Price Breakout Scanner")
    print("4. Gap Scanner")
    print("5. 52 Week High Scanner")
    print("6. Smart Money Scanner")
    print("7. Run All Scanners")
    print("0. Exit")
    print("=" * 60)


def run_delivery():

    scanner = DeliveryScanner()

    result = scanner.high_delivery()

    print()
    print(result.head(20))

    print(f"\nStocks Found : {len(result)}")


def run_volume():

    scanner = VolumeScanner()

    result = scanner.volume_breakout()

    print()
    print(result[
        [
            "symbol",
            "trade_date",
            "ttl_trd_qnty",
            "volume_ratio"
        ]
    ].head(20))

    print(f"\nStocks Found : {len(result)}")


def run_breakout():

    scanner = BreakoutScanner()

    result = scanner.price_breakout()

    print()
    print(result[
        [
            "symbol",
            "trade_date",
            "close_price",
            "previous_high"
        ]
    ].head(20))

    print(f"\nStocks Found : {len(result)}")


def run_gap():

    scanner = GapScanner()

    print()

    print("-" * 60)
    print("GAP UP")
    print("-" * 60)

    gap_up = scanner.gap_up()

    print(gap_up[
        [
            "symbol",
            "trade_date",
            "gap_percentage"
        ]
    ].head(10))

    print(f"\nGap Up Stocks : {len(gap_up)}")

    print()

    print("-" * 60)
    print("GAP DOWN")
    print("-" * 60)

    gap_down = scanner.gap_down()

    print(gap_down[
        [
            "symbol",
            "trade_date",
            "gap_percentage"
        ]
    ].head(10))

    print(f"\nGap Down Stocks : {len(gap_down)}")


def run_52week():

    scanner = High52WeekScanner()

    result = scanner.fifty_two_week_high()

    print()

    print(result[
        [
            "symbol",
            "trade_date",
            "close_price",
            "breakout_percentage"
        ]
    ].head(20))

    print(f"\nStocks Found : {len(result)}")


def run_smart_money():

    scanner = SmartMoneyScanner()

    result = scanner.scan()

    print()

    print(result[
        [
            "symbol",
            "trade_date",
            "close_price",
            "deliv_per",
            "volume_ratio",
            "breakout_percent"
        ]
    ].head(20))

    print(f"\nStocks Found : {len(result)}")


def run_all():

    print("\nRunning Delivery Scanner...")
    run_delivery()

    print("\nRunning Volume Scanner...")
    run_volume()

    print("\nRunning Price Breakout Scanner...")
    run_breakout()

    print("\nRunning Gap Scanner...")
    run_gap()

    print("\nRunning 52 Week High Scanner...")
    run_52week()

    print("\nRunning Smart Money Scanner...")
    run_smart_money()


def main():

    while True:

        print_menu()

        choice = input("Enter Choice : ")

        if choice == "1":
            run_delivery()

        elif choice == "2":
            run_volume()

        elif choice == "3":
            run_breakout()

        elif choice == "4":
            run_gap()

        elif choice == "5":
            run_52week()

        elif choice == "6":
            run_smart_money()

        elif choice == "7":
            run_all()

        elif choice == "0":

            print("\nThank You for using Equity Scanner.")

            break

        else:

            print("\nInvalid Choice")


if __name__ == "__main__":
    main()