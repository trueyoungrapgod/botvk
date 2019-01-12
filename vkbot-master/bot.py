import sqlite3
import datetime
import threading
import time
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor



# если нет строки с ID юзера, то создать
# иначе выдать ошибку
def subUser(event, curs):
    userID = event.obj.from_id # ИД юзера
    curs.execute("SELECT EXISTS(SELECT * FROM users WHERE user_id = '%d')"%(userID))
    if (not int(curs.fetchone()[0])):
        curs.execute("INSERT INTO users (user_id, reg) VALUES ('%d', '%s')"%(userID, '0'))
        vk.messages.send(
            user_id=userID,
            random_id = 0,
            message="Вы подписались!"
        )
        PickClass(event, curs)
    else:
        vk.messages.send(
            user_id=userID,
            random_id = 0,
            message="Вы уже подписаны!"
        )
    return

def unsubUser(event, curs):
    userID = event.obj.from_id # ИД юзера
    curs.execute("SELECT EXISTS(SELECT * FROM users WHERE user_id = '%d')"%(userID))
    if (int(curs.fetchone()[0])):
        curs.execute("DELETE FROM users WHERE user_id = '%d'"%(userID))
        vk.messages.send(
            user_id=userID,
            random_id = 0,
            message="Вы отписались!"
        )
    else:
        vk.messages.send(
            user_id=userID,
            random_id = 0,
            message="Вы не подписаны!"
        )
    return

def subConversation(event, curs):
    chatID = event.chat_id # ID чата
    curs.execute("SELECT EXISTS(SELECT * FROM chats WHERE chat_id = '%d')"%(chatID))
    if (not int(curs.fetchone()[0])):
        curs.execute("INSERT INTO chats (chat_id) VALUES ('%d')"%(chatID))
        vk.messages.send(
            chat_id=chatID,
            random_id = 0,
            message="Ваша беседа подписана!"
        )
    else: # если подписка уже есть
        vk.messages.send(
            chat_id=chatID,
            random_id = 0,
            message="Ваша беседа уже подписана!"
        )
    return

def unsubConversation(event, curs):
    chatID = event.chat_id # ID чата
    curs.execute("SELECT EXISTS(SELECT * FROM chats WHERE chat_id = '%d')"%(chatID))
    if (int(curs.fetchone()[0])):
        curs.execute("DELETE FROM chats WHERE chat_id = '%d'"%(chatID))
        vk.messages.send(
            chat_id=chatID,
            random_id = 0,
            message="Ваша беседа отписана!"
        )
    else: # если подписки нет
        vk.messages.send(
            chat_id=chatID,
            random_id = 0,
            message="Ваша беседа еще не подписана!"
        )
    return
        
##def addToDelayed(event, att):
##    send = event.obj.text # текст, введенный юзером
##    if (len(send) > 11):
##       if (send[9] == '.' or send[9] == '/' and send[12] == '.' or send[12] == '/' and send[20] == ':'):
##           addToDelayed(event, att)
##           return # действие с сообщением с текстом
##        # создание списков людей, которым откладыватся рассылки #
##        date = send[7:23]
##        send = send[24:]
##        if (len(send) != 0):
##            if (len(att) != 0): # отправка рассылки при наличии аттачментов
##                curs.execute("INSERT INTO delayed (text, att, time) VALUES ('%s', '%s', '%s')"%(send, att, date))
##            else: # отправка рассылки без аттачментов
##                curs.execute("INSERT INTO delayed (text, att, time) VALUES ('%s', '%s', '%s')"%(send, '-1', date))
##        else: # отправка рассылки без текста
##            if (len(att) != 0): # но с аттачментами        
##                curs.execute("INSERT INTO delayed (text, att, time) VALUES ('%s', '%s', '%s')"%('-1', att, date))
##    return   

def SendDelayed(event, curs):
    curs.execute("UPDATE users SET menu_id = 17 WHERE user_id = '%s'"%(event.obj.from_id))
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Классы получателей', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Группы получателей', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Тип новости', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Время отправки', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Место отправки', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Отправить', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Удалить сообщение', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id = event.obj.from_id,
        random_id = 0,
        message='Отправка поста',
        keyboard = keyboard.get_keyboard()
    )
    return

