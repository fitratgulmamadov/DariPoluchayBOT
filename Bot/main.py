import telebot
import requests
from datetime import datetime
from main_menu import *


bot = telebot.TeleBot("6376269844:AAGm3OJrNP8krIetlXPyR2ju7OSi8KpKHBk")

# SERVER CONFIG
server_config = 'http://127.0.0.1:8003/botconf/'
server_data = 'http://127.0.0.1:8003/main/'

restore_template = {
	'username': None,
	'password': None,
	'ch_id': None
} 


tmp_dict = {

}

status_dict = {
	'R': '🔴',
	'G': '🟢',
	'W': '⚪️',
	'V': '🤡',
}


# MENU
main_menu_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_markup.row_width = 2
menu_namespace_arr = ['🫶 О нас', '📋 Мои доски', '👋 Приглашение', '🔰 Мой статус', '⚡️ Срочная отправка', '🔒 Данные для восстановления']#, '🧠 Академия Знаний «Дари > Получай»']
main_menu_markup.add(*[telebot.types.KeyboardButton(i) for i in menu_namespace_arr])

# RESTORE ACCAUNT
@bot.message_handler(commands=['restore'])
def command_manager_restore(message):
	msg = bot.reply_to(message, '👤 Введите логин восстановления ( @test )')
	tmp_dict[message.chat.id] = restore_template.copy()
	bot.register_next_step_handler(msg, get_username_password)

def get_username_password(message):
	tmp_dict[message.chat.id]['username'] = message.text
	msg = bot.reply_to(message, '🔒 Введите пароль восстановления')
	bot.register_next_step_handler(msg, get_password_check)

def get_password_check(message):
	tmp_dict[message.chat.id]['password'] = message.text
	try:
		ch_id = int(message.text, 16)
	except:
		ch_id = 5456
	usr = requests.get(server_data + f'tgusers/{ch_id}/')
	# print('dsac', usr, tmp_dict[message.chat.id], usr.json()['link'])
	if 200 <= usr.status_code < 400 and usr.json()['link'] == tmp_dict[message.chat.id]['username']:
		user = usr.json()
		payload = {
			"id": user['id'],
			"name": user['name'],
			"ch_id": message.chat.id,
			"join_date": user['join_date'],
			"link": f'@{message.chat.username}',
			"status": user['status'],
			"board": user['board']['id']
		}
		responce = requests.put(server_data + f'tgusers/{int(message.text, 16)}/', data=payload)
		print(responce.json())
		if 200 <= responce.status_code < 400:
			bot.reply_to(message, new_on_register_login_get % (f"{responce.json()['link']}", hex(responce.json()['ch_id'])))
			
		else:
			bot.reply_to(message, '😢 Ой что-то пошло не так ...')
	else:
		markup = telebot.types.InlineKeyboardMarkup()
		markup_list = [
			{'name': '✅ Yes', 'callback': 'yes_try_again'},
			{'name': '❌ No', 'callback': 'no_try_again'},
		]
		markup.row_width = 2
		markup.add(*[telebot.types.InlineKeyboardButton(i['name'], callback_data=i['callback']) for i in markup_list ])
		bot.send_message(message.chat.id, '😫 Неверный пароль или логин, повторить?', reply_markup=markup)

	tmp_dict.pop(message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == 'yes_try_again')
def call_restore_yes(call):
	msg = bot.reply_to(call.message, '👤 Введите логин восстановления ( @test )')
	tmp_dict[call.message.chat.id] = restore_template.copy()
	bot.register_next_step_handler(msg, get_username_password)

# RESTORE ACCAUNT #


