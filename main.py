import logging
import asyncio
import aiogram
import os
from aiogram.utils.markdown import escape_md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dao import *
from dotenv import load_dotenv,find_dotenv



load_dotenv(find_dotenv())

logging.basicConfig(level=logging.INFO)

token = os.getenv('TOKEN')
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


u_admin = [8289679178]
click = 0


class Form_A(StatesGroup):
    wait_photos = State()
    wait_caption = State()
    
class Form_card(StatesGroup):
    wait_card = State()
    
class Form_request(StatesGroup):
    wait_amount = State()
    
class Form_delete(StatesGroup):
    wait_id = State()



main = DaoBases_main() 
requests = DaoBases_requests()
post = Databace_post()


click_text = "Клик " + "\U0001F4A5"
personal_account =  "Личный кабинет 🌇" 
about = "О боте 👜"
back = "Назад ⬅️"
kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder=100)
btn1 = aiogram.types.KeyboardButton(click_text)
btn2 = aiogram.types.KeyboardButton(personal_account)
btn3 = aiogram.types.KeyboardButton(about)
kb.add(btn1,btn2,btn3)

buttons = click_text , personal_account , about ,back


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id 
    counter = 0
    counter += 1
    balance = None
    balance = main.about_balance(user_id)
    if balance is None :
        balance = 0
        main.insert_balance(user_id,balance)
        await message.answer(f'Привет, {message.from_user.first_name},🧑‍💻Наша команда занимается поиском рекламодателей. Деньги, полученные с показов рекламы, равномерно распределяются между пользователями. Кликай и зарабатывай!! Твой баланс: {balance} ₽',reply_markup=kb)
    else:
        await message.answer(f'Привет, {message.from_user.first_name}! Твой баланс: {str(balance[0])} ₽.Давно вас не видели, рады, что вы снова с нами!🔵🟢🟡🟠🔴',reply_markup=kb)
    
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    user_id = message.from_user.id
    if user_id in u_admin:
        await message.reply("Ты попал в админ панель")
        kb_a = types.InlineKeyboardMarkup()
        btn_1 = types.InlineKeyboardButton(text='⛏Добавить пост⛏',callback_data='add' )
        btn_2 = types.InlineKeyboardButton(text='🔴Удалить🔴',callback_data='delete')
        kb_a.add(btn_1,btn_2)
        await bot.send_message(message.chat.id,"Выбери действие:\nПри загрузке изображения нажимать 'Сжать изображение'\n(Формат подписи:\n[Текст подписи](Ссылка))' ",reply_markup=kb_a)
    else:
        await message.answer("Ты не администратор")

@dp.message_handler(text = buttons)
async def echo(message: types.Message):
    if message.text == click_text:
        kb_rep = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(click_text,callback_data='click')
        btn_back = types.InlineKeyboardButton(back,callback_data='back')


        kb_rep.add(btn1,btn_back)
        await bot.send_message(message.chat.id, "💰:",reply_markup=ReplyKeyboardRemove())

        user_id = message.from_user.id
        balance= main.about_balance(user_id)
        main.update_balance(user_id)

        global click
        click += 1
        file_id = None
        caption = None
        if click % 3 == 0:
                file_id,caption = post.post_post(file_id,caption)
                if file_id[0] is not None: 
                    await bot.send_photo(message.chat.id,photo=file_id, caption=caption,parse_mode='Markdown')
                    await bot.send_message(message.chat.id,f'Следующий клик будет доступен через 1 секунду 🔥Ваш баланс на данный момент:  {str(balance[0])} ₽',reply_markup=kb_rep)
                    await bot.send_message(message.chat.id,f'Следующий клик будет доступен через 1 секунду 🔥Ваш баланс на данный момент:  {str(balance[0])} ₽',reply_markup=kb_rep)

        else:
           await bot.send_message(message.chat.id,f'Следующий клик будет доступен через 1 секунду 🔥Ваш баланс на данный момент:  {str(balance[0])} ₽',reply_markup=kb_rep)        
    elif message.text == personal_account:
        user_id = message.from_user.id

        kb_pr = types.InlineKeyboardMarkup(row_width=1)
        output = "Вывести на карту🧩"
        input = "Добавить номер карты 🧩"
        btn_out = types.InlineKeyboardButton(output,callback_data="output")
        btn_in = types.InlineKeyboardButton(input,callback_data="input")
        kb_pr.add(btn_out,btn_in)
        user_id = message.from_user.id
        result = main.select_card(user_id)
        balance = main.about_balance(user_id)
        if result[0] is not None:
            card_number = result[0]
            await bot.send_message(message.chat.id,f"📝Ваше имя: {message.from_user.first_name}!\n💸Ваш баланс {str(balance[0])}₽ \n 🆔 Ваш id:{message.from_user.id}\nВаша карта: {card_number}",reply_markup=kb_pr)
            date = requests.select_request(user_id)
            if date[0] is not None:
                await bot.send_message(message.chat.id,f"✅✅✅Ваша заявка на вывод создана {str(date[0])}✅✅✅✅",reply_markup=None)    
        else:
            await bot.send_message(message.chat.id,f"📝Ваше имя: {message.from_user.first_name}!\n💸Ваш баланс {str(balance[0])}₽ \n 🆔 Ваш id:{message.from_user.id}\nВаша карта:Не указана",reply_markup=kb_pr)
    elif message.text == about:
        await bot.send_message(message.chat.id,"📊 Статистика проекта:\n👨‍💻 Пользователей в боте: 48805\n🆘 Техническая поддержка - @test",reply_markup=kb)


