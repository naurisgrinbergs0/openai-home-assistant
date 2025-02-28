from datetime import datetime


def get_current_time_settings():
    current_datetime = datetime.now()

    return {
        "date": current_datetime.strftime("%Y-%m-%d"),
        "time": current_datetime.strftime("%H:%M:%S"),
        "week_number": current_datetime.isocalendar().week,
        "weekday_number": current_datetime.weekday() + 1,
    }


def get_date():
    current_datetime = datetime.now()
    return str(current_datetime.date())


def is_today(date_string):
    return date_string == str(datetime.now().date())
