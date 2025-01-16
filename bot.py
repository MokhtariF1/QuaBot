from telethon import events, Button, TelegramClient, types
from sqlite3 import connect
import config
import helper


bot = TelegramClient("robot", config.api_id, config.api_hash, proxy=None if config.proxy is False else config.proxy_address)
print("connecting...")
bot.start(bot_token=config.bot_token)
print("connected!")
db = connect('bot.db')
cur = db.cursor()
bot_text = config.bot_text


@bot.on(events.NewMessage())
async def new_mssg(event):
    user_id = event.sender_id
    find_user = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()
    if find_user is None:
        async with bot.conversation(user_id, timeout=1000) as conv:
            await conv.send_message(bot_text["not_start"])
            btn = [
                Button.request_phone(bot_text["share_phone"], resize=True)
            ]
            await conv.send_message(bot_text["enter_phone"], buttons=btn)
            response = await conv.get_response()
            phone_number = None
            if type(response.media) == types.MessageMediaContact:
                phone_number = response.media.phone_number
                await conv.send_message(bot_text["saved"])
            else:
                await conv.send_message(bot_text["send_phone"])
                return
            await conv.send_message(bot_text["enter_name"])
            name = await conv.get_response()
            name = name.raw_text
            await conv.send_message(bot_text["saved"])
            await conv.send_message(bot_text["enter_city"].format(name=name))
            city = await conv.get_response()
            city = city.raw_text
            await conv.send_message(bot_text["saved"])
            cur.execute(f"INSERT INTO users VALUES ({user_id}, '{phone_number}', '{name}', '{city}')")
            db.commit()
            start_buttons = [
                Button.inline(bot_text["qua"], b'qua'),
                Button.inline(bot_text["zoo"], b'zoo')
            ]
            await conv.send_message(bot_text["start"].format(city=city, name=name), buttons=start_buttons)
    else:
        start_buttons = [
            Button.inline(bot_text["qua"], b'qua'),
            Button.inline(bot_text["zoo"], b'zoo')
        ]
        city, name = find_user[3], find_user[2]
        await event.reply(bot_text["start"].format(city=city, name=name), buttons=start_buttons)
@bot.on(events.CallbackQuery(data=b'qua'))
async def qua(event):
    user_id = event.sender_id
    async with bot.conversation(user_id, timeout=1000) as conv:
        dahe_keys = []
        for i in range(1320, 1401, 10):
            dahe_keys.append(Button.inline(str(i), str.encode(str(i))))
        r = await conv.send_message(bot_text["enter_dahe"], buttons=[dahe_keys[i:i+2] for i in range(0, len(dahe_keys), 2)])
        response = await conv.wait_event(events.CallbackQuery())
        dahe = int(response.data.decode())
        await bot.delete_messages(user_id, r.id)
        years = []
        r = None
        if dahe == 1400:
            years.append([Button.inline(str(1400), str.encode(str(1400))),Button.inline(str(1401), str.encode(str(1401))),Button.inline(str(1402), str.encode(str(1402))),Button.inline(str(1403), str.encode(str(1403)))])
            r = await conv.send_message(bot_text["enter_year"], buttons=years)
        else:
            for i in range(dahe, dahe + 10):
                years.append(Button.inline(str(i), str.encode(str(i))))
            r = await conv.send_message(bot_text["enter_year"], buttons=[years[i:i+2] for i in range(0, len(years), 2)])
        year = await conv.wait_event(events.CallbackQuery())
        year = int(year.data.decode())
        await bot.delete_messages(user_id, r.id)
        months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

        # ایجاد دکمه‌ها با نام ماه‌ها و دیتای ۱ تا ۱۲
        month_buttons = [Button.inline(month, str.encode(str(i+1))) for i, month in enumerate(months)]

        # چیدمان دکمه‌ها به صورت دو به دو
        buttons_layout = [month_buttons[i:i+2] for i in range(0, len(month_buttons), 2)]
        r = await conv.send_message(bot_text["enter_month"], buttons=buttons_layout)
        month = await conv.wait_event(events.CallbackQuery())
        month = int(month.data.decode())
        await bot.delete_messages(user_id, r.id)
        day_buttons = [Button.inline(str(day), str.encode(str(day))) for day in range(1, 31)]

        # چیدمان دکمه‌ها به صورت ۳ به ۳
        buttons_layout = [day_buttons[i:i+3] for i in range(0, len(day_buttons), 3)]
        r = await conv.send_message(bot_text["enter_day"], buttons=buttons_layout)
        day = await conv.wait_event(events.CallbackQuery())
        day = int(day.data.decode())
        await bot.delete_messages(user_id, r.id)
        gender_buttons = [
            [
                Button.inline(bot_text["male"], b'male')
            ],
            [
                Button.inline(bot_text["female"], b'female')
            ],
        ]
        await conv.send_message(bot_text["enter_gender"], buttons=gender_buttons)
        gender = await conv.wait_event(events.CallbackQuery())
        gender = gender.data.decode()
        birth = f"{year}/{month}/{day}"
        await event.reply(bot_text["information"].format(date=birth, gender=bot_text[gender]))
        qua = await helper.qua(year, month, day, gender)
        await conv.send_message(bot_text["qua_number"].format(num=qua), file=f"images/qua/{qua}.jpg")
        await conv.send_message(f"توضیحات عدد شانس {qua}", file=f"sounds/{qua}")