@dp.callback_query_handler(lambda c : True)
async def callback(callback_query: types.CallbackQuery):
    if callback_query.data == 'click':
        kb_rep = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(click_text,callback_data='click')
        btn_back = types.InlineKeyboardButton(back,callback_data='back')
        kb_rep.add(btn1,btn_back)  
        user_id = callback_query.from_user.id
        balance= main.about_balance(user_id)
        main.update_balance(user_id)
        global click
        click += 1
        file_id = None
        caption = None
        if click % 3 == 0:
            file_id,caption = post.post_post(file_id,caption)
            await asyncio.sleep(1)
            if file_id is not None:
                await bot.send_photo(callback_query.message.chat.id,photo=file_id, caption=caption,parse_mode='Markdown')
                await bot.send_message(callback_query.message.chat.id,f'Следующий клик будет доступен через 1 секунду 🔥Ваш баланс на данный момент:  {str(balance[0])} ₽',reply_markup=kb_rep)
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
            else:
                await bot.send_message(callback_query.message.chat.id,f'Следующий клик будет доступен через 1 секунду 🔥Ваш баланс на данный момент:  {str(balance[0])} ₽',reply_markup=kb_rep)
                await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        else:
            await asyncio.sleep(2)
            await bot.send_message(callback_query.message.chat.id,f'Следующий клик будет доступен через 1 секунду 🔥Ваш баланс на данный момент:  {str(balance[0])} ₽',reply_markup=kb_rep)  
            await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id) 
    elif callback_query.data == 'back':
        user_id = callback_query.from_user.id
        balance = main.about_balance(user_id)
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await bot.send_message(callback_query.message.chat.id,f"💰💰💰Твой баланс {str(balance[0])} ₽💰💰💰",reply_markup=kb)
    elif callback_query.data == 'add':
        if callback_query.from_user.id not in u_admin:
            await callback_query.answer( "Вы не являетесь администратором!")
            return
        else:
            await callback_query.message.answer('Отправьте фотографию')
            await Form_A.wait_photos.set()
    elif callback_query.data == 'input':
        await bot.send_message(callback_query.message.chat.id,"💰Введите номер своей карты банковской карты: ")
        await Form_card.wait_card.set()
    elif callback_query.data == 'output':
        await bot.send_message(callback_query.message.chat.id, 'Сколько вы хотели бы вывести? \n💰: ')
        await Form_request.wait_amount.set()
    elif callback_query.data == 'delete':
        await bot.send_message(callback_query.message.chat.id, "Вывожу все посты:")
        await l_photos(callback_query.message.chat.id,post.list_post())
        await bot.send_message(callback_query.message.chat.id, "Какой пост вы хотели бы удалить?")
        await Form_delete.wait_id.set()
async def l_photos(chat_id,photos):
    for id,photo,caption in photos:
        await bot.send_message(chat_id,f'ID:{id}')
        await bot.send_photo(chat_id, photo, caption=caption,parse_mode='Markdown')
        

@dp.message_handler(content_types=types.ContentType.PHOTO, state=Form_A.wait_photos)
async def process_photo(message: types.Message, state: FSMContext):
    await state.update_data(file_id=message.photo[-1].file_id)
    await message.answer('Введите подпись для фотографии')
    await Form_A.wait_caption.set()

@dp.message_handler(state=Form_A.wait_caption)
async def process_caption(message: types.Message, state: FSMContext):
    data = await state.get_data()
    file_id = data.get('file_id')
    caption = message.text   
    post.add_post(file_id,caption)
    await bot.send_message(message.chat.id,'Фотография успешно добавлена в базу данных',reply_markup=kb)
    await state.finish()        
    
    
      
@dp.message_handler(content_types=types.ContentType.TEXT,state=Form_delete.wait_id)   
async def delete_posts(message: types.Message , state: FSMContext):
    id = message.text
    post.delete_post(id)
    await bot.send_message(message.chat.id,"Пост удалён из рекламы!",reply_markup=kb)
    await state.finish()

 
@dp.message_handler(content_types=types.ContentType.ANY,state=Form_request.wait_amount)
async def request(message: types.Message, state : FSMContext):
    amount = float(message.text)
    user_id = message.from_user.id
    balance = main.about_balance(user_id)
    if balance[0] >= amount:
        requests.create_request(user_id,amount)
        main.minus_balance(user_id,amount)
        await bot.send_message(message.chat.id,'⬅️🧳Заявка на вывод успешно создана',reply_markup=kb)
    else:
        await bot.send_message(message.chat.id, '⚒⚒⚒Вы не можете вывести сумму больше, чем вы заработали⚒⚒⚒',reply_markup=kb)
    await state.finish()  
   
   
        
@dp.message_handler(content_types=types.ContentType.TEXT, state=Form_card.wait_card)
async def card(message : types.Message, state : FSMContext):
    user_id = message.from_user.id
    card_number = message.text
    main.save_card(user_id,card_number)
    await bot.send_message(message.chat.id,"Номер карты успешно добавлен🔥 ",reply_markup=kb)
    await state.finish()
    
      

        
        
        
        

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
