import requests
import time
import playsound
import json

# Replace with your actual API endpoint
API_ENDPOINT = "https://zpool.com/api/walletEx?address=WALLETGOESHERE"

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
        return float(data["unpaid"])
    except (json.JSONDecodeError, KeyError):
        print(f"Error parsing API response or 'balance' key not found.")
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
            
        # Print nested data
        if response.status_code == 200:
            data = json.loads(response.text)
            print("\n--- Nested Data ---")
            print(f"Balance: {data['balance']}")
            print(f"Unpaid: {data['unpaid']}")
            print(f"Total: {data['Total']}")
            # Print hashrate for each miner
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")

if __name__ == "__main__":
    while True:
        check_balance_increase()
        time.sleep(300)  # Check every 300 seconds (adjust as needed)