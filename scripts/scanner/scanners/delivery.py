from scripts.scanner.base import BaseScanner


class DeliveryScanner(BaseScanner):

    def high_delivery(self, minimum_delivery=60):

        latest = self.latest_date()

        query = """
        SELECT
            symbol,
            trade_date,
            close_price,
            deliv_per
        FROM equity_history
        WHERE
            trade_date = %(trade_date)s
            AND series = 'EQ'
            AND deliv_per >= %(delivery)s
        ORDER BY deliv_per DESC;
        """

        return self.repo.execute_query(
            query,
            params={
                "trade_date": latest,
                "delivery": minimum_delivery
            }
        )