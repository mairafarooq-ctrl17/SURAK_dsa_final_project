#!/usr/bin/env python3
# Copyright (c) 2026 Alen Rafagudinov
# All rights reserved.
"""
Stock Price Analyzer - Final Project
Algorithms and Data Structures Course
"""

import csv
from typing import List, Tuple, Optional


class StockData:
    """Class to hold stock price information"""
    def __init__(self, date: str, price: float):
        self.date = date
        self.price = price
    
    def __repr__(self):
        return f"{self.date}: ${self.price:.2f}"


def load_stock_data(filename: str) -> List[StockData]:
    """
    Load stock data from CSV file.
    This function is already implemented for you.
    """
    stock_list = []
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                stock_list.append(StockData(row['Date'], float(row['Price'])))
        print(f"✓ Successfully loaded {len(stock_list)} records from {filename}")
        return stock_list
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        return []
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


# ============================================================================
# TODO: IMPLEMENT THE FOLLOWING FUNCTIONS
# ============================================================================

def merge_sort_by_price(stocks: List[StockData]) -> List[StockData]:
    """
    TODO: Implement Merge Sort to sort stocks by price (ascending order)

    Args:
        stocks: List of StockData objects

    Returns:
        New sorted list of StockData objects

    Hint:
    - Use the merge sort algorithm covered in class
    - Compare stock.price values
    - Remember: merge sort divides the list and merges sorted halves
    """
    # Base case: list with 0 or 1 element is already sorted
    if len(stocks) <= 1:
        return stocks[:]

    # Divide: split the list into two halves
    mid = len(stocks) // 2
    left_half = stocks[:mid]
    right_half = stocks[mid:]

    # Conquer: recursively sort both halves
    sorted_left = merge_sort_by_price(left_half)
    sorted_right = merge_sort_by_price(right_half)

    # Merge: combine the sorted halves
    merged = []
    i = j = 0

    while i < len(sorted_left) and j < len(sorted_right):
        if sorted_left[i].price <= sorted_right[j].price:
            merged.append(sorted_left[i])
            i += 1
        else:
            merged.append(sorted_right[j])
            j += 1

    # Add remaining elements from left half
    while i < len(sorted_left):
        merged.append(sorted_left[i])
        i += 1

    # Add remaining elements from right half
    while j < len(sorted_right):
        merged.append(sorted_right[j])
        j += 1

    return merged


def binary_search_by_date(stocks: List[StockData], target_date: str) -> Optional[int]:
    """
    TODO: Implement Binary Search to find a stock entry by date

    Args:
        stocks: List of StockData objects (MUST be sorted by date)
        target_date: Date string to search for (format: YYYY-MM-DD)

    Returns:
        Index of the stock if found, None if not found

    Hint:
    - Assume the list is already sorted by date
    - Compare date strings lexicographically
    - Return the index where the date was found
    """
    left = 0
    right = len(stocks) - 1

    while left <= right:
        mid = (left + right) // 2

        if stocks[mid].date == target_date:
            return mid
        elif target_date < stocks[mid].date:
            right = mid - 1
        else:
            left = mid + 1

    return -1


def calculate_prefix_sum_prices(stocks: List[StockData]) -> List[float]:
    """
    TODO: Implement Prefix Sum to calculate cumulative prices

    Args:
        stocks: List of StockData objects

    Returns:
        List of cumulative sums

    Example:
        If prices are [10, 20, 30], return [10, 30, 60]

    Hint:
    - Create a new list to store cumulative sums
    - Each element is the sum of all previous prices plus current price
    """
    if not stocks:
        return []

    prefix_sums = []
    prefix_sums.append(stocks[0].price)

    for i in range(1, len(stocks)):
        prefix_sums.append(prefix_sums[i-1] + stocks[i].price)

    return prefix_sums


def calculate_moving_average(stocks: List[StockData], window_size: int) -> List[Tuple[str, float]]:
    """
    TODO: Calculate moving average using prefix sums

    Args:
        stocks: List of StockData objects
        window_size: Number of days for moving average

    Returns:
        List of tuples (date, moving_average) for each valid window

    Hint:
    - Use prefix sums to efficiently calculate averages
    - Average of window [i to j] = (prefix[j] - prefix[i-1]) / window_size
    - Only return averages where you have enough data points
    """
    if window_size < 1 or window_size > len(stocks):
        return []

    # Get prefix sums
    prefix = calculate_prefix_sum_prices(stocks)

    result = []

    # Calculate moving averages for valid windows
    for i in range(window_size - 1, len(stocks)):
        if i == window_size - 1:
            # First window: sum is just prefix[i]
            avg = prefix[i] / window_size
        else:
            # Subsequent windows: sum = prefix[i] - prefix[i-window_size]
            avg = (prefix[i] - prefix[i - window_size]) / window_size

        # Round to 2 decimal places and append tuple
        result.append((stocks[i].date, round(avg, 2)))

    return result


