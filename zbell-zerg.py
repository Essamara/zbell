import requests
import time
import playsound
import json

# Replace with your actual API endpoint
API_ENDPOINT = "https://zergpool.com/api/walletEx?address=WALLETGOESHERE"

# Path to the sound file you want to play
SOUND_FILE = "ohyeah.wav"

# Replace with the desired balance increase threshold
BALANCE_INCREASE_THRESHOLD = 1  # 1 coin

def extract_balance_from_api_response(api_response):
    """
    Extracts the "balance" value from the provided JSON string.

    Args:
        api_response: The JSON string representing the API response.

    Returns:
        The extracted "balance" value as a float, or None if not found.
    """

    try:
        data = json.loads(api_response)
        return float(data["total_unconfirmed"])
    except (json.JSONDecodeError, KeyError):
        print(f"Error parsing API response or 'balance' key not found.")
        return None

def extract_hashrate_from_api_response(api_response):
    """
    Extracts the "hashrate_solo" value from the provided JSON string.

    Args:
        api_response: The JSON string representing the API response.

    Returns:
        The extracted "hashrate_solo" value as a string, or None if not found.
    """

    try:
        data = json.loads(api_response)
        summary = data.get("summary", [])
        if summary:
            return summary[0].get("hashrate")
        else:
            print("Hashrate information not found in the API response.")
            return None
    except (json.JSONDecodeError, KeyError):
        print(f"Error parsing API response or 'hashrate_solo' key not found.")
        return None

def check_balance_increase():
    """
    Checks the current Dogecoin balance and compares it with the previous balance.
    Plays a sound if the balance has increased by more than the threshold.
    """
    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()  # Raise an exception for bad status codes
        current_balance = extract_balance_from_api_response(response.text)
        current_hashrate = extract_hashrate_from_api_response(response.text)

        if current_balance is not None:
            global previous_balance
            if 'previous_balance' not in globals():
                previous_balance = current_balance

            if current_balance - previous_balance > BALANCE_INCREASE_THRESHOLD:
                playsound.playsound(SOUND_FILE)
                print(f"Balance increased by {current_balance - previous_balance} Dogecoin!")

            previous_balance = current_balance

        if current_hashrate is not None:
            print(f"Current Hashrate: {current_hashrate}")

        # Print nested data
        if response.status_code == 200:
            data = json.loads(response.text)
            print("\n--- Nested Data ---")
            print(f"Total Confirmed: {data['total_confirmed']}")
            print(f"Total Unconfirmed: {data['total_unconfirmed']}")
            print(f"Balance: {data['balance']}")
            print(f"Unpaid: {data['unpaid']}")
            # Print hashrate for each miner
            miners = data.get("miners", [])
            for miner in miners:
                print(f"Miner Hashrate: {miner.get('hashrate', 'N/A')}") 
            # ... add more nested data as needed ...

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")

if __name__ == "__main__":
    while True:
        check_balance_increase()
        time.sleep(300)  # Check every 300 seconds (adjust as needed)