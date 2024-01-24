# store_covid_data.py
import sqlite3
import requests
import csv
from io import StringIO

def create_covid_table(conn):
    # Create a table to store COVID-19 data
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS covid_data (
            date TEXT PRIMARY KEY,
            cases INTEGER,
            deaths INTEGER,
            recovered INTEGER
        )
    ''')
    conn.commit()

def fetch_covid_data():
    # Define the API endpoint (New York Times COVID-19 data)
    api_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"

    try:
        # Make a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def store_covid_data(conn, data):
    # Parse the CSV data
    csv_reader = csv.DictReader(StringIO(data))
    
    # Insert data into the SQLite database
    cursor = conn.cursor()
    for row in csv_reader:
        cursor.execute('''
            INSERT OR IGNORE INTO covid_data (date, cases, deaths, recovered)
            VALUES (?, ?, ?, ?)
        ''', (row['date'], row['cases'], row['deaths'], row['recovered']))

    conn.commit()

def main():
    # Connect to the SQLite database (creates the database file if not exists)
    conn = sqlite3.connect('covid_database.db')

    # Create the COVID-19 data table
    create_covid_table(conn)

    # Fetch COVID-19 data
    data = fetch_covid_data()

    if data:
        # Store COVID-19 data in the SQLite database
        store_covid_data(conn, data)
        print("Data stored successfully!")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
