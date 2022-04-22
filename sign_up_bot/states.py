from aiogram.dispatcher.filters import state

class States(state.StatesGroup):
    set_subscription = state.State()
    