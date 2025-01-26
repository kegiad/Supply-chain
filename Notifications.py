from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()
slack_token = os.getenv("SLACK_TOKEN")  # Replace with your Slack bot token
channel_id = os.getenv("CHANNEL_ID")   # Replace with your channel ID
def send_slack_notification(message):

    client = WebClient(token=slack_token)

    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
        print("Message sent to Slack:", response)
    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")

# Example usage
#send_slack_notification("IMD has predicted heavy rainfall in the upcoming days, this might impact pepper supply.")


def delete_last_n_messages(CHANNEL_ID):
    headers = {"Authorization": f"Bearer {slack_token}"}
    n = 1
    # Fetch the last 50 messages
    response = requests.get(
        "https://slack.com/api/conversations.history",
        headers=headers,
        params={"channel": CHANNEL_ID, "limit": n}  # Limit to the last 50 messages
    )

    if not response.json().get("ok"):  # Check if fetching messages succeeded
        print(f"Failed to fetch messages: {response.json()}")
        return

    # Parse the response
    messages = response.json().get("messages", [])
    if not messages:
        print("No messages found to delete.")
        return

    # Delete each message
    for message in messages:
        ts = message["ts"]  # Timestamp of the message
        delete_response = requests.post(
            "https://slack.com/api/chat.delete",
            headers=headers,
            json={"channel": CHANNEL_ID, "ts": ts}  # Use `json` to send the payload
        )
        if delete_response.status_code == 200 and delete_response.json().get("ok"):
            print(f"Deleted message with timestamp {ts}")
            time.sleep(1)  # Add delay to avoid rate limits
        else:
            print(f"Failed to delete message with timestamp {ts}: {delete_response.json()}")

