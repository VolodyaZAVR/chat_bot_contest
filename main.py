# -*- coding: utf8 -*-

import telebot
import sqlite3
from telebot import types
import time

# Создаем бота. Token - уникальный ключ нашего бота полученный от botfather
bot = telebot.TeleBot(TOKEN, skip_pending=True)
# Стираем неактуальные сообщения пользователя
bot.remove_webhook()

# Создаем reply клавиатуру
welcome_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn1 = types.KeyboardButton('Определить тип перевозки')
btn2 = types.KeyboardButton('Внутренние перевозки')
btn3 = types.KeyboardButton('Международные перевозки')
btn4 = types.KeyboardButton('С услугами хранения')
btn5 = types.KeyboardButton('Мелкая партия')
welcome_keyboard.row(btn1)
welcome_keyboard.row(btn2, btn3)
welcome_keyboard.row(btn4, btn5)

# Кнопка возврата в меню
keyboard2 = types.InlineKeyboardMarkup()
menu_btn = types.InlineKeyboardButton("Вернуться в меню", callback_data="menu")
keyboard2.row(menu_btn)

# Клавиатура главного меню
keyboard3 = types.InlineKeyboardMarkup()
det_btn = types.InlineKeyboardButton("Определить тип перевозки", callback_data="det_transp")
set_data_btn = types.InlineKeyboardButton("Указать данные", callback_data="set_data")
reg_btn = types.InlineKeyboardButton("Регистрация в ЛК РЖД", callback_data="reg_user")
question_btn = types.InlineKeyboardButton("Часто задаваемые вопросы", callback_data="questions")
keyboard3.row(det_btn, set_data_btn)
keyboard3.row(reg_btn, question_btn)

# Оказалась не нужна в ходе разработки
# keyboard4 = types.InlineKeyboardMarkup()
# keyboard4.row(det_btn)
# keyboard4.row(reg_btn)
# keyboard4.row(question_btn)

keyboard5 = types.InlineKeyboardMarkup()
edit_btn = types.InlineKeyboardButton("Изменить данные", callback_data="edit")
keyboard5.row(det_btn)
keyboard5.row(edit_btn)
keyboard5.row(reg_btn)
keyboard5.row(question_btn)

keyboard6 = types.InlineKeyboardMarkup()
edit_cargo = types.InlineKeyboardButton("Изменить тип груза", callback_data="edit_cargo")
edit_region = types.InlineKeyboardButton("Изменить регион", callback_data="edit_region")
edit_station = types.InlineKeyboardButton("Изменить станцию", callback_data="edit_station")
reset = types.InlineKeyboardButton("Собросить данные", callback_data="reset")
keyboard6.row(edit_cargo, edit_region)
keyboard6.row(edit_station, reset)
keyboard6.row(menu_btn)

keyboard7 = types.InlineKeyboardMarkup()
yes_btn_step1 = types.InlineKeyboardButton("Да", callback_data="yes_step1")
no_btn_step1 = types.InlineKeyboardButton("Нет", callback_data="no_step1")
keyboard7.row(yes_btn_step1, no_btn_step1)

keyboard8 = types.InlineKeyboardMarkup()
yes_btn_step2 = types.InlineKeyboardButton("Да", callback_data="yes_step2")
no_btn_step2 = types.InlineKeyboardButton("Нет", callback_data="no_step2")
keyboard8.row(yes_btn_step2, no_btn_step2)

keyboard9 = types.InlineKeyboardMarkup()
yes_btn_step3 = types.InlineKeyboardButton("Да", callback_data="yes_step3")
no_btn_step3 = types.InlineKeyboardButton("Нет", callback_data="no_step3")
keyboard9.row(yes_btn_step3, no_btn_step3)

keyboard10 = types.InlineKeyboardMarkup()
web_btn = types.InlineKeyboardButton("Перейти на сайт", url="https://www.rzd.ru/")
keyboard10.row(web_btn)

empty_kb = types.InlineKeyboardMarkup()

keyboard11 = types.InlineKeyboardMarkup()
web_btn_1 = types.InlineKeyboardButton("Перейти на ссылку",
                                       url="https://docs.google.com/spreadsheets/d"
                                           "/1zgZoEa2XBqxnrVQ77hDucaEBPVfmWSVApLXNH1ll58Q/edit?usp=sharing")
keyboard11.row(web_btn_1)

keyboard12 = types.InlineKeyboardMarkup()
web_btn_2 = types.InlineKeyboardButton("Перейти на ссылку",
                                       url="https://docs.google.com/spreadsheets/d/1NDOnV1q"
                                           "-Y3R1XYI5qOb1lDllgmQyTV2E2tdfrCeUWUY/edit?usp=sharing")
keyboard12.row(web_btn_2)

keyboard13 = types.InlineKeyboardMarkup()
web_btn_3 = types.InlineKeyboardButton("Перейти на ссылку",
                                       url="https://docs.google.com/spreadsheets/d"
                                           "/1SHzRH_UIeqoEmkN4za5FeuWGColadPcEKUs2PfVt2w0/edit#gid=0")
keyboard13.row(web_btn_3)


