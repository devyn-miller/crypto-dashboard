# import time
# from typing import Dict, Any
from api_client import get_current_price, get_historical_data, get_global_stats, APIError
from price_alerts import PriceAlert
from visualization import plot_price_trend
from utils import format_price

class CryptoTracker:
    def __init__(self):
        self.price_alert = PriceAlert()
        self.running = True

    def display_menu(self):
        print("\nCryptocurrency Tracker Menu:")
        print("1. Get Current Price")
        print("2. View Price Trend")
        print("3. Show Global Stats")
        print("4. Manage Price Alerts")
        print("5. Compare Cryptocurrencies")
        print("6. Exit")

    def get_current_price_menu(self):
        symbol = input("Enter cryptocurrency symbol (e.g., BTC): ").strip().upper()
        price_data = get_current_price(symbol)
        if price_data and "USD" in price_data:
            print(f"\n{symbol}: {format_price(price_data['USD'])}")
        else:
            print(f"Unable to fetch price data for {symbol}")

    def view_price_trend_menu(self):
        symbol = input("Enter cryptocurrency symbol (e.g., BTC): ").strip().upper()
        try:
            days = int(input("Enter number of days for trend (1-30): "))
            if not 1 <= days <= 30:
                print("Please enter a number between 1 and 30")
                return
        except ValueError:
            print("Please enter a valid number")
            return

        historical_data = get_historical_data(symbol, days)
        if historical_data and historical_data.get("Response") == "Success":
            plot_price_trend(historical_data, symbol)
            print(f"\nPrice trend graph saved as {symbol}_trend.png")
        else:
            print(f"Unable to fetch historical data for {symbol}")

    def show_global_stats_menu(self):
        stats = get_global_stats()
        if stats and "Response" in stats:
            print("\nGlobal Cryptocurrency Statistics:")
            print("-" * 50)
            print(f"Total Market Cap: {format_price(stats['total_mcap'])}")
            print(f"Total Volume (24h): {format_price(stats['total_volume'])}")
            print(f"Active Cryptocurrencies: {stats['active_cryptocurrencies']:,}")
        else:
            print("Unable to fetch global statistics")

    def manage_alerts_menu(self):
        while True:
            print("\nAlert Management:")
            print("1. Set New Alert")
            print("2. View Current Alerts")
            print("3. Remove Alert")
            print("4. Back to Main Menu")

            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                symbol = input("Enter cryptocurrency symbol: ").strip().upper()
                try:
                    high = float(input("Enter high price threshold (USD): "))
                    low = float(input("Enter low price threshold (USD): "))
                    self.price_alert.set_alert(symbol, high, low)
                    print(f"\nAlert set for {symbol}")
                except ValueError:
                    print("Please enter valid numbers for thresholds")

            elif choice == "2":
                alerts = self.price_alert.get_alerts()
                if alerts:
                    print("\nCurrent Alerts:")
                    print("-" * 50)
                    for symbol, thresholds in alerts.items():
                        print(f"{symbol}:")
                        print(f"  High: {format_price(thresholds['high'])}")
                        print(f"  Low: {format_price(thresholds['low'])}")
                else:
                    print("No active alerts")

            elif choice == "3":
                symbol = input("Enter cryptocurrency symbol to remove alert: ").strip().upper()
                if self.price_alert.remove_alert(symbol):
                    print(f"Alert removed for {symbol}")
                else:
                    print(f"No alert found for {symbol}")

            elif choice == "4":
                break

    def compare_cryptos_menu(self):
        symbols = input("Enter cryptocurrency symbols separated by comma (e.g., BTC,ETH): ")
        symbols = [s.strip().upper() for s in symbols.split(",")]

        print("\nComparison Results:")
        print("-" * 70)
        print(f"{'Symbol':<10} | {'Price (USD)':<15} | {'24h Change':<10}")
        print("-" * 70)

        for symbol in symbols:
            price_data = get_current_price(symbol)
            if price_data and "USD" in price_data:
                print(f"{symbol:<10} | {format_price(price_data['USD']):<15}")
            else:
                print(f"{symbol:<10} | Error fetching data")

    def run(self):
        while self.running:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ").strip()

            try:
                if choice == "1":
                    self.get_current_price_menu()
                elif choice == "2":
                    self.view_price_trend_menu()
                elif choice == "3":
                    self.show_global_stats_menu()
                elif choice == "4":
                    self.manage_alerts_menu()
                elif choice == "5":
                    self.compare_cryptos_menu()
                elif choice == "6":
                    print("\nExiting Cryptocurrency Tracker...")
                    self.running = False
                else:
                    print("\nInvalid choice. Please try again.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    tracker = CryptoTracker()
    tracker.run()