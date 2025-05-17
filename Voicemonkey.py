import GroupAlarm as ga
import requests

def trigger_voicemonkey(alarm_message: str, repeat_alarm_count: int, token: str, device: str) -> None:
    alarm_message = ga.get_modified_alarm_message(alarm_message, repeat_alarm_count)
    response = requests.get(
        "https://api-v2.voicemonkey.io/announcement?" \
        f"token={token}" \
        f"&device={device}" \
        f"&text={alarm_message}"\
        "&language=de-DE")
    if response.status_code != 200:
        raise Exception(f"Failed to trigger Voicemonkey: {response.status_code} - {response.text}")