import logging


from bd import get_dict_blocks, get_blocks_list, get_blocks_list1, get_rus_name_and_id, get_eng_words, set_user, set_user_block, get_done_blocks
import config


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import BOT_TOKEN

from messages import MESSAGES, get_block_message_start
import keyboard as kb

logging.basicConfig(format=u'%(filename)+13s [LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s]%(message)s', level=logging.DEBUG)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())
GROUP_ID = -448197357
block_list = get_blocks_list()
block_list1 = get_blocks_list1()
# eng_words = []
count = 0
check = -1
async def update_text_blocks(message: types.Message,
dict):
    await message.edit_text(MESSAGES['blocks_message'],
reply_markup=kb.getMarkup(dict))
async def update_text_menu(message: types.Message):
    await message.edit_text(MESSAGES['enter'],
reply_markup=kb.inline_kb_menu)
async def update_text_blocks_start(message: types.Message, word_count, rus_name, block):
    await message.edit_text(get_block_message_start(word_count, rus_name), reply_markup=kb.getStartBlockMarkup(block))

async def update_text_words(message: types.Message):
    await  message.edit_text("Cɥɨɜɨ: " + config.eng_words[count] + ".\n Выберите перевод", reply_markup=kb.getRusWordsMarkup(config.eng_words[count]))

async def update_text_final_words(message: types.Message):
    await message.edit_text ("Поздравляю! Вы прошли все слова из этого блока.", reply_markup=kb.inline_kb_menu)

async def update_text_settings(message: types.Message):
 await message.edit_text("Настройка", reply_markup=kb.getSettingsMarkup())

async def update_text_done_blocks(message: types.Message, blocks):
    result = "Вы прошли блоки: "
    for s in blocks:
        result = result + s + ", "
    result = result[:len(result) - 2]
    await message.edit_text(result, reply_markup=kb.getMenuOnlyMarkup())


@dp.callback_query_handler(lambda c: c.data == 'choose_block')
async def process_callback_choose_block(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
    await update_text_blocks(callback_query.message, get_dict_blocks())
    print(callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == 'menu')
async def process_callback_menu(callback_query: types.CallbackQuery):
    await update_text_menu(callback_query.message)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data in block_list)
async def process_callback_blocks(callback_query: types.CallbackQuery):
    print(callback_query.data)
    word_count, rus_name = get_rus_name_and_id(callback_query.data)
    await update_text_blocks_start(callback_query.message, word_count, rus_name, callback_query.data)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data in block_list1)
async def process_callback_start_block(callback_query: types.CallbackQuery):
    global count
    count = 0
    config.eng_words = get_eng_words(callback_query.data)
    print(config.eng_words)
    await update_text_words(callback_query.message)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == "0" or c.data == "1" or c.data == "2" or c.data == "3" or c.data == "10")
async def process_callback_check(callback_query: types.CallbackQuery):
    global count
    count = count + 1
    if count == len(config.eng_words):
        await update_text_final_words(callback_query.message)
        set_user_block(callback_query.from_user.id)
    elif callback_query.data == "10":
        await update_text_words(callback_query.message)
    else:
        await update_text_blocks(callback_query.message, get_dict_blocks())
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == "settings")
async def process_callback_settings(callback_query: types.CallbackQuery):
    await update_text_settings(callback_query.message)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == "done")
async def process_callback_done(callback_query: types.CallbackQuery):
    done_blocks = get_done_blocks(callback_query.from_user.id)
    await update_text_done_blocks(callback_query.message, done_blocks)
    await bot.answer_callback_query(callback_query.id)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    set_user(message.from_user.id)
    await message.reply(MESSAGES['start'],
reply_markup=kb.inline_kb_menu, reply=False)

@dp.message_handler(commands=[MESSAGES['test_message']])
async def help_message(message: types.Message):
    await message.reply(MESSAGES['enter'])
if __name__ == '__main__':
    executor.start_polling(dp)