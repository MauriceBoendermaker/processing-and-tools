from datetime import datetime


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
