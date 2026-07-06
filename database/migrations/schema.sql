DROP TABLE IF EXISTS equity_history;

CREATE TABLE equity_history (

    symbol VARCHAR(30) NOT NULL,

    series VARCHAR(10) NOT NULL,

    trade_date DATE NOT NULL,

    prev_close NUMERIC(12,2),

    open_price NUMERIC(12,2),

    high_price NUMERIC(12,2),

    low_price NUMERIC(12,2),

    last_price NUMERIC(12,2),

    close_price NUMERIC(12,2),

    avg_price NUMERIC(12,2),

    ttl_trd_qnty BIGINT,

    turnover_lacs NUMERIC(18,2),

    no_of_trades INTEGER,

    deliv_qty BIGINT,

    deliv_per NUMERIC(6,2)

);