# COMMAND AND REF. LINK
@bot.message_handler(commands=['start', 'help'])
def command_manager(message):
	exist_usr = requests.get(server_data + f'tgusers/{message.chat.id}/')


	if 200 <= exist_usr.status_code < 400 and exist_usr.json()['status']:
		bot.send_message(message.chat.id, requests.get(server_config + 'helps/start/').json()['text'], reply_markup=main_menu_markup)
		
		presents = requests.get(server_data + f'presents/?from_user__ch_id={message.chat.id}&status={True}').json()
		if len(presents) == 0:
			bot.send_message(message.chat.id, kick_after_3h, parse_mode='HTML')
	else:
		if 'ref' in message.text:
			sp_ref = message.text.split(' ')[1]
			print(sp_ref)
			valid_ref = requests.get(server_data + f'reflinks/?url=https://t.me/royal_capital_bot?start={sp_ref}').json()
			if len(valid_ref):
				success_del = delete_ref(valid_ref[0]['tguser']['ch_id'])
				if 200 <= success_del.status_code < 400:
					new_user = register_user(message).json()
					bot.send_message(message.chat.id, on_register_login_get % (new_user['link'], hex(new_user['ch_id'])))

					presents = requests.get(server_data + f'presents/?from_user__ch_id={message.chat.id}&status={True}').json()
					if len(presents) == 0:
						bot.send_message(message.chat.id, kick_after_3h, parse_mode='HTML')
					
					bot.send_message(message.chat.id, requests.get(server_config + 'helps/start/').json()['text'], reply_markup=main_menu_markup)
				else:
					bot.reply_to(message, invalid_ref)
			else:
				bot.reply_to(message, invalid_ref)
		else:
			bot.reply_to(message, requests.get(server_config + 'helps/no_ref/').json()['text'])	



		# bot.reply_to(message, requests.get(server_config + 'helps/no_ref/').json()['text'], reply_markup=telebot.types.ReplyKeyboardRemove())


def delete_ref(ch_id):
	print('ref_del')
	return requests.delete(server_data + f'reflinks/{ch_id}/')


def register_user(message):
	first_board = requests.get(server_data + 'boards/?state=1').json()[0]

	payload = {
		"name": f'{message.chat.first_name}  {message.chat.last_name}',
		"ch_id": message.chat.id,
		"link": f"@{message.chat.username}",
		"status": 'W',
		"board": first_board['id']
	}

	return requests.post(server_data + 'tgusers/', data=payload)



# MESSAGES FROM KEYBOARD-INLINE-MARKUP 


