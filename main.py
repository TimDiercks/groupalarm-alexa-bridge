import os
from flask import Flask, jsonify, request
import GroupAlarm as ga
import Voicemonkey as vm

GROUP_ALARM_TOKEN = os.getenv("GROUP_ALARM_TOKEN")
SERVICE_AUTH_TOKEN = os.getenv("SERVICE_AUTH_TOKEN")
VOICEMONKEY_TOKEN = os.getenv("VOICEMONKEY_TOKEN")
VOICEMONKEY_DEVICE_ID = os.getenv("VOICEMONKEY_DEVICE_ID")
REPEAT_ALARM_COUNT = int(os.getenv("REPEAT_ALARM_COUNT"))

if not GROUP_ALARM_TOKEN or \
    not SERVICE_AUTH_TOKEN or \
    not VOICEMONKEY_TOKEN or \
    not VOICEMONKEY_DEVICE_ID or \
    not REPEAT_ALARM_COUNT:
    raise ValueError("Some environment variables are not set correctly.")

app = Flask(__name__)
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

def verify_service_auth_token(token: str) -> bool: 
    # Compare the hashes to prevent timing attacks
    if hash(token) != hash(SERVICE_AUTH_TOKEN):
        raise ValueError("Invalid service auth token")

@app.route('/', methods=['POST'])
def trigger_alarm():
    try:
        json_data = request.get_json()
        if not json_data or 'service_auth_token' not in json_data:
            raise ValueError("No service auth token provided")
        
        verify_service_auth_token(json_data['service_auth_token'])

        response = ga.get_groupalarm_alarms(GROUP_ALARM_TOKEN)
        
        if not response:
            return jsonify({"status": "ok", "message": "No alarms to trigger"}), 200

        most_recent_alarm = ga.get_most_recent_alarm(response['alarms'])

        alarm_message = most_recent_alarm['message']

        vm.trigger_voicemonkey(alarm_message, REPEAT_ALARM_COUNT, VOICEMONKEY_TOKEN, VOICEMONKEY_DEVICE_ID)

    except ValueError as e:
        return jsonify({"error": "Unauthorized", "details": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "An error occured", "details": str(e)}), 400

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)