class Users:
    def __init__(self):
        table_name = 'users.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто -3")
            cur = conn.cursor()
            cur.execute(
                'CREATE TABLE IF NOT EXISTS users (id int, first_name text, cargo_type text, carriage_type text, region text, departure_station text)')
            conn.commit()
            cur.close()
            conn.close()

        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто -3")
        self.__id = None
        self.__first_name = None
        self.__cargo_type = "Не указано"
        self.__carriage_type = ["Не определено"]
        self.__region = "Не указано"
        self.__departure_station = "Не указано"

    def add_user(self, user_id, first_name):
        print(user_id)
        flag = False
        self.__id = user_id
        self.__first_name = first_name
        table_name = 'users.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто -2")
            cur = conn.cursor()
            cur.execute(f"SELECT id FROM users WHERE id =  ?", [user_id])
            res = cur.fetchall()
            if not res:
                cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?);", (
                    user_id, first_name, "Не указано", "Не определено", "Не указано",
                    "Не указано"))
                flag = True
            conn.commit()
            cur.close()
            conn.close()

        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто -2")
        if flag:
            self.set_cargo_type(user_id, "Не указано")
            self.set_carriage_type(user_id, ["Не определено"])
            self.set_region(user_id, "Не указано")
            self.set_departure_station(user_id, "Не указано")

    def set_cargo_type(self, user_id, cargo_type):
        print(user_id)
        self.__cargo_type = cargo_type.strip()
        table_name = 'users.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто -1")
            cur = conn.cursor()
            cur.execute(f'UPDATE users SET cargo_type = ? WHERE id = ?', (cargo_type, user_id))
            print(cargo_type.strip())
            conn.commit()
            cur.close()
            conn.close()

        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто -1")

    def get_cargo_type(self, user_id):
        print(user_id)
        cargo_type = "Не найдено"
        table_name = 'users.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто 0")
            cur = conn.cursor()
            cur.execute(f'SELECT cargo_type FROM users WHERE id = ?', [user_id])
            res = cur.fetchall()
            cargo_type = res[0][0]
            conn.commit()
            cur.close()
            conn.close()
        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто 0")
        self.__cargo_type = cargo_type
        return cargo_type.strip()

    def set_carriage_type(self, user_id, carriage_type):
        print(user_id)
        if len(list(set(carriage_type))) == 1:
            carriage = carriage_type[0]
        else:
            res = ""
            for item in list(set(carriage_type)):
                res += item
                res += " "
            carriage = res.strip()
        self.__carriage_type = carriage
        table_name = 'users.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто 1")
            cur = conn.cursor()
            cur.execute(f'UPDATE users SET carriage_type = ? WHERE id = ?', (carriage, user_id))
            conn.commit()
            cur.close()
            conn.close()

        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто 1")

    def get_carriage_type(self, user_id):
        print(user_id)
        carriage_type = "Не найдено"
        table_name = 'users.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто 2")
            cur = conn.cursor()
            cur.execute(f'SELECT carriage_type FROM users WHERE id = ?', [user_id])
            res = cur.fetchall()
            carriage_type = res[0][0]
            conn.commit()
            cur.close()
            conn.close()
        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто 2")
        self.__carriage_type = carriage_type
        return carriage_type

    def show_carriage_type(self, user_id):
        carr = self.get_carriage_type(user_id)
        return carr.strip()

    def set_region(self, user_id, region):
        print(user_id)
        self.__region = region.strip()
        table_name = 'users.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто 3")
            cur = conn.cursor()
            cur.execute(f'UPDATE users SET region = ? WHERE id = ?', (region.strip(), user_id))
            conn.commit()
            cur.close()
            conn.close()

        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто 3")

    def get_region(self, user_id):
        print(user_id)
        region = "Не найдено"
        table_name = 'users.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто 4")
            cur = conn.cursor()
            cur.execute(f'SELECT region FROM users WHERE id = ?', [user_id])
            res = cur.fetchall()
            region = res[0][0]
            conn.commit()
            cur.close()
            conn.close()
        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто 4")
        self.__region = region.strip()
        return self.__region.strip()

    def set_departure_station(self, user_id, departure_station):
        print(user_id)
        self.__departure_station = departure_station.strip()
        table_name = 'users.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто 5")
            cur = conn.cursor()
            cur.execute(f'UPDATE users SET departure_station = ? WHERE id = ?', (departure_station.strip(), user_id))
            conn.commit()
            cur.close()
            conn.close()

        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто 5")

    def get_departure_station(self, user_id):
        print(user_id)
        departure_station = "Не найдено"
        table_name = 'users.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто 6")
            cur = conn.cursor()
            cur.execute(f'SELECT departure_station FROM users WHERE id = ?', (user_id,))
            res = cur.fetchall()
            departure_station = res[0][0]
            conn.commit()
            cur.close()
            conn.close()
        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто 6")
        self.__departure_station = departure_station.strip()
        return self.__departure_station.strip()


user = Users()


@bot.message_handler(commands=['start'])
def welcome(message):
    # Добавление пользователя в базу данных
    user.add_user(message.chat.id, message.from_user.first_name)
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}!\n\nЯ бот, разработанный ОАО «РЖД» (они об этом не знают) '
                     f'😁\n\n📱 Я предназначен для того, чтобы облегчить вашу связь с компанией ОАО «РЖД».\n\n🚀 С '
                     f'помощью меня Вам не придется долго искать контакты в интернете.\n\nℹ️ Я за пару минут выясню, '
                     f'что Вам нужно, и подскажу, с кем лучше связаться!\n\n▶️ Я могу помочь Вам определить нужный '
                     f'тип грузоперевозки, для этого нажмите на кнопку "Определить тип перевозки".\n\n😨 Глаза боятся? '
                     f'Руки трясутся? А мозг кричит о помощи?\nВы решили зарегестрироваться в личном кабинете!\n'
                     f'Нажмите на кнопку ниже, и я Вам помогу 😉\n\n🤓 Я вобрал в себя мудрость предков, и у меня есть '
                     f'список часто задаваемых вопросов!\n\n❓ Используйте комнду '
                     f'/help, чтобы узнать о командах бота.',
                     reply_markup=welcome_keyboard)
    bot.send_message(message.chat.id,
                     'Для облегчения нашего взаимодйствия мне понадобится информация об интересующих вас:\n<b><u>Типе '
                     'груза</u></b>\n<b><u>Регионе</u></b>\n<b><u>Станции отправления</u></b>\n\nВы можете указать '
                     'их, нажав на кнопку ниже👇️',
                     parse_mode='html',
                     reply_markup=keyboard3)


@bot.message_handler(commands=['menu'])
def back_to_menu(message):
    bot.send_message(message.chat.id,
                     f'Возврат в меню 🔙 ')
    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name},\n\n📱 Вы находитесь в главном меню! Заполните Ваши данные, '
                     f'если не сделали это раньше. 👇\n\n❗️ Воспользуйтесь моей функцией:\n<b>Определить тип '
                     f'грузоперевозки</b>\nВведите /det_transp или нажмите на кнопку  📲 \n\n🥇🥈🥉 И вы зарегестрированы в ЛК РЖД!\nДля этого '
                     f'нажмите соответствующую кнопку ниже или введите /reg_user.\n\n❗️ Список часто задаваемых вопросов - /questions.\n‼️ Список ОЧЕНЬ часто задаваемых вопросов - тоже /questions.\n\n❓ Если Вы не знаете о моих возможностях, '
                     f'то введите команду /help',
                     parse_mode='html')
    show_info(message, keyboard5)


@bot.callback_query_handler(func=lambda call: call.data == "menu")
def to_menu(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text=f'Возврат в меню 🔙 ')
    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name},\n\n📱 Вы находитесь в главном меню! Заполните Ваши данные, '
                     f'если не сделали это раньше. 👇\n\n❗️ Воспользуйтесь моей функцией:\n<b>Определить тип '
                     f'грузоперевозки</b>.\nВведите /det_transp или нажмите на кнопку  📲 \n\n🥇🥈🥉 И вы зарегестрированы в ЛК РЖД!\nДля этого '
                     f'нажмите соответствующую кнопку ниже или введите /reg_user.\n\n❗️ Список часто задаваемых вопросов - /questions.\n‼️ Список ОЧЕНЬ часто задаваемых вопросов - тоже /questions.\n\n❓ Если Вы не знаете о моих возможностях, '
                     f'то введите команду /help',
                     parse_mode='html')
    show_info(message, keyboard5)


