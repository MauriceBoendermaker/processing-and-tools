from datetime import datetime
import time
import httpx


# handige functies voor bij het testen
def match_date(date_str, to_match):

    # huidige format waarin de API datums aanmaakt
    parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    parsed_date = parsed_date.date()

    return parsed_date == to_match


def check_id_exists(json, target_id):
    for item in json:
        if item["id"] == target_id:
            return True
    return False


def check_uid_exists(json, target_uid):
    for item in json:
        if item["uid"] == target_uid:
            return True
    return False


def get_response_time(url):
    start = time.time()
    response = httpx.get(url, headers={"API_KEY": "a1b2c3d4e5"})
    eind = time.time()
    print(response)
    # response tijd naar milliseconde
    return (eind - start) * 1000
