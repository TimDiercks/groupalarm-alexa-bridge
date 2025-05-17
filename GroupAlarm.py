from typing import TypedDict, List
import requests

class Alarm(TypedDict):
    message: str
    startDate: str

class GroupAlarmResponse(TypedDict):
    alarms: List[Alarm]

def get_groupalarm_alarms(access_token) -> List[GroupAlarmResponse]:
    response = requests.get(f"https://app.groupalarm.com/api/v1/alarms/alarmed",headers={
        "Personal-Access-Token": access_token,
    })
    if response.status_code != 200:
        raise Exception(f"Failed to fetch alarms: {response.status_code} - {response.text}")
    return response.json()

def get_most_recent_alarm(alarms: List[Alarm]) -> Alarm:
    if alarms is None or len(alarms) == 0:
        raise ValueError("No alarms found")
    alarms.sort(key=lambda x: x['startDate'], reverse=True)
    return alarms[0]

def get_modified_alarm_message(alarm_message: str, repeat: int) -> str:
    alarm_message = alarm_message.split("EM: ")[0]
    alarm_message = alarm_message.replace("EREIG:", "")
    alarm_message = alarm_message.replace("EO:", "")
    alarm_message = alarm_message.replace("\n", "<break time=\"500ms\"/>")
    return alarm_message * repeat