# ⚡️ Срочная отправка
@bot.message_handler(func=lambda message: message.text == '⚡️ Срочная отправка')
def fast_send(message):
	info = requests.get(server_config + 'helpsmedia/before_send_board/').json()
	user = requests.get(server_data + f'tgusers/{message.chat.id}/').json()
	passed_boards = requests.get(server_data + f'passedboards/?tguser__ch_id={message.chat.id}').json()
	board = user['board']['name']
	img = requests.get(user['board']['img']).content

	all_users_sorted_w = len(requests.get(server_data + f'tgusers/?board__name={user["board"]["name"]}&status=W').json())


	markup = telebot.types.InlineKeyboardMarkup()
	markup.row_width = 1
	markup.add(*[telebot.types.InlineKeyboardButton(i, callback_data=str(i)) for i in ['⚜️ Данные получателя']])

	bot.send_photo(message.chat.id, img, caption=info['text'] % (board, all_users_sorted_w, status_dict[user['status']], len(passed_boards)), reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🔒 Данные для восстановления')
def restore_data(message):
	usr = requests.get(server_data + f'tgusers/{message.chat.id}/')
	
	if 200 <= usr.status_code < 400:
		user = usr.json()
		bot.reply_to(message, on_register_login_get % ((f"{user['link']}", hex(user['ch_id']))))
	else:
		bot.reply_to(message, requests.get(server_config + 'helps/no_ref/').json()['text'])	




# 🔰 Мой статус
@bot.message_handler(func=lambda message: message.text == '🔰 Мой статус')
def my_status(message):
	user = requests.get(server_data + f'tgusers/{message.chat.id}/')

	if 200 <= user.status_code < 400:
		presents_sent = requests.get(server_data + f'presents/?from_user__ch_id={message.chat.id}&status={True}').json()
		presents_rcv = requests.get(server_data + f'presents/?to_user__ch_id={message.chat.id}&status={True}').json()
		presents_sent_board = requests.get(server_data + f'presents/?from_user__ch_id={message.chat.id}&status={True}&board__id={user.json()["board"]["id"]}').json()
		presents_rcv_board = requests.get(server_data + f'presents/?to_user__ch_id={message.chat.id}&status={True}&board__id={user.json()["board"]["id"]}').json()
		usr = user.json()
		all_users_sorted_w = requests.get(server_data + f'tgusers/?board__name={usr["board"]["name"]}&status=W').json()
		all_users_sorted_g = requests.get(server_data + f'tgusers/?board__name={usr["board"]["name"]}&status=G').json()
		my_pos_arr = requests.get(server_data + f'tgusers/?board__name={usr["board"]["name"]}&status={usr["status"]}').json()
		
		bot.reply_to(message, my_status12 % (usr['board']['name'], status_dict[usr['status']], len(presents_rcv_board), len(presents_sent_board), len(presents_rcv), len(presents_sent), len(all_users_sorted_g), len(all_users_sorted_w), my_pos_arr.index(usr)+1))

		presents = requests.get(server_data + f'presents/?from_user__ch_id={message.chat.id}&status={True}').json()
		if len(presents) == 0:
			bot.send_message(message.chat.id, kick_after_3h, parse_mode='HTML')

	else:
		bot.reply_to(message, requests.get(server_config + 'helps/no_ref/').json()['text'])	


# 📋 Мои доски
@bot.message_handler(func=lambda message: message.text == '📋 Мои доски')
def keyboard_manager3(message):
	all_users = requests.get(server_data + 'tgusers/').json()
	if message.chat.id in [i['ch_id'] for i in all_users]:
		user = requests.get(server_data + f'tgusers/{message.chat.id}/').json()
		passed_boards = {b['board']['name']: b['earn'] for b in requests.get(server_data + f'passedboards/?tguser__ch_id={message.chat.id}').json()}
		all_boards = requests.get(server_data + f'boards/').json()
		board_markup = telebot.types.InlineKeyboardMarkup()
		board_markup.row_width = 1
		markups = []
		for board in all_boards:
			if board == user['board']:
				markups.append(telebot.types.InlineKeyboardButton('✅ ' + board['name'], callback_data=board['name']))
			elif board['name'] in passed_boards:
				markups.append(telebot.types.InlineKeyboardButton('☑️ ' + board['name']+ f' ({passed_boards[board["name"]]})', callback_data=board['name']))
			else:
				markups.append(telebot.types.InlineKeyboardButton('❌ ' + board['name'], callback_data=board['name']))


		board_markup.add(*markups)
		# info = requests.get(server_config + 'helpsmedia/on_boards/').json()
		bot.send_photo(message.chat.id, requests.get(user['board']['img']).content, caption=on_my_boards % (user['board']['name'], user['board']['max_present_red']), reply_markup=board_markup)
		
		presents = requests.get(server_data + f'presents/?from_user__ch_id={message.chat.id}&status={True}').json()
		if len(presents) == 0:
			bot.send_message(message.chat.id, kick_after_3h, parse_mode='HTML')
	else:
		bot.reply_to(message, requests.get(server_config + 'helps/no_ref/').json()['text'])	


# 🫶 О нас
@bot.message_handler(func=lambda message: message.text == '🫶 О нас')
def keyboard_manager2(message):
	if message.chat.id in [u['ch_id'] for u in requests.get(server_data + 'tgusers/').json()]:
		help = requests.get(f'{server_config}helpsmedia/boards_info/').json()
		bot.send_photo(message.chat.id, requests.get(help['img']).content, caption=help['text'])
	else:
		bot.reply_to(message, requests.get(server_config + 'helps/no_ref/').json()['text'])


# 👋 Приглашение
@bot.message_handler(func=lambda message: message.text == '👋 Приглашение')
def keyboard_manager1(message):
	user_exist = requests.get(server_data + f'tgusers/{message.chat.id}/')
	if 200 <= user_exist.status_code < 400:
		have_sent_present = requests.get(server_data + f'presents/?from_user__ch_id={message.chat.id}&status={True}&board__id={user_exist.json()["board"]["id"]}').json()
		if len(have_sent_present):
			''' if have sended and confirmed presents'''
			exist_ref = requests.get(server_data + f'reflinks/{message.chat.id}/')

			if 200 <= exist_ref.status_code < 400:
				bot.reply_to(message, exist_ref.json()['url'])
			else:
				ref_link = generate_ref_link(user_exist.json())
				if 200 <= ref_link.status_code < 400:
					bot.reply_to(message, ref_link.json()['url'])
				else:
					bot.reply_to(message, cant_generate_ref)
		else:
			bot.reply_to(message, requests.get(f'{server_config}helps/m_ref_without_pr/').json()['text'])
	else:
		bot.reply_to(message, requests.get(server_config + 'helps/no_ref/').json()['text'])

# MESSAGES FROM KEYBOARD-INLINE-MARKUP END #


def generate_ref_link(user):
	timestamp = int(datetime.now().timestamp())
	payload = {
		"url": f'https://t.me/royal_capital_bot?start=ref_{user["ch_id"]}_{timestamp}',
		"tguser": user['id']
	}
	return requests.post(server_data + 'reflinks/', data=payload)



# CALLBACK FROM BOARDS CLICK
@bot.callback_query_handler(func=lambda call: call.data in [i['name'] for i in requests.get(server_data + 'boards/').json()])
def call_board(call):
	users_boards = {i['ch_id']: i['board']['name'] for i in requests.get(server_data + 'tgusers/').json()}
	if call.message.chat.id in users_boards:
		rcv_data = call.data.replace('✅ ', '').replace('❌ ', '')
		if rcv_data == users_boards[call.message.chat.id]:
			try:
				father = requests.get(server_data + f'tgusers/?board__name={rcv_data}&status=R').json()[0]['link']
				markup = telebot.types.InlineKeyboardMarkup()
				markup.row_width = 2
				markup_dict = [
					{'name': '👋 Сейчас узнаю', 'url': f'https://t.me/{father.replace("@", "")}', 'callback': '👋 Сейчас узнаю'},
					{'name': '✅ Еще не уточнил', 'url': None, 'callback': '✅ Еще не уточнил'},
					{'name': '🤝 Договорился', 'url': None, 'callback': '🤝 Договорился'},
					{'name': '😉 Нужно подумать', 'url': None, 'callback': '😉 Нужно подумать'},
				]
				markup.add(*[telebot.types.InlineKeyboardButton(i['name'], callback_data=i['callback'], url=i['url']) for i in markup_dict])
				bot.send_message(call.message.chat.id, requests.get(server_config + 'helps/active_board_click/').json()['text'] % father, reply_markup=markup)
			
			except:
				bot.send_message(call.message.chat.id, 'there are no users!')

		elif rcv_data in [b['board']['name'] for b in requests.get(server_data + f'passedboards/?tguser__ch_id={call.message.chat.id}').json()]:
			bot.send_message(call.message.chat.id, always_passed_this_board)

		else:
			bot.send_message(call.message.chat.id, requests.get(server_config + 'helps/cant_reg_on_board/').json()['text'])

	else:
		bot.reply_to(call.message, requests.get(server_config + 'helps/no_ref/').json()['text'])


# CALLBACK FROM BOARDS CLICK END #


# CALLBACK FROM ACTIVE BOARD SEND MONEY

@bot.callback_query_handler(func=lambda call: call.data == '🤝 Договорился')
def call_have_place(call):
	board = requests.get(server_data + f'tgusers/{call.message.chat.id}/').json()['board']
	markup = telebot.types.InlineKeyboardMarkup()
	markup.row_width = 2
	markup.add(*[telebot.types.InlineKeyboardButton(i, callback_data=i) for i in ['😉 Нужно подумать', '🤝 Понятно']])
	bot.send_message(call.message.chat.id, requests.get(server_config + 'helps/present_send_info/').json()['text'] % board['present_price'], reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['🤝 Понятно',  '🔙 Вернуться'])
def call_mystatus_and_send(call):
	info = requests.get(server_config + 'helpsmedia/before_send_board/').json()
	user = requests.get(server_data + f'tgusers/{call.message.chat.id}/').json()
	passed_boards = requests.get(server_data + f'passedboards/?tguser__ch_id={call.message.chat.id}').json()
	board = user['board']['name']
	img = requests.get(user['board']['img']).content
	all_users_sorted_w = len(requests.get(server_data + f'tgusers/?board__name={user["board"]["name"]}&status=W').json())
	
	markup = telebot.types.InlineKeyboardMarkup()
	markup.row_width = 1
	markup.add(*[telebot.types.InlineKeyboardButton(i, callback_data=str(i)) for i in ['⚜️ Данные получателя']])#, '👥 Показать дарителей', '♻️ Выбрать другую доску']])

	bot.send_photo(call.message.chat.id, img, caption=info['text'] % (board, all_users_sorted_w ,status_dict[user['status']], len(passed_boards)), reply_markup=markup)

# RECIEVER CONTACTS
@bot.callback_query_handler(func=lambda call: call.data in ['⚜️ Данные получателя', 'otpravil_no'])
def call_reciever(call):
	user = requests.get(server_data + f'tgusers/{call.message.chat.id}/').json()
	info = requests.get(server_config + 'helps/reciever_data/').json()
	reciever = requests.get(server_data + f'tgusers/?board__name={user["board"]["name"]}&status=R').json()[0]
	if user['id'] == reciever['id']:
		bot.send_message(call.message.chat.id, only_one_recv % (user['board']['name'], user['link']))
	
	
	else:
		users_on_board = requests.get(server_data + f'tgusers/?board__name={user["board"]["name"]}').json()
		markup_dict = [
			{'name': '☎️ Связаться с получателем', 'url': f'https://t.me/{reciever["link"].replace("@", "")}', 'callback': '☎️ Связаться с получателем'},
			{'name': '✅ Я отправил подарок', 'url': None, 'callback': '✅ Я отправил подарок'},
			{'name': '❌ Выйти с доски', 'url': None, 'callback': '❌ Выйти с доски'},
			{'name': '🔙 Вернуться', 'url': None, 'callback': '🔙 Вернуться'},
		]
		markup = telebot.types.InlineKeyboardMarkup()
		markup.row_width = 1
		markup.add(*[telebot.types.InlineKeyboardButton(i['name'], callback_data=i['callback'], url=i['url']) for i in markup_dict])

		bot.send_message(call.message.chat.id, info['text'] % (reciever['link'], len(users_on_board), user['board']['present_price']), reply_markup=markup)

# CHOISE FOR SENDING MONY #
@bot.callback_query_handler(func=lambda call: call.data == '✅ Я отправил подарок')
def call_ask_rcv1(call):
	markup_dict = [
		{'name': '✅ Да', 'url': None, 'callback': 'otpravil_yes'},
		{'name': '⛔️ Нет', 'url': None, 'callback': 'otpravil_no'},
	]
	markup = telebot.types.InlineKeyboardMarkup()
	markup.row_width = 2
	markup.add(*[telebot.types.InlineKeyboardButton(i['name'], callback_data=i['callback'], url=i['url']) for i in markup_dict])
	bot.send_message(call.message.chat.id, requests.get(server_config + 'helps/redy_yes_no/').json()['text'], reply_markup=markup)

# CLICKED YES BUTTON ON SENDING #
@bot.callback_query_handler(func=lambda call: call.data == 'otpravil_yes')
def call_ask_rcv2(call):
	user = requests.get(server_data + f'tgusers/{call.message.chat.id}/').json()
	reciever = requests.get(server_data + f'tgusers/?board__name={user["board"]["name"]}&status=R').json()[0]
	info = requests.get(server_config + 'helps/mes_for_reciever/').json()
	
	if user['id'] == reciever['id']:
		bot.send_message(call.message.chat.id, only_one_recv % (user['board']['name'], user['link']))
	
	
	else:
		timestamp = int(datetime.now().timestamp())

		recv_markup_dict = [
			{'name': '✅ Да, получил', 'url': None, 'callback': f'poluchilYes_{call.message.chat.id}_{timestamp}'},
			{'name': '⛔️ Нет, не получал', 'url': None, 'callback': f'poluchilNo_{call.message.chat.id}_{timestamp}'},
		]
		recv_markup = telebot.types.InlineKeyboardMarkup()
		recv_markup.row_width = 2
		recv_markup.add(*[telebot.types.InlineKeyboardButton(i['name'], callback_data=i['callback'], url=i['url']) for i in recv_markup_dict])
		payload = {
			"name": f'poluchilYes_{call.message.chat.id}_{timestamp}',
			"status": False,
			'board': int(user['board']['id']),
			"to_user": reciever['id'],
			"from_user": user['id']
		}

		print(payload)
		
		responce = requests.post(server_data + 'presents/', data=payload)
		print(responce)
		if 200 <= responce.status_code < 400:
			bot.send_message(reciever['ch_id'], info['text'] % (user['board']['present_price'], reciever['board']['name'], user['link']), reply_markup=recv_markup)
			bot.send_message(call.message.chat.id, '✅ Готово')
		
		else:
			bot.send_message(call.message.chat.id, requests.get(server_config + 'helps/cant_send_pres/').json()['text'])


@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'poluchilYes')
def call_recv_yes(call):
	present = requests.get(server_data + f'presents/{call.data}/').json()
	payload = {
		"id": present['id'],
		"name": present['name'],
		"status": True,
		"board": present['board']['id'],
		"to_user": present['to_user']['id'],
		"from_user": present['from_user']['id']
	}
	responce = requests.put(server_data + f'presents/{call.data}/', data=payload)
	my_presents_sent = requests.get(server_data + f'presents/?from_user__ch_id={call.message.chat.id}&status={True}&board__id={present["board"]["id"]}').json()
	my_presents_rcv = requests.get(server_data + f'presents/?to_user__ch_id={call.message.chat.id}&status={True}&board__id={present["board"]["id"]}').json()

	if 200 <= responce.status_code < 400:
		info = requests.get(server_config + 'helps/confirmed_pres/').json()['text']
		bot.send_message(call.message.chat.id, info % (present['board']['present_price'], present['from_user']['link'], len(my_presents_rcv), len(my_presents_sent)))
		

		# PORYADOK VIZOVA FUNKCIY VAZHEN!
		modify_userfrom_W_to_G(present['from_user']['ch_id'])

		if is_change_my_status(present['to_user']):
			rcv_status_to_VOID(present['to_user'])
			print(new_reciever_on_BOARD(present['board']))


		sender_presents_sent = requests.get(server_data + f"presents/?from_user__ch_id={present['from_user']['ch_id']}&status={True}&board__id={present['board']['id']}").json()
		sender_presents_rcv = requests.get(server_data + f"presents/?to_user__ch_id={present['from_user']['ch_id']}&status={True}&board__id={present['board']['id']}").json()
		bot.send_message(present['from_user']['ch_id'], requests.get(server_config + 'helps/success_confirm/').json()['text'] % (present['to_user']['link'], present['board']['present_price'], len(sender_presents_rcv), len(sender_presents_sent)))

	else:
		bot.send_message(call.message.chat.id, requests.get(server_config + 'helps/cant_confirm_pres/').json()['text'])





@bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'poluchilNo')
def call_recv_no(call):
	data = call.data.replace('poluchilNo', 'poluchilYes')
	present = requests.get(server_data + f'presents/{data}/').json()

	my_presents_sent = requests.get(server_data + f'presents/?from_user__ch_id={call.message.chat.id}&status={True}').json()
	my_presents_rcv = requests.get(server_data + f'presents/?to_user__ch_id={call.message.chat.id}&status={True}').json()

	info = requests.get(server_config + 'helps/not_confirmed_pres/').json()['text']
	bot.send_message(call.message.chat.id, info % (present['from_user']['link'], len(my_presents_rcv), len(my_presents_sent)))
	
	sender_presents_sent = requests.get(server_data + f"presents/?from_user__ch_id={present['from_user']['ch_id']}&status={True}").json()
	sender_presents_rcv = requests.get(server_data + f"presents/?to_user__ch_id={present['from_user']['ch_id']}&status={True}").json()
	bot.send_message(present['from_user']['ch_id'], requests.get(server_config + 'helps/not_confirmed_sender/').json()['text'] % (present['to_user']['link'], present['board']['present_price'], len(sender_presents_sent), len(sender_presents_rcv)))



def new_reciever_on_BOARD(board):
	users_on_BOARD = requests.get(server_data + f'tgusers/?board__name={board["name"]}&status=G').json() # HAD SORT WITH ORERING BY "join_date" ON BACKEND
	print(users_on_BOARD)
	if len(users_on_BOARD) == 0:
		''' if a user of the R status, having given himself gifts, left the board and there are no any users with G status '''
		users_on_BOARD = requests.get(server_data + f'tgusers/?board__name={board["name"]}&status=W').json()
	
	early_registered_user = users_on_BOARD[0]

	payload = {
			"id": early_registered_user['id'],
			"name": early_registered_user['name'],
			"ch_id": early_registered_user['ch_id'],
			"join_date": early_registered_user['join_date'],
			"link": early_registered_user['link'],
			"status": 'R',
			"board": early_registered_user['board']['id']
		}
	bot.send_message(early_registered_user['ch_id'], congrats_status_up)
	return requests.put(server_data + f'tgusers/{early_registered_user["ch_id"]}/', data=payload)




