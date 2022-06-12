from aiogram.dispatcher.filters.state import StatesGroup, State


class setting(StatesGroup):
    set_fio = State()
    set_telephone = State()
    set_adress = State()
    check_fio = State()
    check_telephone = State()
    check_adress = State()
    check_profile = State()
    edit_telephone = State()
    edit_fio = State()
    edit_adress = State()