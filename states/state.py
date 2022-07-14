from aiogram.dispatcher.filters.state import StatesGroup, State


class Setting(StatesGroup):
    set_fio = State()
    set_telephone = State()
    check_fio = State()
    check_telephone = State()
    go_site = State()
    set_comment_yourself = State()
    set_comment_courier = State()
    choice_method = State()
    payment = State()
    set_street = State()
    set_house = State()
    set_flat = State()
    check_address = State()
    edit_street = State()
    edit_house = State()
    edit_flat = State()
