from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram import Client, filters
from pyrogram.errors import MessageEmpty, PeerIdInvalid

import wrapper
from Users import Users

app = Client(session_name="rschedule", config_file="../config.ini")


@app.on_message(filters.command("start"))
def send_start(_, message):
    start_text = "Привет! Этот бот отправляет тебе расписание перед парами!\n" \
                 "Так же можешь почитать `/help`"
    message.reply_text(start_text)

    u = Users()
    if u.check_user(message.chat.id) is False:
        u.reg_user(message.chat.username, message.chat.id, "user")


@app.on_message(filters.command("announce"))
def send_announce(_, message):
    u = Users()
    users = u.get_users()
    admins = u.get_admins()
    if message.chat.id not in admins:
        try:
            app.send_message(message.chat.id, "У вас нет прав")
        except PeerIdInvalid:
            pass
    else:
        for id, username, _ in users:
            app.send_message(id, message.command[1])


@app.on_message(filters.command("help"))
def send_help(_, message):
    help_text = "Чтобы пользоваться ботом, можешь просто отправить ему любой текст - " \
                "он скажет тебе расписание на сегодняшний день." \
                "\n\n" \
                "Команды:\n" \
                "`/help` - помощь\n" \
                "`/next` - отправить расписание на следующий день.\n" \
                "`/date <число>` - отправить расписание на это число"
    message.reply_text(help_text)


@app.on_message(filters.command("date"))
def send_date(_, message):
    day = int(message.command[1])
    
    lessons = wrapper.date_wrapper(day)

    try:
        message.reply_text(lessons)
    except MessageEmpty:
        message.reply_text("Нет аргументов.")


@app.on_message(filters.command("next"))
def next_day_lessons(_, message):
    lessons = wrapper.next_day_wrapper()
    message.reply_text(lessons)


@app.on_message(filters.text & filters.private)
def send_lessons(client, message):
    today = date.today()
    
    lessons = wrapper.date_wrapper(today.day)
    
    message.reply_text(lessons)


def send_every_day():
    lessons = wrapper.next_day_wrapper()

    u = Users()
    users = u.get_users()
    for id, _, _ in users:
        try:
            app.send_message(id, lessons)
        except PeerIdInvalid:
            pass


scheduler = BackgroundScheduler()
scheduler.add_job(send_every_day, "cron", day_of_week='mon-fri', hour=8, minute=30)
scheduler.start()

app.run()
