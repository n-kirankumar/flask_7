import re
from log import log_message
from constants import VALID_GENDERS, VALID_BLOOD_GROUPS, LOG_MESSAGES
from data import data


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        log_message('error', f"{LOG_MESSAGES['invalid_email']}: {email}")
        raise ValueError(f"{LOG_MESSAGES['invalid_email']}: {email}")
    log_message('info', f"{LOG_MESSAGES['valid_email']}: {email}")
    return True


def validate_age(age):
    if not (0 < age < 120):
        log_message('error', f"{LOG_MESSAGES['invalid_age']}: {age}")
        raise ValueError(f"{LOG_MESSAGES['invalid_age']}: {age}")
    log_message('info', f"{LOG_MESSAGES['valid_age']}: {age}")
    return True


def validate_mobile(mobile):
    mobile_regex = r'^\d{10}$'
    if not re.match(mobile_regex, mobile):
        log_message('error', f"{LOG_MESSAGES['invalid_mobile']}: {mobile}")
        raise ValueError(f"{LOG_MESSAGES['invalid_mobile']}: {mobile}")
    log_message('info', f"{LOG_MESSAGES['valid_mobile']}: {mobile}")
    return True


def validate_gender(gender):
    if gender not in VALID_GENDERS:
        log_message('error', f"{LOG_MESSAGES['invalid_gender']}: {gender}")
        raise ValueError(f"{LOG_MESSAGES['invalid_gender']}: {gender}")
    log_message('info', f"{LOG_MESSAGES['valid_gender']}: {gender}")
    return True


def validate_blood_group(blood_group):
    if blood_group not in VALID_BLOOD_GROUPS:
        log_message('error', f"{LOG_MESSAGES['invalid_blood_group']}: {blood_group}")
        raise ValueError(f"{LOG_MESSAGES['invalid_blood_group']}: {blood_group}")
    log_message('info', f"{LOG_MESSAGES['valid_blood_group']}: {blood_group}")
    return True


def validate_user_data(func):
    def wrapper(*args, **kwargs):
        user_data = kwargs.get('user_data', {})
        email = user_data.get('email')
        age = user_data.get('age')
        mobile = user_data.get('mobile')
        gender = user_data.get('gender')
        blood_group = user_data.get('blood_group')

        if email:
            validate_email(email)
        if age:
            validate_age(age)
        if mobile:
            validate_mobile(mobile)
        if gender:
            validate_gender(gender)
        if blood_group:
            validate_blood_group(blood_group)

        return func(*args, **kwargs)

    return wrapper


@validate_user_data
def get_user_info(username, current_user, is_admin, user_data=None):
    if username not in data["records"]:
        log_message('error', f"{LOG_MESSAGES['user_not_found']}: {username}")
        raise ValueError(f"{LOG_MESSAGES['user_not_found']}: {username}")

    if not is_admin and current_user != username:
        log_message('error', f"{LOG_MESSAGES['unauthorized_access']}: {current_user} trying to access {username}")
        raise PermissionError(f"{LOG_MESSAGES['unauthorized_access']}: {current_user} trying to access {username}")

    user_info = data["records"][username]
    log_message('info', f"{LOG_MESSAGES['user_info']}: {username}, {user_info}")
    return user_info


@validate_user_data
def create_user_profile(username, user_data):
    if username in data["records"]:
        log_message('error', f"{LOG_MESSAGES['user_exists']}: {username}")
        raise ValueError(f"{LOG_MESSAGES['user_exists']}: {username}")

    data["records"][username] = user_data
    log_message('info', f"{LOG_MESSAGES['user_created']}: {username}, {user_data}")
    return user_data


@validate_user_data
def update_user_info(username, user_data, current_user, is_admin):
    if username not in data["records"]:
        log_message('error', f"{LOG_MESSAGES['user_not_found']}: {username}")
        raise ValueError(f"{LOG_MESSAGES['user_not_found']}: {username}")

    if not is_admin and current_user != username:
        log_message('error', f"{LOG_MESSAGES['unauthorized_update']}: {current_user} trying to update {username}")
        raise PermissionError(f"{LOG_MESSAGES['unauthorized_update']}: {current_user} trying to update {username}")

    data["records"][username].update(user_data)
    updated_info = data["records"][username]
    log_message('info', f"{LOG_MESSAGES['user_updated']}: {username}, {updated_info}")
    return updated_info


def list_all_users(current_user, is_admin):
    if not is_admin:
        log_message('error', f"{LOG_MESSAGES['unauthorized_list_users']}: {current_user}")
        raise PermissionError(f"{LOG_MESSAGES['unauthorized_list_users']}: {current_user}")

    log_message('info', f"{LOG_MESSAGES['list_all_users']}: {current_user}")
    return data["records"]
