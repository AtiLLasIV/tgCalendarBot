from aiogram import F, Router, types

from aiogram.fsm.context import FSMContext
import states

from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from datetime import datetime

from saving_data import user_data, date_format, default_date_object, tz

import requests
from config import OPEN_WEATHER_TOKEN

import kb
import text


router = Router()

last_date_object = dict()


@router.message(Command("start"))
async def start_handler(msg: Message):
    user_data[msg.from_user.id] = dict()
    last_date_object[msg.from_user.id] = default_date_object
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(Command("menu"))
@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.callback_query(F.data == "menu")
# @router.message(states.DefaultState.active)
async def menu(msg: Message, state: FSMContext):
    await msg.answer(text.menu, reply_markup=kb.menu)


# @router.message(F.text == "add_task")
@router.callback_query(F.data == "add_task")
async def add_task(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.add_task, reply_markup=kb.exit_kb)
    # await state.set_state(states.DefaultState.finish)
    await state.set_state(states.AddingTask.write_date)


@router.message(states.AddingTask.write_date)
async def input_date(msg: Message, state: FSMContext):
    date_text = msg.text
    global last_date_object
    last_date_object[msg.from_user.id] = datetime.strptime(date_text, date_format)
    user_data[msg.from_user.id][last_date_object[msg.from_user.id]] = " "
    await state.set_state(states.AddingTask.write_text)

    await msg.answer(text.input_date, reply_markup=kb.exit_kb)


@router.message(states.AddingTask.write_text)
async def input_task(msg: Message, state: FSMContext):
    task_text = msg.text
    user_data[msg.from_user.id][last_date_object[msg.from_user.id]] = task_text
    await state.set_state(states.AddingTask.finish)
    await msg.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "active_tasks")
async def print_task(callback: types.CallbackQuery, state: FSMContext):
    text_message = text.all_events
    for key in user_data[callback.from_user.id]:
        text_message += ("<i>" + str(key.strftime(date_format))[:10] + " " + str(key.strftime(date_format))[11:] +
                         "</i>: <code>" + user_data[callback.from_user.id][key] + "</code>\n \n")
    if len(user_data[callback.from_user.id]) == 0:
        await callback.message.reply(text.no_events)
    else:
        await callback.message.answer(text_message)
    await callback.message.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "today_tasks")
async def print_today_task(callback: types.CallbackQuery, state: FSMContext):
    today_date = datetime.now(tz=tz)
    tmp_key = str(today_date)[:10]
    are_events_today = False
    text_message = text.events_today
    for key in user_data[callback.from_user.id]:
        if str(key)[:10] == tmp_key:
            are_events_today = True
            text_message += ("<i>" + str(key.strftime(date_format))[:10] + " " + str(key.strftime(date_format))[11:] +
                             "</i>: <code>" + user_data[callback.from_user.id][key] + "</code>\n \n")
    if not are_events_today:
        await callback.message.reply(text.no_events_today)
    else:
        await callback.message.answer(text_message)
    await callback.message.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "delete_tasks")
async def delete_task(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.start_delete, reply_markup=kb.exit_kb)
    await state.set_state(states.DeleteState.write_date)


@router.message(states.DeleteState.write_date)
async def date_delete(msg: Message, state: FSMContext):
    del_date = msg.text
    tmp_key = datetime.strptime(del_date, date_format)
    if tmp_key in user_data[msg.from_user.id].keys():
        await msg.answer(text.good_delete)
        user_data[msg.from_user.id].pop(tmp_key)
    else:
        await msg.reply(text.wrong_delete)
    await state.set_state(states.DeleteState.finish)
    await msg.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "weather")
async def ask_town(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text.weather_request, reply_markup=kb.exit_kb)
    await state.set_state(states.WeatherState.write_town)


@router.message(states.WeatherState.write_town)
async def forecast(msg: Message, state: FSMContext):
    emoji_dict = {
        "Clear": "Ясно☀️",
        "Clouds": "Облачно☁️",
        "Rain": "Дождь🌧️",
        "Drizzle": "Морось🌧️",
        "Thunderstorm": "Гроза⛈️",
        "Snow": "Снег🌨️",
        "Mist": "Туман🌫️"
    }
    try:
        city = msg.text
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPEN_WEATHER_TOKEN}&units=metric")
        all_dates = r.json()
        list_dates = all_dates["list"]
        full_forecast = text.forecast_title
        full_forecast += f"🏙️<b>Город</b>: <b>{city}</b> \n \n"
        for iter in range(len(list_dates)):
            if iter % 3 != 0:
                continue
            temp = all_dates["list"][iter]["main"]["temp"]
            weather_description = all_dates["list"][iter]["weather"][0]["main"]
            if weather_description in emoji_dict:
                wd = emoji_dict[weather_description]
            else:
                wd = "<error>"
            humidity = list_dates[iter]["main"]["humidity"]
            wind = list_dates[iter]["wind"]["speed"]
            date = list_dates[iter]["dt_txt"]
            full_forecast += (f"<b> {date} </b> \nТемпература: <code>{temp}C°</code> \nОсадки: "
                              f"<code>{wd}</code> \nВлажность: "
                              f"<code>{humidity}%</code>\nСкорость ветра: <code>{wind} м/с</code>\n \n")

        await msg.answer(full_forecast)
        await state.set_state(states.WeatherState.finish)
        await msg.answer(text.menu, reply_markup=kb.menu)
    except:
        await msg.reply("Город не найден 😢")