@bot.message_handler(commands=['help'])
def process_help_command(message: types.Message):
    bot.send_message(message.chat.id,
                     "Я очень рад что ты захотел узнать обо мне подробнее 😊\n\nВот список команд, которые я могу "
                     "выполнить:\n\n/start - Запуск бота\n/menu - Перейти в меню\n/det_transp - Определить тип "
                     "грузоперевозки\n/help - Текст помощи\n/help_cargo - Список типов грузов\n/help_region - Список "
                     "регионов\n/help_station - Список станций отправления\n/set_data - Указать данные\n/edit - "
                     "Изменить данные\n/edit_cargo - Изменить тип груза\n/edit_region - Изменить "
                     "регион\n/edit_station - Изменить станцию отправления\n/reset - Сбросить данные\n/website - Перейти "
                     "на веб сайт",
                     reply_markup=keyboard2)


@bot.message_handler(commands=['website'])
def website(message):
    bot.send_message(message.chat.id, "Ссылка на сайт ОАО «РЖД»", reply_markup=keyboard10)


@bot.message_handler(commands=['show_info'])
def show_info(message, kb=keyboard5):
    bot.send_message(message.chat.id,
                     f'Вы указали для меня интересующие Вас:\n\nТип груза: <b><u>{user.get_cargo_type(message.chat.id)}</u></b>\nРегион: '
                     f'<b><u>{user.get_region(message.chat.id)}</u></b>\nСтанция отправления: <b><u>{user.get_departure_station(message.chat.id)}</u></b>',
                     parse_mode='html', reply_markup=kb)


@bot.message_handler(commands=['set_data'])
def set_data_command(message):
    if user.get_cargo_type(message.chat.id) == "Не указано":
        ask_cargo_type(message)
        return
    elif user.get_region(message.chat.id) == "Не указано":
        ask_region(message)
        return
    elif user.get_departure_station(message.chat.id) == "Не указано":
        ask_station(message)
        return
    else:
        show_info(message, keyboard6)


@bot.message_handler(commands=['edit_cargo'])
def edit_cargo_command(message):
    show_info(message, empty_kb)
    ask_cargo_type(message)


@bot.message_handler(commands=['edit_region'])
def edit_region_command(message):
    show_info(message, empty_kb)
    ask_region(message)


@bot.message_handler(commands=['edit_station'])
def edit_station_command(message):
    show_info(message, empty_kb)
    ask_station(message)


@bot.message_handler(commands=['edit'])
def edit_command(message):
    show_info(message, keyboard6)


@bot.message_handler(commands=['det_transp'])
def determinate_command(message):
    determine_transportation(message)


@bot.message_handler(commands=['reg_user'])
def reg_user_command(message):
    bot.send_message(message.chat.id,
                     "<b>Как зарегестрироваться в личном кабинете?</b>\n"
                     "Для регистрации в личном кабинете:\n"
                     "1. Перейдите на страницу личного кабинета РЖД в раздел Регистрация https://cargolk.rzd.ru/sign_up\n"
                     "2. Выберите способ регистрации без помощи АС ЭТРАН (в этом случае информация о компании автоматически заполнится на основе данных из налоговой службы)\n"
                     "3. Введите ИНН или ЕЛС вашей компании\n"
                     "4. Выберите вашу роль - генеральный директор или менеджер. От этого выбора будет зависеть предоставляемый Вам функционал (генеральный директор имеет полный набор прав, доступны все функции Личного кабинета; менеджер может управлять компанией в ЛК, работать с документами и договорами, имеет права передоверия и последующего передоверия)\n"
                     "5. Для продолжения регистрации Вам необходимо скачать предоставляемые на странице регистрации шаблоны заявления о присоединении к положению об организации расчётов;  информационной справки, содержащей сведения о владельцах контрагента, включая конечных бенефициаров, с приложением подтверждающих документов; доверенности на представление клиента в ЛК (если ваша роль - менеджер)\n"
                     "6. Далее Вам необходимо заполнить информацию о вашей компании, а также ее адрес и ТЦФТО для обслуживания \n"
                     "7. После этого необходимо загрузить документы, указанные в пукте 5 этой инструкции\n"
                     "8. Следующим шагом является заполнение ваших персональных данных\n"
                     "9. Последним является заполнение регистрационных данных, таких как логин и пароль.\n\n"
                     "После выполнения этих шагов ваша заявка должна поступить в систему. Учтите, что после регистрации Вам будут выданы реквизиты и счет на оплату в размере 100 рублей, который необходимо будет оплатить от имени вашей компании. После оплаты просиходит подтверждение того, что Вы действительно являетесь гениральным директором или менеджером регистрируемой компании. В будущем данные средства можно будет использовать для оплаты платных услуг.\n\n"
                     "Надеюсь я Вам помог 😊",
                     parse_mode='html',
                     reply_markup=keyboard2)


@bot.message_handler(commands=['questions'])
def questions_command(message):
    bot.send_message(message.chat.id,
                     "<b>Часто задаваемые вопросы</b> ❓ \n\n"
                     "<b>Как создавать документы?</b>\n\nВ личном кабинете РЖД в разделе Документы > Создание\nМожно создать:\n"
                     "– уведомление о завершении грузовой операции;\n"
                     "– заявку на перевозку грузов;\n"
                     "– накладную на порожний рейс;– доверенность на вагоны;\n"
                     "– накладную на гружёный рейс.\n"
                     "Также Вы можете подать заявку на оказание услуги из Единого договора в разделе Услуги > Дополнительные > Услуги из единого договора. Узнайте, как подать заявку на нужную Вам услугу, в разделе О кабинете > Инструкция по работе с Личным кабинетом.\n"
                     "Эти и другие функции доступны после регистрации в личном кабинете РЖД.\n\n"
                     "<b>Что мне использовать, личный кабинет РЖД Грузовые перевозки или систему ЭТРАН?</b>\n\nЛичный кабинет РЖД подойдет для компаний, относящихся к сектору малого и среднего предпринимательства, а также для компаний с небольшим или непостоянным грузопотоком.\n"
                     "Выберите удобный вариант перевозки и совершите заказ, воспользуйтесь дополнительными услугами и подайте заявку на отстой или переадресацию вагонов - этот и другой расширенный функционал станет доступен Вам после регистрации в личном кабинете РЖД.РЖД Грузовые перевозки (https://www.rzd.ru/)\n\n"
                     "<b>Как посчитать стоимость перевозки?</b>\n\n"
                     "Вы пожете осуществить примерный расчет стоимости грузоперевозки на сайте личного кабинета РЖД в разделе Калькулятор.\n"
                     "Для выполнения расчетов Вам понадобится указать станции отправления и прибытия груза, наименование груза, род вагона и тд. Если Вы испытываете сложности с определением рода вагона, Вы можете найти соответсвующий вопрос в меню бота.\nhttps://cargolk.rzd.ru/services/calculator",
                     parse_mode='html',
                     reply_markup=keyboard2)