def kadane_max_profit(stocks: List[StockData]) -> Tuple[int, int, float]:
    """
    TODO: Use Kadane's Algorithm to find the best period to buy and sell

    Args:
        stocks: List of StockData objects

    Returns:
        Tuple of (buy_index, sell_index, max_profit)

    Hint:
    - Think of this as finding maximum subarray sum problem
    - Daily change = price[i] - price[i-1]
    - Find the contiguous period with maximum total change
    - Track where the maximum subarray starts and ends

    Example:
        Prices: [100, 95, 105, 110, 90]
        Changes: [-5, +10, +5, -20]
        Best period: buy at index 1 (95), sell at index 3 (110), profit = 15
    """
    if len(stocks) < 2:
        return (0, 0, 0.0)

    # Step 1: Convert prices to daily changes
    changes = []
    for i in range(1, len(stocks)):
        changes.append(stocks[i].price - stocks[i-1].price)

    # Step 2: Apply Kadane's algorithm to find maximum subarray
    max_so_far = changes[0]
    max_ending_here = changes[0]

    start = 0
    end = 0
    temp_start = 0

    for i in range(1, len(changes)):
        # If current sum is negative, start fresh from current element
        if max_ending_here < 0:
            max_ending_here = changes[i]
            temp_start = i
        else:
            max_ending_here += changes[i]

        # Update maximum if we found a better sum
        if max_ending_here > max_so_far:
            max_so_far = max_ending_here
            start = temp_start
            end = i

    # Step 3: Map back to original stock indices
    # Buy at the day before the changes subarray starts
    # changes[i] represents change from day i to day i+1
    # So if changes[start] is the first change, we buy at day start
    buy_index = start
    sell_index = end + 1
    max_profit = max_so_far

    return (buy_index, sell_index, round(max_profit, 2))


# ============================================================================
# DISPLAY FUNCTIONS (Already implemented for you)
# ============================================================================

def display_all_data(stocks: List[StockData]):
    """Display all stock data"""
    if not stocks:
        print("No data available.")
        return
    
    print("\n" + "="*50)
    print("ALL STOCK DATA")
    print("="*50)
    for i, stock in enumerate(stocks):
        print(f"{i+1:3}. {stock}")
    print("="*50)


def display_sorted_by_price(stocks: List[StockData]):
    """Display stocks sorted by price"""
    sorted_stocks = merge_sort_by_price(stocks)
    if sorted_stocks is None:
        print("⚠ Function not implemented yet!")
        return
    
    print("\n" + "="*50)
    print("STOCKS SORTED BY PRICE (Lowest to Highest)")
    print("="*50)
    for i, stock in enumerate(sorted_stocks):
        print(f"{i+1:3}. {stock}")
    print("="*50)


def search_by_date(stocks: List[StockData]):
    """Search for stock price by date"""
    date_input = input("Enter date to search (YYYY-MM-DD): ").strip()
    
    index = binary_search_by_date(stocks, date_input)
    if index is None:
        print(f"⚠ Date '{date_input}' not found or function not implemented yet!")
    elif index == -1:
        print(f"Date '{date_input}' not found in data.")
    else:
        print(f"\n✓ Found: {stocks[index]}")


def display_moving_averages(stocks: List[StockData]):
    """Display moving averages"""
    try:
        window = int(input("Enter window size for moving average (e.g., 5): ").strip())
        if window < 1:
            print("Window size must be at least 1")
            return
        
        moving_avgs = calculate_moving_average(stocks, window)
        if moving_avgs is None:
            print("⚠ Function not implemented yet!")
            return
        
        print("\n" + "="*50)
        print(f"{window}-DAY MOVING AVERAGE")
        print("="*50)
        for date, avg in moving_avgs:
            print(f"{date}: ${avg:.2f}")
        print("="*50)
    except ValueError:
        print("Please enter a valid number")


def display_best_profit_period(stocks: List[StockData]):
    """Display the best buy/sell period"""
    result = kadane_max_profit(stocks)
    if result is None:
        print("⚠ Function not implemented yet!")
        return
    
    buy_idx, sell_idx, profit = result
    
    print("\n" + "="*50)
    print("BEST PROFIT PERIOD (Using Kadane's Algorithm)")
    print("="*50)
    print(f"📉 Buy on:  {stocks[buy_idx].date} at ${stocks[buy_idx].price:.2f}")
    print(f"📈 Sell on: {stocks[sell_idx].date} at ${stocks[sell_idx].price:.2f}")
    print(f"💰 Profit:  ${profit:.2f}")
    print("="*50)


# ============================================================================
# MAIN MENU
# ============================================================================

def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("STOCK PRICE ANALYZER")
    print("="*50)
    print("1. View all stock data")
    print("2. View stocks sorted by price")
    print("3. Search for stock by date")
    print("4. Calculate moving average")
    print("5. Find best profit period")
    print("6. Exit")
    print("="*50)


def main():
    """Main program loop"""
    print("\n" + "🎯 "*20)
    print("WELCOME TO STOCK PRICE ANALYZER")
    print("🎯 "*20)
    
    # Load the data
    stocks = load_stock_data('stock_data.csv')
    
    if not stocks:
        print("Cannot proceed without data. Exiting.")
        return
    
    # Main loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            display_all_data(stocks)
        elif choice == '2':
            display_sorted_by_price(stocks)
        elif choice == '3':
            search_by_date(stocks)
        elif choice == '4':
            display_moving_averages(stocks)
        elif choice == '5':
            display_best_profit_period(stocks)
        elif choice == '6':
            print("\n👋 Thank you for using Stock Price Analyzer!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 6.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
