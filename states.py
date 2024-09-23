from aiogram.fsm.state import StatesGroup, State


class AddingTask(StatesGroup):
    write_date = State()
    write_text = State()
    finish = State()


class DeleteState(StatesGroup):
    write_date = State()
    finish = State()


class WeatherState(StatesGroup):
    write_town = State()
    finish = State()
