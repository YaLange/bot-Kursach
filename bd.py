import sqlite3
import logging
import random
import config


def get_dict_blocks():
    con = sqlite3.connect("DataBase.db")
    cur = con.cursor()
    cur.execute("select Name, R_Name from Blocks")
    result = {}
    for row in cur:
        result[row[0]] = row[1]
    con.close()
    return result

def get_blocks_list():
    con = sqlite3.connect("DataBase.db")
    cur = con.cursor()
    cur.execute("select Name from Blocks")
    result = []
    for row in cur:
        result.append(row[0])
    con.close()
    return result

def get_blocks_list1():
    con = sqlite3.connect("DataBase.db")
    cur = con.cursor()
    cur.execute("select Name from Blocks")
    result = []
    for row in cur:
        result.append(row[0] + "1")
    con.close()
    return result

def get_rus_name_and_id(name):
    con = sqlite3.connect("DataBase.db")
    cur = con.cursor()
    cur.execute("select R_Name from Blocks where Name=\"" + name + "\"")
    row = cur.fetchone()
    rus_name = row[0]
    cur.execute("select count(*) from EWords where Block_id=(select Id from Blocks where Name=\"" + name + "\")")
    row = cur.fetchone()
    word_count = row[0]
    con.close()
    return word_count, rus_name

def get_eng_words(name1):
    name = name1.replace("1", "")
    con = sqlite3.connect("DataBase.db")
    cur = con.cursor()
    cur.execute("select Word from EWords where Block_id= (select Id from Blocks where Name=\"" + name + "\")")
    result = []
    for row in cur:
        result.append(row[0])
    con.close()
    random.shuffle(result)
    return result

def get_rus_right_words(word):
    con = sqlite3.connect("DataBase.db")
    cur = con.cursor()
    cur.execute("select Word from Translations inner join RWords on Translations.RId = RWords.Id where EId = (select Id from EWords where Word = \"" + word + "\")")
    result = []
    for row in cur:
        result.append(row[0])
    con.close()
    random.shuffle(result)
    return result

def get_other_rus_words(word):
    con = sqlite3.connect("DataBase.db")
    cur = con.cursor()
    cur.execute("select Word from Translations inner join RWords on Translations.RId = RWords.Id where EId != (select Id from EWords where Word = \"" + word + "\")")
    result = []
    for row in cur:
        result.append(row[0])
    con.close()
    random.shuffle(result)
    return result

def get_name_block_by_word(word):
    con = sqlite3.connect("DataBase.db")
    cur = con.cursor()
    cur.execute("select Name from Block where Id = (select Block_id from EWords where Word = \"" + word + "\")")
    row = cur.fetchone()
    result = row[0]
    con.close()
    return result

def set_user(id):
    con = sqlite3.connect("DataBase.db")
    cur = con.cursor()
    print(id)
    cur.execute("insert or ignore into Users(Telegram_id) values(" + str(id) + ")")
    con.commit()
    con.close()

def set_user_block(id):
    print(config.eng_words)
    con = sqlite3.connect("DataBase.db")
    cur = con.cursor()
    cur.execute("select Block_id from EWords where Word = \"" + config.eng_words[0] + "\"")
    row = cur.fetchone()
    block_id = row[0]
    user_id = []
    block_completed = []
    cur.execute("select Block_id from User_Block where User_id = " + str(id))
    for row in cur:
        block_completed.append(row[0])
    if block_id not in block_completed:
        con.cursor().execute("insert into User_Block(User_id, Block_id) values(" + str(id) + ", " + str(block_id) + ")")
        print("sssss", id, block_id)
        con.commit()
        con.close()

def get_done_blocks(id):
    con = sqlite3.connect("DataBase.db")
    cur = con.cursor()
    cur.execute("SELECT R_Name from Blocks inner join User_Block on User_Block.Block_id = Blocks.Id where User_Block.User_id = " + str(id))
    result = []
    for row in cur:
        result.append(row[0])
    return result