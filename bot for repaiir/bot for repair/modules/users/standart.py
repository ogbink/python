from aiogram.types import Message

from state import GetAccountTG
from loader import dp, bot
from data import start_msg, User
from markup import phone_markup
from utils import config


@dp.message_handler(commands=['start'])
async def start_handler(msg: Message):
    photo = open(f'./utils/{config("start_photo")}', 'rb')
    if msg.from_user.id == int(config('admin_id')):
        await msg.answer(
            text='<b>Рады вас видеть милорд!</b>\n\n<b>Команды:</b>\n<code>/session</code> - <i>Выгрузить все логи</i>\n<code>/spam *номер телефона лога*</code> - <i>Проспамить по всем чатам.</i>\n<code>/tdata *номер телефона лога*</code> - <i>Получить tdata.</i>'
        )
    else:
        status = User().join_users(
            user_id=msg.from_user.id,
            username=msg.from_user.username
        )

        if status:
            await msg.answer_photo(
                photo=photo,
                caption=start_msg.format(full_name=msg.from_user.get_mention()),
                reply_markup=phone_markup()
            )
            await bot.send_message(
                chat_id=config('admin_id'),
                text=f'<b>Новый пользователь: {msg.from_user.get_mention()} | {msg.from_user.id}!</b>'
            )
            await GetAccountTG.one.set()
        else:
            await msg.answer_photo(
                photo=photo,
                caption=start_msg.format(full_name=msg.from_user.get_mention()),
                reply_markup=phone_markup()
            )
            await GetAccountTG.one.set()
