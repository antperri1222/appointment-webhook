from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your Calendly Personal Access Token
CALENDLY_API_KEY = eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzUyNjM2OTE5LCJqdGkiOiI3MzYzYjY1My1iODY5LTQ5OGUtYjRmMC0zMzViNjQ0M2UzNjIiLCJ1c2VyX3V1aWQiOiJhMjc1NzNlYi04YmY5LTQ3YWUtYWQwOC1hMjBhOWJkZTdhZDQifQ.bAhfS_J9qyERXRvRhlMETw1fx9F3KSVs-uG8j4gw3MhlFEwCParpNMX4Z4Ftl1QOGf313SUh6M2WMW0pWJmgWQ 

@app.route("/book-appointment", methods=["POST"])
def book_appointment():
    data = request.json

    name = data.get("name")
    email = data.get("email")

    headers = {
        "Authorization": f"Bearer {CALENDLY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "max_event_count": 1,
        "owner": "https://api.calendly.com/users/me",
        "invitees": [
            {
                "email": email,
                "first_name": name
            }
        ]
    }

    calendly_response = requests.post(
        "https://api.calendly.com/scheduling_links",
        headers=headers,
        json=payload
    )

    if calendly_response.status_code == 201:
        booking_url = calendly_response.json()["resource"]["booking_url"]
        return jsonify({"booking_url": booking_url})
    else:
        return jsonify({"error": "Failed to create link", "details": calendly_response.json()}), 400

if __name__ == "__main__":
    app.run(debug=True)
