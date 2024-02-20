import random
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from messages import MESSAGES
from bd import get_rus_right_words, get_other_rus_words

inline_btn_choose_block = InlineKeyboardButton('Выбор блока', callback_data='choose_block')
inline_btn_settings = InlineKeyboardButton('Настройки', callback_data='settings')
inline_btn_menu = InlineKeyboardButton('Главное меню', callback_data='menu')
inline_kb_menu = InlineKeyboardMarkup().add(inline_btn_choose_block, inline_btn_settings)

def getMarkup(blockDict):
    print(blockDict)
    markup = InlineKeyboardMarkup()
    for key, value in blockDict.items():
        markup.add(InlineKeyboardButton(value, callback_data=key))
    markup.add(inline_btn_menu)
    return markup

def getStartBlockMarkup(block):
    markup = InlineKeyboardMarkup()
    block = block + '1'
    print(block)
    text = "Начать"
    markup.add(InlineKeyboardButton(text, callback_data=block), inline_btn_menu)
    return markup

def getRusWordsMarkup(word):
    right_words = get_rus_right_words(word)
    other_words = get_other_rus_words(word)
    sum_words = [right_words[0], other_words[0], other_words[1], other_words[2]]
    random.shuffle(sum_words)
    answerId = sum_words.index(right_words[0])
    markup = InlineKeyboardMarkup(row_width=2)
    for idx, val in enumerate(sum_words):
        if idx == answerId:
            markup.add(InlineKeyboardButton(val, callback_data="10"))
        else:
            markup.add(InlineKeyboardButton(val, callback_data=str(idx)))
    markup.add(inline_btn_menu)
    return markup

def getSettingsMarkup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Что пройдено", callback_data="done"), InlineKeyboardButton("Напоминания", callback_data="remember"), inline_btn_menu)
    return markup

def getMenuOnlyMarkup():
    markup = InlineKeyboardMarkup()
    markup.add(inline_btn_menu)
    return markup