from datetime import datetime
import time


def convert_time(unix_time):
    return datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')


def get_unix_timestamp():
    return int(time.time())


def convert_linebreaks_to_br(original_str):
    return original_str.replace("\n", "<br>")


def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M')