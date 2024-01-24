# fetch_covid_data.py
import requests

def fetch_covid_data():
    api_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            # Print the first 5 records for demonstration
            for record in data[:5]:
                print(record)
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_covid_data()