@bot.on(events.CallbackQuery(data=b'zoo'))
async def zoo(event):
    user_id = event.sender_id
    async with bot.conversation(user_id, timeout=1000) as conv:
        dahe_keys = []
        for i in range(1320, 1401, 10):
            dahe_keys.append(Button.inline(str(i), str.encode(str(i))))
        r = await conv.send_message(bot_text["enter_dahe"], buttons=[dahe_keys[i:i+2] for i in range(0, len(dahe_keys), 2)])
        response = await conv.wait_event(events.CallbackQuery())
        dahe = int(response.data.decode())
        await bot.delete_messages(user_id, r.id)
        years = []
        r = None
        if dahe == 1400:
            years.append([Button.inline(str(1400), str.encode(str(1400))),Button.inline(str(1401), str.encode(str(1401))),Button.inline(str(1402), str.encode(str(1402))),Button.inline(str(1403), str.encode(str(1403)))])
            r = await conv.send_message(bot_text["enter_year"], buttons=years)
        else:
            for i in range(dahe, dahe + 10):
                years.append(Button.inline(str(i), str.encode(str(i))))
            r = await conv.send_message(bot_text["enter_year"], buttons=[years[i:i+2] for i in range(0, len(years), 2)])
        year = await conv.wait_event(events.CallbackQuery())
        year = int(year.data.decode())
        await bot.delete_messages(user_id, r.id)
        months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

        # ایجاد دکمه‌ها با نام ماه‌ها و دیتای ۱ تا ۱۲
        month_buttons = [Button.inline(month, str.encode(str(i+1))) for i, month in enumerate(months)]

        # چیدمان دکمه‌ها به صورت دو به دو
        buttons_layout = [month_buttons[i:i+2] for i in range(0, len(month_buttons), 2)]
        r = await conv.send_message(bot_text["enter_month"], buttons=buttons_layout)
        month = await conv.wait_event(events.CallbackQuery())
        month = int(month.data.decode())
        await bot.delete_messages(user_id, r.id)
        day_buttons = [Button.inline(str(day), str.encode(str(day))) for day in range(1, 31)]

        # چیدمان دکمه‌ها به صورت ۳ به ۳
        buttons_layout = [day_buttons[i:i+3] for i in range(0, len(day_buttons), 3)]
        r = await conv.send_message(bot_text["enter_day"], buttons=buttons_layout)
        day = await conv.wait_event(events.CallbackQuery())
        day = int(day.data.decode())
        await bot.delete_messages(user_id, r.id)
        name, about, image = await helper.zoo(year, month, day)
        await conv.send_message(f"حیوان سال تولد شما {name} است!", file=image)        
        await conv.send_message(about)
bot.run_until_disconnected()