def DelayedClass(event, curs):
    curs.execute("UPDATE users SET menu_id = 18 WHERE user_id = '%s'"%(event.obj.from_id))
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('9', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('10', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('11', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Все классы', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Вернуться', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id = event.obj.from_id,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message='Выберите класс'
    )
    return

def DelayedGroups(event, curs):
    curs.execute("UPDATE users SET menu_id = 19 WHERE user_id = '%s'"%(event.obj.from_id))
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('МИ', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('МЭ', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Г', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Ю', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Д', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('В', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('П', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('СЭ', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Все группы', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Вернуться', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id = event.obj.from_id,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message='Выберите группу'
    )
    return

def DelayedType(event, curs):
    curs.execute("UPDATE users SET menu_id = 20 WHERE user_id = '%s'"%(event.obj.from_id))
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Стандартные', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Важные', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Дедлайны ИВР', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Вернуться', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id = event.obj.from_id,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message='Выберите тип новостей'
    )
    return

def DelayedConv(event, curs):
    curs.execute("UPDATE users SET menu_id = 22 WHERE user_id = '%s'"%(event.obj.from_id))
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Все', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Пользователи', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Беседы', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Вернуться', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id = event.obj.from_id,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message='Выберите место отправления'
    )
    return

def DelayedPost():
    sql = sqlite3.connect('bot.db')
    curs = sql.cursor()
    longpoll = VkBotLongPoll(vk_session, '174143158')
    while (True):
        now = datetime.datetime.now()
        
        curs.execute("SELECT author FROM delayed")
        ats = curs.fetchall()
        curs.execute("SELECT text FROM delayed")
        text = curs.fetchall()
        curs.execute("SELECT att FROM delayed")
        att = curs.fetchall()
        curs.execute("SELECT time FROM delayed")
        dates = curs.fetchall()
        curs.execute("SELECT type FROM delayed")
        types = curs.fetchall()
        curs.execute("SELECT classes FROM delayed")
        classes = curs.fetchall()
        curs.execute("SELECT groups FROM delayed")
        groups = curs.fetchall()
        curs.execute("SELECT conv FROM delayed")
        conv = curs.fetchall()
        for i in range(len(dates)):
            day = int(dates[i][0][0] + dates[i][0][1])
            month = int(dates[i][0][3] + dates[i][0][4])
            year = int(dates[i][0][6] + dates[i][0][7] + dates[i][0][8] + dates[i][0][9])
            hour = int(dates[i][0][11] + dates[i][0][12])
            minute = int(dates[i][0][14] + dates[i][0][15])
            curTime = time.ctime(time.time()).split()
            curDay = int(curTime[2])
            curMonth = curTime[1]
            if curMonth == 'Jan':
                curMonth = 1
            elif curMonth == 'Feb':
                curMonth = 2
            elif curMonth == 'Mar':
                curMonth = 3
            elif curMonth == 'Apr':
                curMonth = 4
            elif curMonth == 'May':
                curMonth = 5
            elif curMonth == 'Jun':
                curMonth = 6
            elif curMonth == 'Jul':
                curMonth = 7
            elif curMonth == 'Aug':
                curMonth = 8
            elif curMonth == 'Sep':
                curMonth = 9
            elif curMonth == 'Oct':
                curMonth = 10
            elif curMonth == 'Nov':
                curMonth = 11
            elif curMonth == 'Dec':
                curMonth = 12
            curYear = int(curTime[4])
            curTime = curTime[3]
            curHour = int(curTime[0] + curTime[1])
            curMinute = int(curTime[3] + curTime[4])
            if (curYear == year and curMonth == month and curDay == day and curHour == hour and curMinute == minute):
                cl = list(map(int, classes[i][0].split()))
                gr = list(map(int, groups[i][0].split()))
                if (conv[i][0] == 0):
                    users = []
                    for l in cl:
                        for k in gr:
                            curs.execute("SELECT user_id FROM users WHERE class = '%d' AND gr = '%d' AND news_type = '%d'"%(l, k, types[i][0]))
                            try:
                                ids = curs.fetchone()[0]
                                users.append(ids)
                            except BaseException:
                                continue
                
                    curs.execute("SELECT chat_id FROM chats")
                    chats = curs.fetchall()
                    if len(text) != 0 and len(att) != 0:
                        for ids in users:
                            vk.messages.send(
                                user_id=ids,
                                random_id = 0,
                                message = text,
                                attachment = att
                            )
                        for ids in chats:
                            vk.messages.send(
                                chat_id=ids,
                                random_id = 0,
                                message = text,
                                attachment = att
                            )
                    elif len(text) == 0 and len(att) != 0:
                        for ids in users:
                            vk.messages.send(
                                user_id=ids,
                                random_id = 0,
                                attachment = att
                            )
                        for ids in chats:
                            vk.messages.send(
                                chat_id=ids,
                                random_id = 0,
                                attachment = att
                            )
                    elif len(text) != 0 and len(att) == 0:
                        for ids in users:
                            vk.messages.send(
                                user_id=ids,
                                random_id = 0,
                                message = text
                            )
                        for ids in chats:
                            vk.messages.send(
                                chat_id=ids,
                                random_id = 0,
                                message = text
                            )
                elif (conv[i][0] == 1):
                    users = []
                    for l in cl:
                        for k in gr:
                            curs.execute("SELECT user_id FROM users WHERE class = '%d' AND gr = '%d' AND news_type = '%d'"%(l, k,types[i][0]))
                            try:
                                ids = curs.fetchone()[0]
                                users.append(ids)
                            except BaseException:
                                continue
                
                    if len(text) != 0 and len(att) != 0:
                        for ids in users:
                            vk.messages.send(
                                user_id=ids,
                                random_id = 0,
                                message = text,
                                attachment = att
                            )
                    elif len(text) == 0 and len(att) != 0:
                        for ids in users:
                            vk.messages.send(
                                user_id=ids,
                                random_id = 0,
                                attachment = att
                            )
                    elif len(text) != 0 and len(att) == 0:
                        for ids in users:
                            vk.messages.send(
                                user_id=ids,
                                random_id = 0,
                                message = text
                            )
                elif (conv[i][0] == 2):  
                    curs.execute("SELECT chat_id FROM chats")
                    chats = curs.fetchall()
                    if len(text) != 0 and len(att) != 0:
                        for ids in chats:
                            vk.messages.send(
                                chat_id=ids,
                                random_id = 0,
                                message = text,
                                attachment = att
                            )
                    elif len(text) == 0 and len(att) != 0:
                        for ids in chats:
                            vk.messages.send(
                                chat_id=ids,
                                random_id = 0,
                                attachment = att
                            )
                    elif len(text) != 0 and len(att) == 0:
                        for ids in chats:
                            vk.messages.send(
                                chat_id=ids,
                                random_id = 0,
                                message = text
                            )
                curs.execute("DELETE FROM delayed WHERE author = '%d'"%(int(ats[i][0])))
            
                
        time.sleep(60)            
    return

def SendMessage(event, curs):
    curs.execute("UPDATE users SET menu_id = 13 WHERE user_id = '%s'"%(event.obj.from_id))
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Классы получателей', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Группы получателей', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Тип новости', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Место отправки', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Отправить', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Удалить сообщение', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id = event.obj.from_id,
        random_id = 0,
        message='Отправка поста',
        keyboard = keyboard.get_keyboard()
    )
    return

