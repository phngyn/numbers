-- Asset types (e.g., stocks, bonds, cryptocurrencies)
CREATE TABLE asset_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Assets (e.g., AAPL, BTC, VTSAX)
CREATE TABLE assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_id INTEGER NOT NULL,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (type_id) REFERENCES asset_types(id)
);

-- Price data
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(18, 8) NOT NULL,
    high DECIMAL(18, 8) NOT NULL,
    low DECIMAL(18, 8) NOT NULL,
    close DECIMAL(18, 8) NOT NULL,
    volume BIGINT,
    adjusted_close DECIMAL(18, 8),
    FOREIGN KEY (asset_id) REFERENCES assets(id),
    UNIQUE (asset_id, date)
);

-- Data sources (e.g., Yahoo Finance, CoinGecko)
CREATE TABLE data_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    url VARCHAR(255)
);

-- Last update tracking
CREATE TABLE last_updates (
    asset_id INTEGER PRIMARY KEY,
    data_source_id INTEGER NOT NULL,
    last_updated TIMESTAMP NOT NULL,
    FOREIGN KEY (asset_id) REFERENCES assets(id),
    FOREIGN KEY (data_source_id) REFERENCES data_sources(id)
);

-- Transaction types (e.g., buy, sell, dividend)
CREATE TABLE transaction_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Financial transactions
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    transaction_type_id INTEGER NOT NULL,
    date TIMESTAMP NOT NULL,
    quantity DECIMAL(18, 8) NOT NULL,
    price DECIMAL(18, 8) NOT NULL,
    total_amount DECIMAL(18, 8) NOT NULL,
    fees DECIMAL(18, 8) DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (asset_id) REFERENCES assets(id),
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_types(id)
);


-- Indexes for performance
CREATE INDEX idx_price_history_asset_date ON price_history(asset_id, date);
CREATE INDEX idx_assets_symbol ON assets(symbol);
CREATE INDEX idx_transactions_asset_date ON transactions(asset_id, date);
CREATE INDEX idx_transactions_type ON transactions(transaction_type_id);
