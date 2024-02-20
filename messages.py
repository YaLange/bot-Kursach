enter_message = 'Бот поможет Вам в обучении английскому языку. \nС его помощью вы легко сможете набрать базу слов для продолжения изучения языка'\

start_message = 'Привет!\n' + enter_message
invalid_key_message = 'Ключ "{key}" не подходит.\n' + enter_message
state_reset_message = 'Состояние успешно сброшено'
current_state_message = 'Текущее состояние - "{current_state}", что удовлетворяет условию "один из {states}"'
block_message = 'Выберите блок для изучения'
block_message_start = 'Вы выбрали блок ... Он содержит ... слов'
block_message_words = 'Тут слово из БД'


MESSAGES = {
 'start': start_message,
 'enter': enter_message,
 'invalid_key': invalid_key_message,
 'state_reset': state_reset_message,
 'current_state': current_state_message,
 'blocks_message': block_message,
 'blocks_message_start': block_message_start,
 'blocks_message_words': block_message_words,
}


def get_block_message_start(word_count, rus_name):
    return "Вы выбрали блок " + rus_name + ". Он содержит " + str(word_count) + "слов."