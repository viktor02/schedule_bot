from datetime import date, timedelta
from LessonsLoader import LessonsLoader


def get_lessons_text(year, month, day) -> str:
    less = LessonsLoader()

    weekday = date(year, month, day).isoweekday()
    is_odd_week = True if date(year, month, day).isocalendar()[1] % 2 == 0 else False

    lessons = less.get_lessons(weekday, is_odd_week)
    time = less.get_time()

    text = ""
    for weekday, number, lesson, teacher, odd in lessons:
        time_s = time[number - 1][1]
        time_e = time[number - 1][2]
        text += f"{time_s} {time_e} | {lesson}\n"

    return text


def date_wrapper(day) -> str:
    nday = date(date.today().year, date.today().month, day)
    holiday = nday.isoweekday() > 5
    if holiday:
        return "Этот день выходной"

    lessons = nday.strftime("%b %d %Y") + "\n"
    lessons += get_lessons_text(nday.year, nday.month, nday.day)
    return lessons


def next_day_wrapper() -> str:
    next_day = date.today() + timedelta(days=1)
    return date_wrapper(next_day.day)
