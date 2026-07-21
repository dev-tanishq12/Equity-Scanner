from scripts.scanner.base import BaseScanner


class DeliveryScanner(BaseScanner):

    """
    Scanner for identifying stocks with
    high delivery percentage.
    """

    def high_delivery(self, minimum_delivery=60):

        latest = self.latest_date()

        return self.repo.get_high_delivery(
            trade_date=latest,
            minimum_delivery=minimum_delivery
        )