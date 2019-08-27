from datetime import datetime
import bcrypt


def convert_linebreaks_to_br(original_str):
    return original_str.replace("\n", "<br>")


def get_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M')


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def validate_password(password1, password2):
    if password1 == password2:
        return True
    return False