# Finance Dashboard

This project is a Python-based financial asset dashboard that allows users to track and visualize their various financial assets.

## Features

- Store and manage different types of financial assets (stocks, bonds, cryptocurrencies, etc.)
- Fetch and update asset prices automatically
- Visualize asset allocation and performance
- Track net worth over time

## Project Structure

The main components of this project are:

- `main.py`: The main script containing database operations and price update functions
- `asset_prices.db`: SQLite database for storing asset and price data
- `requirements.txt`: List of dependencies
## Database Schema

The project uses a SQLite database with the following tables:

- `asset_types`: Stores different types of assets
- `assets`: Stores individual assets
- `price_history`: Stores historical price data for assets
- `data_sources`: Tracks different data sources for price information
- `last_updates`: Keeps track of when each asset was last updated

## Setup and Installation

1. Ensure you have Python 3.x installed, SQLite3 installed
1. Clone this repository
1. Install required packages:
   ```bash
   mkdir finance_dashboard
   cd finance_dashboard
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   sqlite3 numbers.db < numbers_schema.sql
   ```

## Usage

To initialize the database and start tracking assets:

1. Run the `create_database()` function to set up the database schema
1. Use the provided functions to add asset types, assets, and price data
1. Run the `update_stock_prices()` function periodically to fetch the latest price data

## Future Improvements

- Implement a web interface using Flask or FastAPI
- Add more data sources for different types of assets
- Create visualizations using libraries like Plotly or Matplotlib
- Implement user authentication for multi-user support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
