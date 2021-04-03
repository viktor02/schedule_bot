from datetime import date
from LessonsLoader import LessonsLoader


def get_lessons_text(year, month, day):
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