def MessageClass(event, curs):
    curs.execute("UPDATE users SET menu_id = 14 WHERE user_id = '%s'"%(event.obj.from_id))
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('9', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('10', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('11', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Все классы', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Вернуться', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id = event.obj.from_id,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message='Выберите класс'
    )
    return

def MessageGroups(event, curs):
    curs.execute("UPDATE users SET menu_id = 15 WHERE user_id = '%s'"%(event.obj.from_id))
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('МИ', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('МЭ', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Г', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Ю', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Д', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('В', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('П', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('СЭ', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Все группы', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Вернуться', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id = event.obj.from_id,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message='Выберите группу'
    )
    return

def MessageType(event, curs):
    curs.execute("UPDATE users SET menu_id = 16 WHERE user_id = '%s'"%(event.obj.from_id))
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Стандартные', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Важные', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Дедлайны ИВР', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Вернуться', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id = event.obj.from_id,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message='Выберите тип новостей'
    )
    return

def MessageConv(event, curs):
    curs.execute("UPDATE users SET menu_id = 23 WHERE user_id = '%s'"%(event.obj.from_id))
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Все', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Пользователи', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Беседы', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Вернуться', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id = event.obj.from_id,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message='Выберите место отправления'
    )
    return

def MessagePost(event, curs):
    userID = event.obj.from_id
    curs.execute("SELECT text FROM posts WHERE author = '%d'"%(userID))
    text = curs.fetchone()[0]
    curs.execute("SELECT att FROM posts WHERE author = '%d'"%(userID))
    att = curs.fetchone()[0]
    curs.execute("SELECT classes FROM posts WHERE author = '%d'"%(userID))
    cl = list(map(int, curs.fetchone()[0].split()))
    curs.execute("SELECT groups FROM posts WHERE author = '%d'"%(userID))
    gr = list(map(int, curs.fetchone()[0].split()))
    curs.execute("SELECT type FROM posts WHERE author = '%d'"%(userID))
    tp = curs.fetchone()[0]
    curs.execute("SELECT conv FROM posts WHERE author = '%d'"%(userID))
    conv = curs.fetchone()[0]
    if (conv == 0):
        users = []
        for l in cl:
            for k in gr:
                curs.execute("SELECT user_id FROM users WHERE class = '%d' AND gr = '%d' AND news_type = '%d'"%(l, k, tp))
                try:
                    ids = curs.fetchone()[0]
                    users.append(ids)
                except BaseException:
                    continue
    
        curs.execute("SELECT chat_id FROM chats")
        chats = curs.fetchall()
        if len(text) != 0 and len(att) != 0:
            for ids in users:
                vk.messages.send(
                    user_id=ids,
                    random_id = 0,
                    message = text,
                    attachment = att
                )
            for ids in chats:
                vk.messages.send(
                    chat_id=ids,
                    random_id = 0,
                    message = text,
                    attachment = att
                )
        elif len(text) == 0 and len(att) != 0:
            for ids in users:
                vk.messages.send(
                    user_id=ids,
                    random_id = 0,
                    attachment = att
                )
            for ids in chats:
                vk.messages.send(
                    chat_id=ids,
                    random_id = 0,
                    attachment = att
                )
        elif len(text) != 0 and len(att) == 0:
            for ids in users:
                vk.messages.send(
                    user_id=ids,
                    random_id = 0,
                    message = text
                )
            for ids in chats:
                vk.messages.send(
                    chat_id=ids,
                    random_id = 0,
                    message = text
                )
    elif (conv == 1):
        users = []
        for l in cl:
            for k in gr:
                curs.execute("SELECT user_id FROM users WHERE class = '%d' AND gr = '%d' AND news_type = '%d'"%(l, k,tp))
                try:
                    ids = curs.fetchone()[0]
                    users.append(ids)
                except BaseException:
                    continue
    
        if len(text) != 0 and len(att) != 0:
            for ids in users:
                vk.messages.send(
                    user_id=ids,
                    random_id = 0,
                    message = text,
                    attachment = att
                )
        elif len(text) == 0 and len(att) != 0:
            for ids in users:
                vk.messages.send(
                    user_id=ids,
                    random_id = 0,
                    attachment = att
                )
        elif len(text) != 0 and len(att) == 0:
            for ids in users:
                vk.messages.send(
                    user_id=ids,
                    random_id = 0,
                    message = text
                )
    elif (conv == 2):  
        curs.execute("SELECT chat_id FROM chats")
        chats = curs.fetchall()
        if len(text) != 0 and len(att) != 0:
            for ids in chats:
                vk.messages.send(
                    chat_id=ids,
                    random_id = 0,
                    message = text,
                    attachment = att
                )
        elif len(text) == 0 and len(att) != 0:
            for ids in chats:
                vk.messages.send(
                    chat_id=ids,
                    random_id = 0,
                    attachment = att
                )
        elif len(text) != 0 and len(att) == 0:
            for ids in chats:
                vk.messages.send(
                    chat_id=ids,
                    random_id = 0,
                    message = text
                )
    curs.execute("DELETE FROM posts WHERE author = '%d'"%(userID))
    return        
def isAdmin(event, curs):
    userID = event.obj.from_id # ИД юзера
    curs.execute("SELECT user_id FROM admins")
    adms = curs.fetchall()
    for ids in range(len(adms)):
        if str(adms[ids][0]) == str(userID):
            return True
    return False

            
def PickClass(event, curs):
    userID = event.obj.from_id
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('9', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('10', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('11', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id=userID,
        random_id = 0,
        message="Выберите класс",
        keyboard = keyboard.get_keyboard()
    )
    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
    reg = int(curs.fetchone()[0])
    if (reg != 8):
        curs.execute("UPDATE users SET reg = 0 WHERE user_id = '%s'"%(event.obj.from_id))
    curs.execute("UPDATE users SET menu_id = 0 WHERE user_id = '%s'"%(event.obj.from_id))
    return


def PickGroup(event, curs):
    userID = event.obj.from_id
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('МатИнфо', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('МатЭк', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Гум', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Юр', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Дизайн', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Восток', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Психология', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('СоцЭк', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id=userID,
        random_id = 0,
        message="Выберите направление",
        keyboard = keyboard.get_keyboard()
    )
    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
    reg = int(curs.fetchone()[0])
    if (reg != 8):
        curs.execute("UPDATE users SET reg = 1 WHERE user_id = '%s'"%(event.obj.from_id))
    curs.execute("UPDATE users SET menu_id = 1 WHERE user_id = '%s'"%(event.obj.from_id))
    return
    
def PickSubClass(event, curs):
    userID = event.obj.from_id
    keyboard = VkKeyboard(one_time=True)
    userID = event.obj.from_id
    curs.execute("SELECT gr FROM users WHERE user_id = '%d'"%(userID))
    cl = int(curs.fetchone()[0])
    if cl == 0 or cl == 1 or cl == 2 or cl == 7:
        keyboard.add_button('1', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('2', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('3', color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button('4', color=VkKeyboardColor.DEFAULT)
        keyboard.add_button('5', color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()
        keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    else:
        if cl == 3 or cl == 5 or cl == 6:
            keyboard.add_button('1', color=VkKeyboardColor.DEFAULT)
            keyboard.add_button('2', color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
        elif cl == 4:
            keyboard.add_button('1', color=VkKeyboardColor.DEFAULT)
            keyboard.add_button('2', color=VkKeyboardColor.DEFAULT)
            keyboard.add_button('3', color=VkKeyboardColor.DEFAULT)
            keyboard.add_line()
            keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id=userID,
        random_id = 0,
        message="Выберите группу",
        keyboard = keyboard.get_keyboard()
    )
    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
    reg = int(curs.fetchone()[0])
    if (reg != 8):
        curs.execute("UPDATE users SET reg = 2 WHERE user_id = '%s'"%(event.obj.from_id))
    curs.execute("UPDATE users SET menu_id = 2 WHERE user_id = '%s'"%(event.obj.from_id))
    return
    
def FirstQuestion(event, curs):
    userID = event.obj.from_id
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('1', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('2', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('3', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id=userID,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message="Вопрос [1/3]:\n1. Все\n2. Только самые важные \n3. Только о дедлайнах ИВР"
    )
    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
    reg = int(curs.fetchone()[0])
    if (reg != 8):
        curs.execute("UPDATE users SET reg = 3 WHERE user_id = '%s'"%(event.obj.from_id))
    curs.execute("UPDATE users SET menu_id = 3 WHERE user_id = '%s'"%(event.obj.from_id))
    return
    
def SecondQuestion(event, curs):
    userID = event.obj.from_id
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('1', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('2', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id=userID,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message="Вопрос [2/3]: О новостях каких проектов Вы хотите получать новости? \n1. Всех \n2. Выбрать важные"
    )
    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
    reg = int(curs.fetchone()[0])
    if (reg != 8):
        curs.execute("UPDATE users SET reg = 4 WHERE user_id = '%s'"%(event.obj.from_id))
    curs.execute("UPDATE users SET menu_id = 4 WHERE user_id = '%s'"%(event.obj.from_id))
    return
    
def ChooseGroups(event, curs):
    userID = event.obj.from_id
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('1', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('2', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('3', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('4', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('5', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('6', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('7', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('8', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('9', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('10', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('11', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('12', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('13', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('14', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('15', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('16', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('17', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Закончить', color=VkKeyboardColor.DEFAULT)
    vk.messages.send(
        user_id=userID,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message="Выбор группы"
    )
    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
    reg = int(curs.fetchone()[0])
    if (reg != 8):
        curs.execute("UPDATE users SET reg = 5 WHERE user_id = '%s'"%(event.obj.from_id))
    curs.execute("UPDATE users SET menu_id = 5 WHERE user_id = '%s'"%(event.obj.from_id))
    return


def ThirdQuestion(event, curs):
    userID = event.obj.from_id
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('1', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('2', color=VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    vk.messages.send(
        user_id=userID,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message="Вопрос [3/3]: За сколько информировать:\n1. За неделю \n2. За 1-2 дня до мероприятия "
    )
    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
    reg = int(curs.fetchone()[0])
    if (reg != 8):
        curs.execute("UPDATE users SET reg = 6 WHERE user_id = '%s'"%(event.obj.from_id))
    curs.execute("UPDATE users SET menu_id = 6 WHERE user_id = '%s'"%(event.obj.from_id))
    return

def MainMenu(event, curs):
     userID = event.obj.from_id
     keyboard = VkKeyboard(one_time=True)
     keyboard.add_button('Настройки', color=VkKeyboardColor.DEFAULT)
     keyboard.add_button('Поделиться', color=VkKeyboardColor.DEFAULT)
     keyboard.add_button('Отзыв', color=VkKeyboardColor.DEFAULT)
     keyboard.add_line()
     keyboard.add_button('Отписаться', color=VkKeyboardColor.NEGATIVE)
     vk.messages.send(
        user_id=userID,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message="Главное меню"
     )
     curs.execute("UPDATE users SET menu_id = 10 WHERE user_id = '%s'"%(event.obj.from_id))
     return

def Settings(event, curs):
     userID = event.obj.from_id
     keyboard = VkKeyboard(one_time=True)
     curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
     reg = int(curs.fetchone()[0])
     keyboard.add_button('Класс', color=VkKeyboardColor.DEFAULT)
     if reg >= 1:
         keyboard.add_button('Направление', color=VkKeyboardColor.DEFAULT)
     if reg >= 2:
         keyboard.add_button('Группа', color=VkKeyboardColor.DEFAULT)
         keyboard.add_line()
     if reg >= 3:
         keyboard.add_button('Новости', color=VkKeyboardColor.DEFAULT)
     if reg >= 4:
         keyboard.add_button('Проекты', color=VkKeyboardColor.DEFAULT)
     if reg >= 6:
         keyboard.add_button('Время', color=VkKeyboardColor.DEFAULT)
     keyboard.add_line()
     keyboard.add_button('Вернуться', color=VkKeyboardColor.NEGATIVE)
     vk.messages.send(
        user_id=userID,
        random_id = 0,
        keyboard = keyboard.get_keyboard(),
        message="Настройки"
     )
     curs.execute("UPDATE users SET menu_id = 11 WHERE user_id = '%s'"%(event.obj.from_id))
     return



def Bot():
    

    sql = sqlite3.connect('bot.db')
    curs = sql.cursor()
    longpoll = VkBotLongPoll(vk_session, '174143158')
    for event in longpoll.listen():
        if (event.type == VkBotEventType.MESSAGE_NEW): # если новое сообщение
            if (len(event.obj.text) != 0):
                if (event.obj.text[0] == '/'):
                    text = event.obj.text
                    if (text == '/menu'):
                        MainMenu(event, curs)
                    if (text == '/sub'):
                        if (event.from_user):
                            subUser(event, curs)
                            sql.commit()
                        elif (event.from_chat):
                            subConversation(event, curs)
                            sql.commit()
                    elif (text == '/unsub'):
                        if (event.from_user):
                            unsubUser(event, curs)
                            sql.commit()
                        elif (event.from_chat):
                            unsubConversation(event, curs)
                            sql.commit()
                    elif (text == '/send' and event.from_user):
                        if (isAdmin(event, curs)):
                            curs.execute("DELETE FROM posts WHERE author = '%d'"%(event.obj.from_id))
                            curs.execute("INSERT INTO posts (author) VALUES ('%d')"%(event.obj.from_id))
                            SendMessage(event, curs)
                            sql.commit()
                    elif (text == '/delay' and event.from_user):
                        if (isAdmin(event, curs)):
                            curs.execute("DELETE FROM delayed WHERE author = '%d'"%(event.obj.from_id))
                            curs.execute("INSERT INTO delayed (author) VALUES ('%d')"%(event.obj.from_id))
                            SendDelayed(event, curs)
                            sql.commit()
                else:
                    if (event.from_user):
                        userID = event.obj.from_id # ИД юзера
                        curs.execute("SELECT EXISTS(SELECT * FROM users WHERE user_id = '%d')"%(userID))
                        if (not int(curs.fetchone()[0])):
                            vk.messages.send(
                                user_id=userID,
                                random_id = 0,
                                message="Вы не подписаны! /sub - подписаться на рассылку"
                            )
                        else:
                            curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                            reg = int(curs.fetchone()[0])
                            curs.execute("SELECT menu_id FROM users WHERE user_id = '%s'"%(event.obj.from_id))
                            menu_id = int(curs.fetchone()[0])
                            st = 0
                            if (reg == 0 and menu_id == 0):
                                if event.obj.text == '9':
                                    curs.execute("UPDATE users SET class = 9 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == '10':
                                    curs.execute("UPDATE users SET class = 10 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == '11':
                                    curs.execute("UPDATE users SET class = 11 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'Отмена':
                                    st = 1
                                    vk.messages.send(
                                        user_id=userID,
                                        random_id = 0,
                                        message="Вы сможете установить персональные настройки рассылки, используя главное меню (/menu)"
                                    )
                                else:
                                    st = 1
                                if (st == 0):         
                                     vk.messages.send(
                                         user_id=userID,
                                         random_id = 0,
                                         message="Класс выбран!"
                                     )
                                     PickGroup(event, curs)
                            elif (reg == 1 and menu_id == 1):
                                if event.obj.text == 'МатИнфо':
                                    curs.execute("UPDATE users SET gr = 0 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'МатЭк':
                                    curs.execute("UPDATE users SET gr = 1 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'Гум':
                                    curs.execute("UPDATE users SET gr = 2 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'Юр':
                                    curs.execute("UPDATE users SET gr = 3 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'Дизайн':
                                    curs.execute("UPDATE users SET gr = 4 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'Восток':
                                    curs.execute("UPDATE users SET gr = 5 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'Психология':
                                    curs.execute("UPDATE users SET gr = 6 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'СоцЭк':
                                    curs.execute("UPDATE users SET gr = 7 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'Отмена':
                                    st = 1
                                    vk.messages.send(
                                        user_id=userID,
                                        random_id = 0,
                                        message="Вы сможете установить персональные настройки рассылки, используя главное меню (/menu)"
                                    )
                                else:
                                    st = 1
                                if (st == 0):
                                    vk.messages.send(
                                        user_id=userID,
                                        random_id = 0,
                                        message="Направление выбрано!"
                                    )
                                    PickSubClass(event, curs)
                            elif (reg == 2 and menu_id == 2):
                                if event.obj.text == '1':
                                    curs.execute("UPDATE users SET subclass = 1 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == '2':
                                    curs.execute("UPDATE users SET subclass = 2 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == '3':
                                    curs.execute("UPDATE users SET subclass = 3 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == '4':
                                    curs.execute("UPDATE users SET subclass = 4 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == '5':
                                    curs.execute("UPDATE users SET subclass = 5 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'Отмена':
                                    st = 1
                                    vk.messages.send(
                                        user_id=userID,
                                        random_id = 0,
                                        message="Вы сможете установить персональные настройки рассылки, используя главное меню (/menu)"
                                    )
                                else:
                                    st = 1
                                if (st == 0):
                                    vk.messages.send(
                                        user_id=userID,
                                        random_id = 0,
                                        message="Группа выбрана!"
                                    )
                                    FirstQuestion(event, curs)
                            elif (reg == 3 and menu_id == 3):
                                if event.obj.text == '1':
                                    curs.execute("UPDATE users SET news_type = 1 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == '2':
                                    curs.execute("UPDATE users SET news_type = 2 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == '3':
                                    curs.execute("UPDATE users SET news_type = 3 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'Отмена':
                                    st = 1
                                    vk.messages.send(
                                        user_id=userID,
                                        random_id = 0,
                                        message="Вы сможете установить персональные настройки рассылки, используя главное меню (/menu)"
                                    )
                                else:
                                    st = 1
                                if (st == 0):
                                    vk.messages.send(
                                        user_id=userID,
                                        random_id = 0,
                                        message="Новости выбраны"
                                    )
                                    SecondQuestion(event, curs)
                            elif (reg == 4 and menu_id == 4):
                                if event.obj.text == '1':
                                    curs.execute("UPDATE users SET project_list = -1 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == '2':
                                    ChooseGroups(event, curs)
                                elif event.obj.text == 'Отмена':
                                    st = 1
                                    vk.messages.send(
                                        user_id=userID,
                                        random_id = 0,
                                        message="Вы сможете установить персональные настройки рассылки, используя главное меню (/menu)"
                                    )
                                else:
                                    st = 1
                                if (st == 0):
                                    vk.messages.send(
                                        user_id=userID,
                                        random_id = 0,
                                        message="Новости выбраны"
                                    )
                                    ThirdQuestion(event, curs)
                            elif (reg == 5 and menu_id == 5):
                                if (event.obj.text == '1'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '1 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '2'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '2 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '3'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '3 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '4'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '4 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '5'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '5 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '6'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '6 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '7'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '7 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '8'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '8 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '9'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '9 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '10'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '10 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '11'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '11 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '12'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '12 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '13'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '13 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '14'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '14 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '15'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '15 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '16'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '16 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == '17'):
                                    curs.execute("SELECT reg FROM users WHERE user_id = '%d'"%(userID))
                                    s = curs.fetchone()[0]
                                    s += '17 '
                                    curs.execute("UPDATE users SET project_list = '%s' WHERE user_id = '%d'"%(s, userID))
                                elif (event.obj.text == 'Закончить'):
                                    curs.execute("UPDATE users SET reg = 6 WHERE user_id = '%d'"%(userID))
                                    

                            elif (reg == 6 and menu_id == 6):
                                if event.obj.text == '1':
                                    curs.execute("UPDATE users SET inform_time = 1 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == '2':
                                    curs.execute("UPDATE users SET inform_time = 2 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'Отмена':
                                    st = 1
                                    vk.messages.send(
                                        user_id=userID,
                                        random_id = 0,
                                        message="Вы сможете установить персональные настройки рассылки, используя главное меню (/menu)"
                                    )
                                else:
                                    st = 1
                                if (st == 0):
                                    vk.messages.send(
                                        user_id=userID,
                                        random_id = 0,
                                        message="Ваша рассылка настроена! Вы сможете в любой момент настроить ее заново, используя главное меню (/menu)"
                                    )
                            elif (menu_id == 10):
                                if event.obj.text == 'Настройки':
                                    Settings(event, curs)
                                elif event.obj.text == 'Поделиться':
                                    print('Я поделился')
                                    MainMenu(event, curs)
                                elif event.obj.text == 'Отзыв':
                                    vk.messages.send(
                                        user_id = userID,
                                        random_id = 0,
                                        message="Введите ваш отзыв"
                                    )         
                                    curs.execute("UPDATE users SET menu_id = 12 WHERE user_id = '%s'"%(event.obj.from_id))
                                elif event.obj.text == 'Отписаться':
                                    unsubUser(event, curs)

                            elif (menu_id == 11):
                                if event.obj.text == 'Класс':
                                    PickClass(event, curs)
                                elif event.obj.text == 'Направление':
                                    PickGroup(event, curs)
                                elif event.obj.text == 'Группа':
                                    PickSubClass(event, curs)
                                elif event.obj.text == 'Новости':
                                    FirstQuestion(event, curs)
                                elif event.obj.text == 'Проекты':
                                    SecondQuestion(event, curs)
                                elif event.obj.text == 'Время':
                                    ThirdQuestion(event, curs)
                                elif event.obj.text == 'Вернуться':
                                    MainMenu(event, curs)
                            elif (menu_id == 12):
                                text = "Отзыв от ID " + str(event.obj.from_id) + ". Текст: " + event.obj.text
                                vk.messages.send(
                                    user_id = 290620897,
                                    random_id = 0,
                                    message = text
                                )
                                curs.execute("UPDATE users SET menu_id = 10 WHERE user_id = '%s'"%(event.obj.from_id))
                                MainMenu(event, curs)
                            elif (menu_id == 13):
                                if event.obj.text == 'Классы получателей':
                                    MessageClass(event, curs)
                                elif event.obj.text == 'Группы получателей':
                                    MessageGroups(event, curs)
                                elif event.obj.text == 'Тип новости':
                                    MessageType(event, curs)
                                elif event.obj.text == 'Место отправки':
                                    MessageConv(event, curs)
                                elif event.obj.text == 'Отправить':
                                    MessagePost(event, curs)
                                elif event.obj.text == 'Удалить сообщение':
                                    curs.execute("DELETE FROM posts WHERE author = '%d'"%(userID))
                                else:
                                    curs.execute("SELECT text FROM posts WHERE author = '%d'"%(userID))
                                    text = curs.fetchone()[0]
                                    curs.execute("SELECT att FROM posts WHERE author = '%d'"%(userID))
                                    att = curs.fetchone()[0]

                                    if len(text) == 0 and len(att) == 0:
                                        conv = vk.messages.getConversationsById(peer_ids = userID) 
                                        lMes = conv.get('items')[0].get('last_message_id') 
                                        stats = vk.messages.getById(
                                            message_ids = lMes,
                                            extended = 1
                                        )
                                        atts = stats.get('items')[0].get('attachments') 
                                        att = ''

                                        for i in range(len(atts)):
                                            attType = atts[i].get('type')
                                            att += attType + str(atts[i].get(attType).get('owner_id')) + '_' + str(atts[i].get(attType).get('id')) + ','
                                            if (str(atts[i].get(attType).get('access_key')) != 'None'):
                                                att = att[:len(att)-1]
                                                att += '_' + str(atts[i].get(attType).get('access_key')) + ','

                                                
                                        att = att[:len(att)-1]
                                        send = event.obj.text

                                        if len(send) != 0:
                                            curs.execute("UPDATE posts SET text = '%s' WHERE author = '%s'"%(send, userID))
                                        if len(att) != 0:
                                            curs.execute("UPDATE posts SET att = '%s' WHERE author = '%s'"%(send, userID))
                                        SendMessage(event, curs)
                            elif (menu_id == 14):
                                st = 0
                                curs.execute("SELECT classes FROM posts WHERE author = '%d'"%(userID))
                                cl = curs.fetchone()[0]
                                if event.obj.text == '9':
                                    cl += '9 '
                                elif event.obj.text == '10':
                                    cl += '10 '
                                elif event.obj.text == '11':
                                    cl += '11 '
                                elif event.obj.text == 'Все классы':
                                    cl = '9 10 11'
                                    st = 1
                                    curs.execute("UPDATE posts SET classes = '%s' WHERE author = '%d'"%(cl, userID))
                                    SendMessage(event, curs)
                                elif event.obj.text == 'Вернуться':
                                    st = 1
                                    SendMessage(event, curs)
                                if st == 0:
                                    curs.execute("UPDATE posts SET classes = '%s' WHERE author = '%d'"%(cl, userID))
                                    MessageClass(event, curs)

                            elif (menu_id == 15):
                                st = 0
                                curs.execute("SELECT groups FROM posts WHERE author = '%d'"%(userID))
                                gr = curs.fetchone()[0]
                                if event.obj.text == 'МИ':
                                    gr += '0 '
                                elif event.obj.text == 'МЭ':
                                    gr += '1 '
                                elif event.obj.text == 'Г':
                                    gr += '2 '
                                elif event.obj.text == 'Ю':
                                    gr += '3 '
                                elif event.obj.text == 'Д':
                                    gr += '4 '
                                elif event.obj.text == 'В':
                                    gr += '5 '
                                elif event.obj.text == 'П':
                                    gr += '6 '
                                elif event.obj.text == 'СЭ':
                                    gr += '7 '
                                elif event.obj.text == 'Все группы':
                                    gr = '0 1 2 3 4 5 6 7'
                                    st = 1
                                elif event.obj.text == 'Вернуться':
                                    st = 1
                                    SendMessage(event, curs)
                                if st == 0:
                                    curs.execute("UPDATE posts SET groups = '%s' WHERE author = '%d'"%(gr, userID))
                                    MessageGroups(event, curs)
                                else:
                                    curs.execute("UPDATE posts SET groups = '%s' WHERE author = '%d'"%(gr, userID))
                                    SendMessage(event, curs)

                            elif (menu_id == 16):
                                if event.obj.text == 'Стандартные':
                                    curs.execute("UPDATE delayed SET type = 1 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Важные':
                                    curs.execute("UPDATE delayed SET type = 2 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Дедлайны ИВР':
                                    curs.execute("UPDATE delayed SET type = 3 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Вернуться':
                                    SendMessage(event, curs)
                                SendMessage(event, curs)
                                
                            elif (menu_id == 17):
                                if event.obj.text == 'Классы получателей':
                                    DelayedClass(event, curs)
                                elif event.obj.text == 'Группы получателей':
                                    DelayedGroups(event, curs)
                                elif event.obj.text == 'Тип новости':
                                    DelayedType(event, curs)
                                elif event.obj.text == 'Место отправки':
                                    DelayedConv(event, curs)
                                elif event.obj.text == 'Время отправки':
                                    curs.execute("UPDATE users SET menu_id = 21 WHERE user_id = '%d'"%(event.obj.from_id))
                                elif event.obj.text == 'Отправить':
                                    curs.execute("SELECT time FROM delayed WHERE author = '%d'"%(event.obj.from_id))
                                    date = curs.fetchone()[0]
                                    text = "Сообщение будет опубликовано " + date
                                    vk.messages.send(
                                        user_id=event.obj.from_id,
                                        random_id = 0,
                                        message=text
                                    )
                                    MainMenu(event, curs)
                                elif event.obj.text == 'Удалить сообщение':
                                    curs.execute("DELETE FROM delayed WHERE author = '%d'"%(userID))
                                else:
                                    curs.execute("SELECT text FROM delayed WHERE author = '%d'"%(userID))
                                    text = curs.fetchone()[0]
                                    curs.execute("SELECT att FROM delayed WHERE author = '%d'"%(userID))
                                    att = curs.fetchone()[0]

                                    if len(text) == 0 and len(att) == 0:
                                        conv = vk.messages.getConversationsById(peer_ids = userID) 
                                        lMes = conv.get('items')[0].get('last_message_id') 
                                        stats = vk.messages.getById(
                                            message_ids = lMes,
                                            extended = 1
                                        )
                                        atts = stats.get('items')[0].get('attachments') 
                                        att = ''

                                        for i in range(len(atts)):
                                            attType = atts[i].get('type')
                                            att += attType + str(atts[i].get(attType).get('owner_id')) + '_' + str(atts[i].get(attType).get('id')) + ','
                                            if (str(atts[i].get(attType).get('access_key')) != 'None'):
                                                att = att[:len(att)-1]
                                                att += '_' + str(atts[i].get(attType).get('access_key')) + ','

                                                
                                        att = att[:len(att)-1]
                                        send = event.obj.text

                                        if len(send) != 0:
                                            curs.execute("UPDATE delayed SET text = '%s' WHERE author = '%s'"%(send, userID))
                                        if len(att) != 0:
                                            curs.execute("UPDATE delayed SET att = '%s' WHERE author = '%s'"%(send, userID))
                                    SendDelayed(event, curs)
                                        
                            elif (menu_id == 18):
                                st = 0
                                curs.execute("SELECT classes FROM delayed WHERE author = '%d'"%(userID))
                                cl = curs.fetchone()[0]
                                if event.obj.text == '9':
                                    cl += '9 '
                                elif event.obj.text == '10':
                                    cl += '10 '
                                elif event.obj.text == '11':
                                    cl += '11 '
                                elif event.obj.text == 'Все классы':
                                    cl = '9 10 11'
                                    st = 1
                                    curs.execute("UPDATE delayed SET classes = '%s' WHERE author = '%d'"%(cl, userID))
                                    SendDelayed(event, curs)
                                elif event.obj.text == 'Вернуться':
                                    st = 1
                                    SendDelayed(event, curs)
                                if st == 0:
                                    curs.execute("UPDATE delayed SET classes = '%s' WHERE author = '%d'"%(cl, userID))
                                    DelayedClass(event, curs)

                            elif (menu_id == 19):
                                st = 0
                                curs.execute("SELECT groups FROM delayed WHERE author = '%d'"%(userID))
                                gr = curs.fetchone()[0]
                                if event.obj.text == 'МИ':
                                    gr += '0 '
                                elif event.obj.text == 'МЭ':
                                    gr += '1 '
                                elif event.obj.text == 'Г':
                                    gr += '2 '
                                elif event.obj.text == 'Ю':
                                    gr += '3 '
                                elif event.obj.text == 'Д':
                                    gr += '4 '
                                elif event.obj.text == 'В':
                                    gr += '5 '
                                elif event.obj.text == 'П':
                                    gr += '6 '
                                elif event.obj.text == 'СЭ':
                                    gr += '7 '
                                elif event.obj.text == 'Все группы':
                                    gr = '0 1 2 3 4 5 6 7'
                                    st = 1
                                elif event.obj.text == 'Вернуться':
                                    st = 1
                                    SendDelayed(event, curs)
                                if st == 0:
                                    curs.execute("UPDATE delayed SET groups = '%s' WHERE author = '%d'"%(gr, userID))
                                    DelayedGroups(event, curs)
                                elif st == 1:
                                    curs.execute("UPDATE delayed SET groups = '%s' WHERE author = '%d'"%(gr, userID))
                                    SendDelayed(event, curs)
                                    

                            elif (menu_id == 20):
                                if event.obj.text == 'Стандартные':
                                    curs.execute("UPDATE delayed SET type = 1 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Важные':
                                    curs.execute("UPDATE delayed SET type = 2 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Дедлайны ИВР':
                                    curs.execute("UPDATE delayed SET type = 3 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Вернуться':
                                    SendDelayed(event, curs)
                                SendDelayed(event, curs)
                            
                            elif (menu_id == 21):
                                text = event.obj.text
                                if text[2] == '.' and text[5] == '.' and text[10] == ' ' and text[13] == ':' and len(text) == 16:
                                    if int(text[0]+text[1]) > 0 and int(text[0]+text[1]) <= 31 and int(text[3]+text[4]) > 0 and int(text[3]+text[4]) <= 12 and int(text[6] + text[7] + text[8] + text[9]) >= 2019 and int(text[11]+text[12]) >= 0 and int(text[11]+text[12]) <= 24 and int(text[14]+text[15]) >= 0 and int(text[14]+text[15]) <= 60:
                                        curs.execute("UPDATE delayed SET time = '%s' WHERE author = '%d'"%(text, event.obj.from_id))
                                        SendDelayed(event, curs)
                                    else:
                                        vk.messages.send(
                                            user_id=event.obj.from_id,
                                            random_id = 0,
                                            message="Ошибка ввода даты"
                                        )
                                else:
                                    vk.messages.send(
                                        user_id=event.obj.from_id,
                                        random_id = 0,
                                        message="Ошибка ввода даты"
                                    )

                            elif (menu_id == 22):
                                if event.obj.text == 'Все':
                                    curs.execute("UPDATE delayed SET conv = 0 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Пользователи':
                                    curs.execute("UPDATE delayed SET conv = 1 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Беседы':
                                    curs.execute("UPDATE delayed SET conv = 2 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Вернуться':
                                    SendDelayed(event, curs)
                                SendDelayed(event, curs)

                            elif (menu_id == 23):
                                if event.obj.text == 'Все':
                                    curs.execute("UPDATE posts SET conv = 0 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Пользователи':
                                    curs.execute("UPDATE posts SET conv = 1 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Беседы':
                                    curs.execute("UPDATE posts SET conv = 2 WHERE author = '%d'"%(userID))
                                elif event.obj.text == 'Вернуться':
                                    SendMessage(event, curs)
                                SendMessage(event, curs)
                                        
                                    
                                    
                                
        sql.commit()
                                
                                

vk_session = vk_api.VkApi(token='212bfe399afff4b3ea2d0f12d16e2885fb92320f365f6fb514a56b6ae32f12de0456269c19df73e5503a1')
# longpoll = VkBotLongPoll(vk_session, '174143158')
vk = vk_session.get_api()
post = threading.Event()
postThread = threading.Thread(target=DelayedPost)

bot = threading.Event()
botThread= threading.Thread(target = Bot)

postThread.start()
botThread.start()

post.set()

postThread.join()
botThread.join()






