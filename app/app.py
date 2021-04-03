from pyrogram import Client, filters
from datetime import date
import wrapper

app = Client(session_name="rschedule", config_file="../config.ini")


@app.on_message(filters.text & filters.private)
def send_lessons(client, message):
    today = date(2021, 3, 4)

    holiday = today.isoweekday() > 5
    if holiday:
        return message.reply_text("Сегодня пар нет")

    lessons = wrapper.get_lessons_text(today.year, today.month, today.day)
    message.reply_text(lessons)


app.run()
