from datetime import datetime


def convert_linebreaks_to_br(original_str):
    return original_str.replace("\n", "<br>")


def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M')