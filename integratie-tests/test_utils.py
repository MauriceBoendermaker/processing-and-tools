from datetime import datetime
import time
import httpx


# handige functies voor bij het testen
def match_date(date_str, to_match):

    # format zonder tijdzone, met microseconden
    parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f").date()
    return parsed_date == to_match


def match_date_timezone(date_str, to_match):

    # format met timezone
    parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").date()
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


def check_code_exists(json, target_code):
    for item in json:
        if item["code"] == target_code:
            return True
    return False


def check_reference_exists(json, target_reference):
    for item in json:
        if item["item_reference"] == target_reference:
            return True
    return False
