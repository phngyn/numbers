import sqlite3
import yfinance as yf
from datetime import datetime, timedelta


def add_asset_type(name):
    with sqlite3.connect('asset_prices.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO asset_types (name) VALUES (?)", (name,))
        return cursor.lastrowid

def add_asset(type_id, symbol, name):
    with sqlite3.connect('asset_prices.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO assets (type_id, symbol, name) VALUES (?, ?, ?)", 
                       (type_id, symbol, name))
        return cursor.lastrowid

def add_price_data(asset_id, date, open_price, high, low, close, volume, adjusted_close):
    with sqlite3.connect('asset_prices.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO price_history 
            (asset_id, date, open, high, low, close, volume, adjusted_close) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (asset_id, date, open_price, high, low, close, volume, adjusted_close))

def get_latest_price(symbol):
    with sqlite3.connect('asset_prices.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ph.close 
            FROM price_history ph
            JOIN assets a ON ph.asset_id = a.id
            WHERE a.symbol = ?
            ORDER BY ph.date DESC
            LIMIT 1
        """, (symbol,))
        result = cursor.fetchone()
        return result[0] if result else None

def get_price_history(symbol, start_date, end_date):
    with sqlite3.connect('asset_prices.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ph.date, ph.open, ph.high, ph.low, ph.close, ph.volume, ph.adjusted_close
            FROM price_history ph
            JOIN assets a ON ph.asset_id = a.id
            WHERE a.symbol = ? AND ph.date BETWEEN ? AND ?
            ORDER BY ph.date
        """, (symbol, start_date, end_date))
        return cursor.fetchall()


def update_stock_prices():
    with sqlite3.connect('asset_prices.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, symbol FROM assets WHERE type_id = (SELECT id FROM asset_types WHERE name = 'Stock')")
        stocks = cursor.fetchall()

    for stock_id, symbol in stocks:
        stock = yf.Ticker(symbol)
        history = stock.history(period="7d")  # Get last 7 days of data
        
        for date, row in history.iterrows():
            add_price_data(
                stock_id,
                date.date(),
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                row['Volume'],
                row['Close']  # Using 'Close' as 'Adjusted Close' for simplicity
            )

    # Update last_updates table
    with sqlite3.connect('asset_prices.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO last_updates (asset_id, data_source_id, last_updated)
            SELECT id, 
                   (SELECT id FROM data_sources WHERE name = 'Yahoo Finance'), 
                   ?
            FROM assets 
            WHERE type_id = (SELECT id FROM asset_types WHERE name = 'Stock')
        """, (datetime.now(),))

# Run this function daily
update_stock_prices()