@bot.message_handler(commands=['reset'])
def reset_command(message):
    user.set_cargo_type(message.chat.id, "Не указано")
    user.set_carriage_type(message.chat.id, ["Не определено"])
    user.set_region(message.chat.id, "Не указано")
    user.set_departure_station(message.chat.id, "Не указано")
    bot.send_message(message.chat.id, 'Готово!')
    show_info(message)


@bot.message_handler(commands=['help_cargo'])
def help_cargo_command(message):
    bot.send_message(message.chat.id, "Ссылка на таблицу официальных типов грузов ОАО «РЖД».", reply_markup=keyboard11)


@bot.message_handler(commands=['help_region'])
def help_region_command(message):
    bot.send_message(message.chat.id, "Ссылка на таблицу регионов, обслуживаемых ОАО «РЖД».", reply_markup=keyboard12)


@bot.message_handler(commands=['help_station'])
def help_station_command(message):
    bot.send_message(message.chat.id, "Ссылка на таблицу станций отправления, обслуживаемых ОАО «РЖД».",
                     reply_markup=keyboard12)


@bot.message_handler(commands=['help_rzhd'])
def help_station_command(message):
    bot.send_message(message.chat.id, "Ссылка на таблицу дочерних компаний ОАО «РЖД».",
                     reply_markup=keyboard13)


