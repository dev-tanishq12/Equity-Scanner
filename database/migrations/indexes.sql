CREATE INDEX idx_symbol
ON equity_history(symbol);

CREATE INDEX idx_trade_date
ON equity_history(trade_date);

CREATE INDEX idx_symbol_date
ON equity_history(symbol, trade_date);

CREATE INDEX idx_series
ON equity_history(series);