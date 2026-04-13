#!/usr/bin/env python3
"""
Running Stats Visualization Script
Reads running data from CSV and displays various performance charts.
"""

import sys
import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def parse_duration(duration_str):
    """Parse duration string (HH:MM:SS) to total minutes."""
    if pd.isna(duration_str) or duration_str == '':
        return None
    
    try:
        parts = str(duration_str).split(':')
        if len(parts) == 3:
            hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
            return hours * 60 + minutes + seconds / 60
        elif len(parts) == 2:
            minutes, seconds = int(parts[0]), int(parts[1])
            return minutes + seconds / 60
        return None
    except (ValueError, AttributeError):
        return None


def load_and_process_data(csv_path):
    """Load and process the running stats CSV file."""
    # Read CSV - the file has some extra header rows at the end with summary data
    # We need to skip those
    df = pd.read_csv(csv_path)
    
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    # Filter out rows where Date doesn't look like a valid date
    # The summary rows have different structure
    df = df[df['Date'].astype(str).str.match(r'^\d+/\d+/\d+$', na=False)].copy()
    
    # Parse Date
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # Parse Duration to minutes
    df['Duration_Minutes'] = df['Duration'].apply(parse_duration)
    
    # Ensure Distance is numeric
    df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce')
    
    # Filter out rows with no valid distance or duration
    df = df[(df['Distance'] > 0) & (df['Duration_Minutes'].notna())].copy()
    
    # Calculate pace (minutes per mile)
    df['Pace'] = df['Duration_Minutes'] / df['Distance']
    
    # Add useful time components
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.to_period('M')
    df['Week'] = df['Date'].dt.to_period('W')
    
    return df


def plot_miles_per_month(ax, df):
    """Plot miles per month as bar chart."""
    monthly = df.groupby('Month')['Distance'].sum()
    
    # Convert period to timestamp for plotting
    x = monthly.index.to_timestamp()
    
    ax.bar(x, monthly.values, width=20, alpha=0.7, color='steelblue')
    ax.set_title('Miles per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Miles')
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def plot_miles_per_year(ax, df):
    """Plot miles per year as bar chart."""
    yearly = df.groupby('Year')['Distance'].sum()
    
    ax.bar(yearly.index, yearly.values, alpha=0.7, color='seagreen')
    ax.set_title('Miles per Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Miles')
    ax.set_xticks(yearly.index)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def plot_average_pace_over_time(ax, df):
    """Plot average pace over time as line chart."""
    monthly_pace = df.groupby('Month')['Pace'].mean()
    
    x = monthly_pace.index.to_timestamp()
    
    ax.plot(x, monthly_pace.values, marker='.', linewidth=1, color='coral')
    ax.set_title('Average Pace (min/mile) Over Time')
    ax.set_xlabel('Month')
    ax.set_ylabel('Minutes per Mile')
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def plot_run_frequency(ax, df):
    """Plot number of runs per month as bar chart."""
    monthly_runs = df.groupby('Month').size()
    
    x = monthly_runs.index.to_timestamp()
    
    ax.bar(x, monthly_runs.values, width=20, alpha=0.7, color='mediumpurple')
    ax.set_title('Run Frequency per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Runs')
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def plot_weekly_mileage_trend(ax, df):
    """Plot weekly mileage trend as line chart."""
    # Sort by date first
    df_sorted = df.sort_values('Date')
    
    # Calculate daily mileage
    daily = df_sorted.groupby('Date')['Distance'].sum()
    
    # Resample to weekly and calculate rolling average
    weekly = daily.resample('W').sum()
    
    # 4-week rolling average
    rolling = weekly.rolling(window=4, min_periods=1).mean()
    
    ax.plot(weekly.index, weekly.values, alpha=0.4, color='gray', label='Weekly')
    ax.plot(rolling.index, rolling.values, linewidth=2, color='darkorange', label='4-Week Avg')
    ax.set_title('Weekly Mileage Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel('Miles')
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')


def plot_distance_distribution(ax, df):
    """Plot distance distribution as histogram."""
    ax.hist(df['Distance'], bins=30, alpha=0.7, color='teal', edgecolor='black')
    ax.set_title('Distance Distribution')
    ax.set_xlabel('Miles')
    ax.set_ylabel('Frequency')
    ax.axvline(df['Distance'].mean(), color='red', linestyle='--', label=f'Mean: {df["Distance"].mean():.2f}')
    ax.legend()


def main():
    parser = argparse.ArgumentParser(description='Visualize running statistics')
    parser.add_argument(
        'csv_path',
        nargs='?',
        default='running-stats.csv',
        help='Path to running stats CSV file'
    )
    args = parser.parse_args()
    
    # Verify file exists
    if not Path(args.csv_path).exists():
        print(f"Error: File not found: {args.csv_path}")
        sys.exit(1)
    
    # Load and process data
    print(f"Loading data from {args.csv_path}...")
    df = load_and_process_data(args.csv_path)
    print(f"Loaded {len(df)} runs from {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
    
    # Create figure with 2x3 subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Running Statistics Dashboard', fontsize=16, fontweight='bold')
    
    # Plot all 6 charts
    plot_miles_per_month(axes[0, 0], df)
    plot_miles_per_year(axes[0, 1], df)
    plot_average_pace_over_time(axes[0, 2], df)
    plot_run_frequency(axes[1, 0], df)
    plot_weekly_mileage_trend(axes[1, 1], df)
    plot_distance_distribution(axes[1, 2], df)
    
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()