# Инструкция по регистрации
@bot.callback_query_handler(func=lambda call: call.data == "reg_user")
def reg_user(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(chat_id,
                     "<b>Как зарегестрироваться в личном кабинете?</b>\n"
                     "Для регистрации в личном кабинете:\n"
                     "1. Перейдите на страницу личного кабинета РЖД в раздел Регистрация https://cargolk.rzd.ru/sign_up\n"
                     "2. Выберите способ регистрации без помощи АС ЭТРАН (в этом случае информация о компании автоматически заполнится на основе данных из налоговой службы)\n"
                     "3. Введите ИНН или ЕЛС вашей компании\n"
                     "4. Выберите вашу роль - генеральный директор или менеджер. От этого выбора будет зависеть предоставляемый Вам функционал (генеральный директор имеет полный набор прав, доступны все функции Личного кабинета; менеджер может управлять компанией в ЛК, работать с документами и договорами, имеет права передоверия и последующего передоверия)\n"
                     "5. Для продолжения регистрации Вам необходимо скачать предоставляемые на странице регистрации шаблоны заявления о присоединении к положению об организации расчётов;  информационной справки, содержащей сведения о владельцах контрагента, включая конечных бенефициаров, с приложением подтверждающих документов; доверенности на представление клиента в ЛК (если ваша роль - менеджер)\n"
                     "6. Далее Вам необходимо заполнить информацию о вашей компании, а также ее адрес и ТЦФТО для обслуживания \n"
                     "7. После этого необходимо загрузить документы, указанные в пукте 5 этой инструкции\n"
                     "8. Следующим шагом является заполнение ваших персональных данных\n"
                     "9. Последним является заполнение регистрационных данных, таких как логин и пароль.\n\n"
                     "После выполнения этих шагов ваша заявка должна поступить в систему. Учтите, что после регистрации Вам будут выданы реквизиты и счет на оплату в размере 100 рублей, который необходимо будет оплатить от имени вашей компании. После оплаты просиходит подтверждение того, что Вы действительно являетесь гениральным директором или менеджером регистрируемой компании. В будущем данные средства можно будет использовать для оплаты платных услуг.\n\n"
                     "Надеюсь я Вам помог 😊",
                     parse_mode='html',
                     reply_markup=keyboard2)


# Часто задаваемые вопросы
@bot.callback_query_handler(func=lambda call: call.data == "questions")
def questions(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(chat_id,
                     "<b>Часто задаваемые вопросы</b> ❓ \n\n"
                     "<b>Как создавать документы?</b>\n\nВ личном кабинете РЖД в разделе Документы > Создание\nМожно создать:\n"
                     "– уведомление о завершении грузовой операции;\n"
                     "– заявку на перевозку грузов;\n"
                     "– накладную на порожний рейс;– доверенность на вагоны;\n"
                     "– накладную на гружёный рейс.\n"
                     "Также Вы можете подать заявку на оказание услуги из Единого договора в разделе Услуги > Дополнительные > Услуги из единого договора. Узнайте, как подать заявку на нужную Вам услугу, в разделе О кабинете > Инструкция по работе с Личным кабинетом.\n"
                     "Эти и другие функции доступны после регистрации в личном кабинете РЖД.\n\n"
                     "<b>Что мне использовать, личный кабинет РЖД Грузовые перевозки или систему ЭТРАН?</b>\n\nЛичный кабинет РЖД подойдет для компаний, относящихся к сектору малого и среднего предпринимательства, а также для компаний с небольшим или непостоянным грузопотоком.\n"
                     "Выберите удобный вариант перевозки и совершите заказ, воспользуйтесь дополнительными услугами и подайте заявку на отстой или переадресацию вагонов - этот и другой расширенный функционал станет доступен Вам после регистрации в личном кабинете РЖД.РЖД Грузовые перевозки: https://www.rzd.ru/\n\n"
                     "<b>Как посчитать стоимость перевозки?</b>\n\n"
                     "Вы пожете осуществить примерный расчет стоимости грузоперевозки на сайте личного кабинета РЖД в разделе Калькулятор.\n"
                     "Для выполнения расчетов Вам понадобится указать станции отправления и прибытия груза, наименование груза, род вагона и тд. Если Вы испытываете сложности с определением рода вагона, Вы можете найти соответсвующий вопрос в меню бота.\nhttps://cargolk.rzd.ru/services/calculator",
                     parse_mode='html',
                     reply_markup=keyboard2)


@bot.callback_query_handler(func=lambda call: call.data == "set_data")
def set_data(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    if user.get_cargo_type(message.chat.id) == "Не указано":
        ask_cargo_type(message)
        return
    elif user.get_region(message.chat.id) == "Не указано":
        ask_region(message)
        return
    elif user.get_departure_station(message.chat.id) == "Не указано":
        ask_station(message)
        return
    else:
        show_info(message, keyboard6)


@bot.callback_query_handler(func=lambda call: call.data == "edit_cargo")
def edit_cargo(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    show_info(call.message, empty_kb)
    ask_cargo_type(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "edit_region")
def edit_region(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    show_info(call.message, empty_kb)
    ask_region(call.message)
    reset_station(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "edit_station")
def edit_station(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    show_info(call.message, empty_kb)
    ask_station(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "edit")
def edit_data(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    show_info(call.message, keyboard6)


@bot.callback_query_handler(func=lambda call: call.data == "det_transp")
def determinate(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    determine_transportation(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "reset")
def reset(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    user.set_cargo_type(message.chat.id, "Не указано")
    user.set_carriage_type(message.chat.id, ["Не определено"])
    user.set_region(message.chat.id, "Не указано")
    user.set_departure_station(message.chat.id, "Не указано")
    bot.send_message(call.message.chat.id, 'Готово! Данные сброшены.')
    show_info(call.message)


@bot.message_handler(content_types=['photo', 'audio', 'video'])
def get_visual(message):
    bot.reply_to(message,
                 'Я не умею распознавать такое. Но я попробую...\n\nВы прислали мне что-то интересное!')


# Пользователь подтвердил требуемую грузоперевозку: с услугами хранения
@bot.callback_query_handler(func=lambda call: call.data == "yes_step1")
def yes_step1(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id - 1)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Я знаю что Вам подойдёт!')
    # Выводим результат: с услугами хранения
    storage_services(call.message)


# Спрашиваем про мелкую партию грузоперевозки
@bot.callback_query_handler(func=lambda call: call.data == "no_step1")
def no_step1(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(chat_id=chat_id,
                     text='Хорошо, быть может...\n\nВам требуется перевозка мелкой партии груза (до 1 тонны)?',
                     reply_markup=keyboard8)


# Пользователь подтвердил требуемую грузоперевозку: мелкая партия груза
@bot.callback_query_handler(func=lambda call: call.data == "yes_step2")
def yes_step2(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Я знаю что Вам подойдёт!')
    small_cargo(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "no_step2")
def no_step2(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.delete_message(chat_id=chat_id, message_id=message_id)
    bot.send_message(chat_id=chat_id,
                     text='Странно... Хотя! А, забудьте...\nНо давайте попробуем.\n\nВам требуется совершать '
                          'международные перевозки?',
                     reply_markup=keyboard9)


@bot.callback_query_handler(func=lambda call: call.data == "yes_step3")
def yes_step3(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Я знаю что Вам подойдёт!')
    international_transportation(message)


@bot.callback_query_handler(func=lambda call: call.data == "no_step3")
def no_step3(call: types.CallbackQuery):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Я знаю что Вам подойдёт!')
    if user.get_cargo_type(message.chat.id) == "Не указано":
        bot.send_message(call.message.chat.id,
                         'При выборе внутренних перевозок мне очень важно знать небольшую информацию.\nПожалуйста, '
                         'помогите мне и я помогу Вам!')
        det_ask_cargo_type(call.message)
        return
    elif user.get_region(message.chat.id) == "Не указано":
        bot.send_message(call.message.chat.id,
                         'При выборе внутренних перевозок мне очень важно знать небольшую информацию.\nПожалуйста, '
                         'помогите мне и я помогу Вам!')
        det_ask_region(call.message)
        return
    elif user.get_departure_station(message.chat.id) == "Не указано":
        bot.send_message(call.message.chat.id,
                         'При выборе внутренних перевозок мне очень важно знать небольшую информацию.\nПожалуйста, '
                         'помогите мне и я помогу Вам!')
        det_ask_station(call.message)
    else:
        domestic_transportation(call.message)


@bot.message_handler(content_types=['text'])
def text_analys(message):
    if message.text == "Определить тип перевозки":
        determine_transportation(message)
    elif message.text == "Внутренние перевозки":
        domestic_transportation(message)
    elif message.text == "Международные перевозки":
        international_transportation(message)
    elif message.text == "С услугами хранения":
        storage_services(message)
    elif message.text == "Мелкая партия":
        small_cargo(message)
    else:
        bot.send_message(message.chat.id,
                         'Я не чат gpt, и у меня не получается распознавать сложный текст.\nНо Вы можете выбрать нужную кнопку, и я обязательно покажу, что умею!')


def text_format(input):
    text = input.lower().strip()
    res = text[0].upper() + text[1:]
    return res


# Определить тип грузоперевозки
def determine_transportation(message):
    bot.send_message(message.chat.id,
                     'Отлично, я Вам помогу!\n\nЯ буду задавать Вам простые вопросы Да/Нет формата для того чтобы '
                     'помочь определиться!')
    bot.send_message(message.chat.id,
                     f'Для начала давайте поймём...\n\nВам требуется контейнерная перевозка с условиями хранения?',
                     reply_markup=keyboard7)


def domestic_transportation(message):
    if user.get_cargo_type(message.chat.id) == "Не указано":
        bot.send_message(message.chat.id,
                         text=f'Для начала укажите ваш тип груза!')
        ask_cargo_type(message)
        return

    elif user.get_region(message.chat.id) == "Не указано":
        bot.send_message(message.chat.id,
                         text=f'Для начала укажите ваш регион!')
        ask_region(message)
        return

    elif user.get_departure_station(message.chat.id) == "Не указано":
        bot.send_message(message.chat.id,
                         text=f'Для начала укажите вашу станцию отправления!')
        ask_station(message)
        return
    else:
        pass

    code_station = 0
    table_name = 'code_station.sqlite3'
    conn1 = sqlite3.connect(table_name)
    try:
        print(f"Соединение с {table_name} открыто")
        cur1 = conn1.cursor()
        cur1.execute(
            f"SELECT id FROM codes WHERE station LIKE '%{user.get_departure_station(message.chat.id).upper()}%' AND region LIKE '%{user.get_region(message.chat.id)}%'")
        res1 = cur1.fetchall()
        if not res1:
            bot.send_message(message.chat.id,
                             f"УПС!\nВидимо Ваши данные были неправильно введены, здесь я бессилен.")
            back_to_menu(message)
            return
        else:
            for r in res1:
                code_station = r[0]
        conn1.commit()
        cur1.close()
        conn1.close()

    except sqlite3.Error as error:
        print(f"Ошибка при работе с {table_name}", error)
    finally:
        if conn1:
            conn1.close()
            print("fСоединение с {table_name} закрыто")

    table_name = 'filials.sqlite3'
    conn = sqlite3.connect(table_name)
    try:
        print(f"Соединение с {table_name} открыто")
        cur = conn.cursor()
        temp = user.get_carriage_type(message.chat.id)
        for i in range(len(temp)):
            carriage = temp[i]
            cur.execute(
                f"SELECT name, contatcts, address, region FROM filials WHERE region LIKE '%{user.get_region(message.chat.id)}%' AND "
                f"station LIKE '%{code_station}%' AND carriage LIKE '%{carriage}%'")
        res = cur.fetchall()

        if not res:
            bot.send_message(message.chat.id,
                             f"Я не смог найти подходящую компанию :(\n\nПопробуйте открыть таблицу и посмотреть, "
                             f"какие контакты могут Вам подойти. Воспользуйтесь командой /help_rzhd.\nТакже "
                             f"попробуйте заново ввести данные!")
            back_to_menu(message)
            return
        else:
            bot.send_message(message.chat.id,
                             f'Вы указали интересующий Вас тип грузоперевоки:\n<b><u>Внутренние '
                             f'перевозки</u></b>\n\nИнтересующий Вас тип груза: <b><u>'
                             f'{user.get_cargo_type(message.chat.id)}</u></b>\nПодходящий тип вагона: <b><u>'
                             f'{user.show_carriage_type(message.chat.id)}</u></b>\nРегион: <b><u>{user.get_region(message.chat.id)}</u></b>\nСтанция '
                             f'отправки: <b><u>{user.get_departure_station(message.chat.id)}</u></b>\n\nВнутренними перевозками '
                             f'занимаются:',
                             parse_mode='html')
            for r in res:
                bot.send_message(message.chat.id,
                                 f'{r[0]}\nКонтактные данные: {r[1]}\nАдрес: {r[2]}\nОбласти компетенции: {r[3]}',
                                 parse_mode='html')
            bot.send_message(message.chat.id,
                             f'Надеюсь я был полезен для вас!',
                             parse_mode='html',
                             reply_markup=keyboard2)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print(f"Ошибка при работе с {table_name}", error)
    finally:
        if conn:
            conn.close()
            print(f"Соединение с {table_name} закрыто")


def storage_services(message):
    bot.send_message(message.chat.id,
                     f'Вы указали интересующий Вас тип грузоперевоки:\n<b><u>С услугами '
                     f'хранения</u></b>\n\nИнтересующий Вас тип груза: <b><u>{user.get_cargo_type(message.chat.id)}</u></b>\nПодходящий '
                     f'тип вагона: <b><u>{user.show_carriage_type(message.chat.id)}</u></b>\nРегион: <b><u>'
                     f'{user.get_region(message.chat.id)}</u></b>\nСтанция отправки: <b><u>{user.get_departure_station(message.chat.id)}</u></b>\n\nПеревозками '
                     f'с услугами хранения занимается:\nОАО «РЖД Бизнес-Актив»\nСайт: '
                     f'<u>https://rzdba.ru/</u>\nКонтактный телефон: <u>+7(495)161-78-78</u>, '
                     f'<u>+7(495)161-81-81</u>\nАдрес: г.Москва, ул.Ольховская д.4, к.2\nОбласти компетенции: '
                     f'внутренние перевозки Россия, Китай, Европа\n\nОбратитесь к ним, и они наверняка удивятся, '
                     f'что Вы сразу их нашли!',
                     parse_mode='html',
                     reply_markup=keyboard2)


def small_cargo(message):
    bot.send_message(message.chat.id,
                     f'Вы указали интересующий Вас тип грузоперевоки:\n<b><u>Мелкая партия '
                     f'груза</u></b>\n\nИнтересующий Вас тип груза: <b><u>{user.get_cargo_type(message.chat.id)}</u></b>\nПодходящий тип '
                     f'вагона: <b><u>{user.show_carriage_type(message.chat.id)}</u></b>\nРегион: <b><u>'
                     f'{user.get_region(message.chat.id)}</u></b>\nСтанция отправки: <b><u>{user.get_departure_station(message.chat.id)}</u></b>\n\nМелкими '
                     f'партиями груза занимается:\nОАО «РЖД Логистика»\nСайт: <u>https://rzdlog.ru/</u>\nКонтактный '
                     f'телефон: <u>+7(499)369-60-74</u>, <u>+7(495)988-68-68</u>\nАдрес: г.Москва ул. Маши Порываевой '
                     f'д. 34.\nОбласти компетенции: внутренние перевозки Россия, страны СНГ, страны Балтии, Европа, '
                     f'коридоры "Восток-Запад" и "Север-Юг"\n\nОбратитесь к ним, и они наверняка удивятся, '
                     f'что Вы сразу их нашли!',
                     parse_mode='html',
                     reply_markup=keyboard2)


def international_transportation(message):
    bot.send_message(message.chat.id,
                     f'Вы указали интересующий Вас тип грузоперевоки:\n<b><u>Международные '
                     f'перевозки</u></b>\n\nИнтересующий Вас тип груза: <b><u>{user.get_cargo_type(message.chat.id)}</u></b>\nПодходящий '
                     f'тип вагона: <b><u>{user.show_carriage_type(message.chat.id)}</u></b>\nРегион: <b><u>'
                     f'{user.get_region(message.chat.id)}</u></b>\nСтанция отправки: <b><u>'
                     f'{user.get_departure_station(message.chat.id)}</u></b>\n\nМеждународными перевозками занимается:\nОАО «РЖД '
                     f'Логистика»\nСайт: <u>https://rzdlog.ru/</u>\nКонтактный телефон: <u>+7(499)369-60-74</u>, '
                     f'<u>+7(495)988-68-68</u>\nАдрес: г.Москва ул. Маши Порываевой д. 34.\nОбласти компетенции: '
                     f'внутренние перевозки Россия, страны СНГ, страны Балтии, Европа, коридоры "Восток-Запад" и '
                     f'"Север-Юг"\n\nОАО «РЖД Бизнес-Актив»\nСайт: <u>https://rzdba.ru/</u>\nКонтактный телефон: '
                     f'<u>+7(495)161-78-78</u>, <u>+7(495)161-81-81</u>\nАдрес: г.Москва, ул.Ольховская д.4, '
                     f'к.2\nОбласти компетенции: внутренние перевозки Россия, Китай, Европа\n\nОбратитесь к ним, '
                     f'и они наверняка удивятся, что Вы сразу их нашли!',
                     parse_mode='html',
                     reply_markup=keyboard2)


def reset_station(message):
    user.set_departure_station(message.chat.id, "Не указано")


def ask_cargo_type(message):
    bot.send_message(message.chat.id,
                     f'🚋 Вы находитесь в функции запроса типа груза.')
    show_info(message, empty_kb)
    bot.send_message(message.chat.id,
                     f'Укажите тип груза для перевозки.\nВажно! Указывайте текст такой, чтобы его было проще всего '
                     f'найти по совпадению!\n\nЕсли у Вас возникли трудности воспользуйтесь командой /help_cargo.')
    bot.register_next_step_handler(message, get_cargo_type)


def get_cargo_type(message):
    cargo_type = text_format(message.text.strip())
    if cargo_type == "Определить тип перевозки":
        determine_transportation(message)
        return
    elif cargo_type == "Внутренние перевозки":
        domestic_transportation(message)
        return
    elif cargo_type == "Международные перевозки":
        international_transportation(message)
        return
    elif cargo_type == "С услугами хранения":
        storage_services(message)
        return
    elif cargo_type == "Мелкая партия":
        small_cargo(message)
        return
    else:
        pass

    bot.send_message(chat_id=message.chat.id, text=f"Вы ввели: {message.text.strip()}.")

    table_name = 'cargo.sqlite3'
    conn = sqlite3.connect(table_name)
    try:
        print(f"Соединение с {table_name} открыто")
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM cargo WHERE cargo_type LIKE '%{cargo_type}%'")
        res = cur.fetchall()

        if not res:
            bot.send_message(message.chat.id,
                             f"Я не смог найти интересующий Вас тип груза :(\n\nПопробуйте открыть таблицу и "
                             f"посмотреть, какие типы грузов у нас имеются. Воспользуйтесь командой /help_cargo.")
            back_to_menu(message)
            return
        else:
            carriage = []
            cargo = ''
            for r in res:
                cargo = r[0]
            for r in res:
                if r[0] == cargo:
                    carriage.append(r[1])
            user.set_cargo_type(message.chat.id, cargo)
            user.set_carriage_type(message.chat.id, carriage)
            bot.send_message(message.chat.id, f"Я нашёл интересующий Вас тип груза! Это: {cargo}.")
            show_info(message)
        conn.commit()
        cur.close()
        conn.close()
    except sqlite3.Error as error:
        print(f"Ошибка при работе с {table_name}", error)
    finally:
        if conn:
            conn.close()
            print(f"Соединение с {table_name} закрыто")


def ask_region(message):
    bot.send_message(message.chat.id,
                     f'📞 Вы находитесь в функции запроса региона.')
    show_info(message, empty_kb)
    bot.send_message(message.chat.id,
                     text=f'Укажите интересующий Вас регион.\n\nВажно! Указывайте текст такой, чтобы его было проще '
                          f'всего найти по совпадению\n\nЕсли у Вас возникли трудности воспользуйтесь командой '
                          f'/help_region!')
    bot.register_next_step_handler(message, get_region)


def get_region(message):
    region = text_format(message.text.strip())
    if region == "Определить тип перевозки":
        determine_transportation(message)
        return
    elif region == "Внутренние перевозки":
        domestic_transportation(message)
        return
    elif region == "Международные перевозки":
        international_transportation(message)
        return
    elif region == "С услугами хранения":
        storage_services(message)
        return
    elif region == "Мелкая партия":
        small_cargo(message)
        return
    else:
        pass

    bot.send_message(chat_id=message.chat.id, text=f"Вы ввели: {message.text.strip()}.")

    table_name = 'stations.sqlite3'
    conn = sqlite3.connect(table_name)
    try:
        print(f"Соединение с {table_name} открыто")
        cur = conn.cursor()
        cur.execute(
            f"SELECT region FROM stations WHERE region_lower LIKE '%{region.lower()}%'")
        res = cur.fetchall()

        if not res:
            bot.send_message(message.chat.id,
                             f"Я не смог найти ваш регион :(\n\nПопробуйте открыть таблицу и посмотреть, какие регионы "
                             f"обслуживает ОАО «РЖД». Воспользуйтесь командой /help_region!")
            back_to_menu(message)
            return
        else:
            region = res[0][0]
            user.set_region(message.chat.id, region)
            bot.send_message(message.chat.id, f"Я нашёл ваш регион! Это: {region}.")
            show_info(message)
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print(f"Ошибка при работе с {table_name}", error)
    finally:
        if conn:
            conn.close()
            print(f"Соединение с {table_name} закрыто")


def ask_station(message):
    bot.send_message(message.chat.id,
                     f'🚩 Вы находитесь в функции запроса станции отправления.')
    show_info(message, empty_kb)
    bot.send_message(message.chat.id,
                     text=f'Укажите интересующую Вас станцию отправления.\n\nВажно! Указывайте текст такой, чтобы его '
                          f'было проще всего найти по совпадению\n\nЕсли у Вас возникли трудности воспользуйтесь '
                          f'командой /help_station!')
    bot.register_next_step_handler(message, get_station)


def get_station(message):
    station = text_format(message.text.strip())
    if user.get_region(message.chat.id) == "Не указано":
        bot.send_message(message.chat.id,
                         text=f'Для начала укажите ваш регион!')
        ask_region(message)
        return
    else:
        if station == "Определить тип перевозки":
            determine_transportation(message)
            return
        elif station == "Внутренние перевозки":
            domestic_transportation(message)
            return
        elif station == "Международные перевозки":
            international_transportation(message)
            return
        elif station == "С услугами хранения":
            storage_services(message)
            return
        elif station == "Мелкая партия":
            small_cargo(message)
            return
        else:
            pass

        bot.send_message(chat_id=message.chat.id, text=f"Вы ввели: {message.text.strip()}.")

        table_name = 'stations.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто")
            cur = conn.cursor()
            cur.execute(
                f"SELECT station FROM stations WHERE station LIKE '%{station}%' AND region LIKE '%{user.get_region(message.chat.id)}%'")
            res = cur.fetchall()

            if not res:
                bot.send_message(message.chat.id,
                                 f"Я не смог найти вашу станцию отправления :(\n\nПопробуйте открыть таблицу и "
                                 f"посмотреть, какие станции отправления находятся в вашем регионе. Воспользуйтесь "
                                 f"командой /help_station.")
                back_to_menu(message)
                return
            else:
                st = res[0][0]
                user.set_departure_station(message.chat.id, st)
                bot.send_message(message.chat.id, f"Я нашёл вашу станцию отправки! Это: {st}.")
                show_info(message)
            conn.commit()
            cur.close()
            conn.close()

        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто")


def det_ask_cargo_type(message):
    bot.send_message(message.chat.id,
                     f'🚋 Вы находитесь в функции запроса типа груза.')
    show_info(message, empty_kb)
    bot.send_message(message.chat.id,
                     f'Укажите тип груза для перевозки.\nВажно! Указывайте текст такой, чтобы его было проще всего '
                     f'найти по совпадению!\n\nЕсли у Вас возникли трудности воспользуйтесь командой /help_cargo.')
    bot.register_next_step_handler(message, det_get_cargo_type)


def det_get_cargo_type(message):
    cargo_type = text_format(message.text.strip())
    if cargo_type == "Определить тип перевозки":
        determine_transportation(message)
        return
    elif cargo_type == "Внутренние перевозки":
        domestic_transportation(message)
        return
    elif cargo_type == "Международные перевозки":
        international_transportation(message)
        return
    elif cargo_type == "С услугами хранения":
        storage_services(message)
        return
    elif cargo_type == "Мелкая партия":
        small_cargo(message)
        return
    else:
        pass

    bot.send_message(chat_id=message.chat.id, text=f"Вы ввели: {message.text.strip()}.")

    table_name = 'cargo.sqlite3'
    conn = sqlite3.connect(table_name)
    try:
        print(f"Соединение с {table_name} открыто")
        cur = conn.cursor()
        cur.execute(
            f"SELECT * FROM cargo WHERE cargo_type LIKE '%{cargo_type}%'")
        res = cur.fetchall()

        if not res:
            bot.send_message(message.chat.id,
                             f"Я не смог найти интересующий Вас тип груза :(\n\nПопробуйте открыть таблицу и "
                             f"посмотреть, какие типы грузов у нас имеются. Воспользуйтесь командой /help_cargo.")
            back_to_menu(message)
            return
        else:
            carriage = []
            cargo = ''
            for r in res:
                cargo = r[0]
            for r in res:
                if r[0] == cargo:
                    carriage.append(r[1])
            user.set_cargo_type(message.chat.id, cargo)
            user.set_carriage_type(message.chat.id, carriage)
            bot.send_message(message.chat.id, f"Я нашёл интересующий Вас тип груза! Это: {cargo}.")
        conn.commit()
        cur.close()
        conn.close()
    except sqlite3.Error as error:
        print(f"Ошибка при работе с {table_name}", error)
    finally:
        if conn:
            conn.close()
            print(f"Соединение с {table_name} закрыто")
    if user.get_region(message.chat.id) == "Не указано":
        det_ask_region(message)
    elif user.get_departure_station(message.chat.id) == "Не указано":
        det_ask_station(message)
    else:
        domestic_transportation(message)


def det_ask_region(message):
    bot.send_message(message.chat.id,
                     f'📞 Вы находитесь в функции запроса региона.')
    show_info(message, empty_kb)
    bot.send_message(message.chat.id,
                     text=f'Укажите интересующий Вас регион.\n\nВажно! Указывайте текст такой, чтобы его было проще '
                          f'всего найти по совпадению\n\nЕсли у Вас возникли трудности воспользуйтесь командой '
                          f'/help_region!')
    bot.register_next_step_handler(message, det_get_region)


def det_get_region(message):
    region = text_format(message.text.strip())
    if region == "Определить тип перевозки":
        determine_transportation(message)
        return
    elif region == "Внутренние перевозки":
        domestic_transportation(message)
        return
    elif region == "Международные перевозки":
        international_transportation(message)
        return
    elif region == "С услугами хранения":
        storage_services(message)
        return
    elif region == "Мелкая партия":
        small_cargo(message)
        return
    else:
        pass

    bot.send_message(chat_id=message.chat.id, text=f"Вы ввели: {message.text.strip()}.")

    table_name = 'stations.sqlite3'
    conn = sqlite3.connect(table_name)
    try:
        print(f"Соединение с {table_name} открыто")
        cur = conn.cursor()
        cur.execute(
            f"SELECT region FROM stations WHERE region_lower LIKE '%{region.lower()}%'")
        res = cur.fetchall()

        if not res:
            bot.send_message(message.chat.id,
                             f"Я не смог найти ваш регион :(\n\nПопробуйте открыть таблицу и посмотреть, какие регионы "
                             f"обслуживает ОАО «РЖД». Воспользуйтесь командой /help_region!")
            back_to_menu(message)
            return
        else:
            region = res[0][0]
            user.set_region(message.chat.id, region)
            bot.send_message(message.chat.id, f"Я нашёл ваш регион! Это: {region}.")
        conn.commit()
        cur.close()
        conn.close()

    except sqlite3.Error as error:
        print(f"Ошибка при работе с {table_name}", error)
    finally:
        if conn:
            conn.close()
            print(f"Соединение с {table_name} закрыто")
    if user.get_cargo_type(message.chat.id) == "Не указано":
        det_ask_region(message)
    elif user.get_departure_station(message.chat.id) == "Не указано":
        det_ask_station(message)
    else:
        domestic_transportation(message)


def det_ask_station(message):
    bot.send_message(message.chat.id,
                     f'🚩 Вы находитесь в функции запроса станции отправления.')
    show_info(message, empty_kb)
    bot.send_message(message.chat.id,
                     text=f'Укажите интересующую Вас станцию отправления.\n\nВажно! Указывайте текст такой, чтобы его '
                          f'было проще всего найти по совпадению\n\nЕсли у Вас возникли трудности воспользуйтесь '
                          f'командой /help_station.')
    bot.register_next_step_handler(message, det_get_station)


def det_get_station(message):
    station = text_format(message.text.strip())
    if user.get_region(message.chat.id) == "Не указано":
        bot.send_message(message.chat.id,
                         text=f'Для начала укажите ваш регион!')
        ask_region(message)
        return
    else:
        if station == "Определить тип перевозки":
            determine_transportation(message)
            return
        elif station == "Внутренние перевозки":
            domestic_transportation(message)
            return
        elif station == "Международные перевозки":
            international_transportation(message)
            return
        elif station == "С услугами хранения":
            storage_services(message)
            return
        elif station == "Мелкая партия":
            small_cargo(message)
            return
        else:
            pass

        bot.send_message(chat_id=message.chat.id, text=f"Вы ввели: {message.text.strip()}.")

        table_name = 'stations.sqlite3'
        conn = sqlite3.connect(table_name)
        try:
            print(f"Соединение с {table_name} открыто")
            cur = conn.cursor()
            cur.execute(
                f"SELECT station FROM stations WHERE station LIKE '%{station}%' AND region LIKE '%{user.get_region(message.chat.id)}%'")
            res = cur.fetchall()

            if not res:
                bot.send_message(message.chat.id,
                                 f"Я не смог найти вашу станцию отправления :(\n\nПопробуйте открыть таблицу и "
                                 f"посмотреть, какие станции отправления находятся в вашем регионе. Воспользуйтесь "
                                 f"командой /help_station.")
                back_to_menu(message)
                return
            else:
                st = res[0][0]
                user.set_departure_station(message.chat.id, st)
                bot.send_message(message.chat.id, f"Я нашёл вашу станцию отправки! Это: {st}.")
            conn.commit()
            cur.close()
            conn.close()

        except sqlite3.Error as error:
            print(f"Ошибка при работе с {table_name}", error)
        finally:
            if conn:
                conn.close()
                print(f"Соединение с {table_name} закрыто")
    if user.get_cargo_type(message.chat.id) == "Не указано":
        det_ask_cargo_type(message)
    else:
        domestic_transportation(message)


if __name__ == "__main__":
    print("Bot is started")
    while True:
        try:
            # Запуск бота
            bot.polling(skip_pending=True, none_stop=True)

        except Exception as e:
            print(e)
            # или import traceback; traceback.print_exc() для печати полной инфы
            time.sleep(15)
