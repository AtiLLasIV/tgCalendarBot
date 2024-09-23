from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="📝 Добавить событие", callback_data="add_task")],
    [InlineKeyboardButton(text="⛅ Прогноз погоды", callback_data="weather")],
    [InlineKeyboardButton(text="⏳️ События сегодня", callback_data="today_tasks")],
    [InlineKeyboardButton(text="🕰️ Все события", callback_data="active_tasks")],
    [InlineKeyboardButton(text="❌️ Удалить событие", callback_data="delete_tasks")]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выйти в меню")]], resize_keyboard=True)