def rcv_status_to_VOID(user):
	payload = {
			"id": user['id'],
			"name": user['name'],
			"ch_id": user['ch_id'],
			"join_date": user['join_date'],
			"link": user['link'],
			"status": 'V',
			"board": user['board']['id']
		}
	return requests.put(server_data + f'tgusers/{user["ch_id"]}/', data=payload).json()



def is_change_my_status(user):
	presents = requests.get(server_data + f'presents/?to_user__ch_id={user["ch_id"]}&status={True}&board__id={user["board"]["id"]}').json()
	print('khuy', len(presents))

	if len(presents) >= user['board']['max_present_red']:

		passed_board_payload = {
			"earn": user['board']['present_price']*user['board']['max_present_red'],
			"tguser": user['id'],
			"board": user['board']['id']
		}
		requests.post(server_data + 'passedboards/', data=passed_board_payload)

		markup = telebot.types.InlineKeyboardMarkup()
		markup.row_width = 2
		markup.add(*[telebot.types.InlineKeyboardButton(i['name'], callback_data=i['callback'], url=i['url']) for i in markup_leave_board])

		bot.send_message(user["ch_id"], transition_from_board % (user['board']['name'], user['board']['present_price']*7) , reply_markup=markup)
		
		return True

	else:
		return False


@bot.callback_query_handler(func=lambda call: call.data in '✅ Остаться')
def call_leave_no(call):
	user = requests.get(server_data + f'tgusers/{call.message.chat.id}/').json()
	current_board_state = user["board"]["state"]

	# GAME OVER
	if current_board_state >= 7:
		payload = {
			"id": user['id'],
			"name": user['name'],
			"ch_id": 0,
			"join_date": user['join_date'],
			"link": user['link'],
			"status": 'V',
			"board": user['board']['id']
		}
		requests.put(server_data + f'tgusers/{call.message.id}/', data=payload)

		bot.delete_message(call.message.chat.id, call.message.id)
		bot.send_message(call.message.chat.id, 'U leaved our game')

	else:
		next_board = requests.get(server_data + f'boards/?state={current_board_state + 1}').json()[0]
		users_on_board = requests.get(server_data + f'tgusers/?board__name={next_board["name"]}').json()
		
		payload = {
			"id": user['id'],
			"name": user['name'],
			"ch_id": user['ch_id'],
			"join_date": user['join_date'],
			"link": user['link'],
			"status": 'W',
			"board": next_board['id']
		}
		requests.put(server_data + f'tgusers/{user["ch_id"]}/', data=payload)


		bot.delete_message(call.message.chat.id, call.message.id)
		bot.send_message(call.message.chat.id, new_board % (next_board['name'], next_board['present_price'], len(users_on_board)))





@bot.callback_query_handler(func=lambda call: call.data == '❌ Покинуть')
def call_leave_yes(call):
	user = requests.get(server_data + f'tgusers/{call.message.chat.id}/').json()
	payload = {
		"id": user['id'],
		"name": user['name'],
		"ch_id": 0,
		"join_date": user['join_date'],
		"link": user['link'],
		"status": "V",
		"board": user['board']['id']
	}
	requests.put(server_data + f'tgusers/{call.message.chat.id}/', data=payload)
	bot.delete_message(call.message.chat.id, call.message.id)
	bot.send_message(call.message.chat.id, 'U leaved our game')





def modify_userfrom_W_to_G(ch_id):
	user = requests.get(server_data + f'tgusers/{ch_id}/').json()
	print(user)
	if user['status'] == 'W':
		payload = {
			"id": user['id'],
			"name": user['name'],
			"ch_id": ch_id,
			"join_date": user['join_date'],
			"link": user['link'],
			"status": 'G',
			"board": user['board']['id'],
		}
		requests.put(server_data + f'tgusers/{ch_id}/', data=payload)
	
	else:
		pass

bot.infinity_polling()