from scripts.scanner.repository import EquityRepository


def main():

    repo = EquityRepository()

    print("\nLatest Trading Day")
    print(repo.get_latest_date())

    print("\nTotal Symbols")
    print(len(repo.get_symbols()))

    print("\nRELIANCE History")
    print(repo.get_symbol_history("RELIANCE").head())


if __name__ == "__main__":
    main()