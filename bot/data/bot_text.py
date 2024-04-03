# -*- coding: utf-8 -*-

"""
Текст можно менять по своему желанию. Следовательно и стилистику бота
! МОЖНО ИСПОЛЬЗОВАТЬ HTML РАЗМЕТКУ

Параметры можно менять местами или вовсе не использовать в сообщениях
! НЕ ВСЕ СООБЩЕНИЯ ПОДДЕРЖИВАЮТ ПАРАМЕТРЫ
! ПАРАМЕТРЫ УКАЗЫВАЮТСЯ В фигурных скобках {название}

Переменные + возможные параметры:
profile - {ID}, {username}, {balance}, {referrer}
invitations - {balance_for_referral}, {link}
earn_currency - {balance_for_click}
task_text - {task_id}, {description}, {reward}
withdraw - {link}
admin_menu - {name}
statistic - {hour}, {day}, {month}, {block}, {all}
completed_task - {task_id}, {reward}
used_promo - {reward}
no_money - {min_withdraw}
no_referrals - {referral}
cant_check_task - {channel_id}
new_referrer = {username}, {balance_for_referral}, {new_balance}
deleted - {promo}
added - {promo}, {reward}
deleted - {task_id}
"""

class BotText:
	welcome = "✅ <b>Добро пожаловать в StandClix!</b>\n" \
			  "➡️ <b>Здесь ты можешь поднять голды абсолютно без вложений</b>\n" \
			  "<i>Тебе лишь нужно выполнять простые действия</i>\n\n" \
			  "<i>Жми кнопку</i> <b>Начать!</b>"

	main_menu = "👻 <b>Пункт управления ботом</b>\n\n" \
				"🔥 <i>Для начала рекомендую покликать голды, потом переходи на выполнение заданий и приглашение друзей!</i>"

	profile = "<b>Профиль:</b>\n" \
			  "➖➖➖➖➖➖➖➖➖\n" \
			  "<b>ID:</b> <code>{ID}</code>\n" \
			  "<b>Username:</b> <code>{username}</code>\n" \
			  "<b>Balance:</b> <code>{balance}</code>\n" \
			  "<b>Рефералов:</b> <code>{referrer}</code>\n" \
			  "➖➖➖➖➖➖➖➖➖"

	earn = "🔥 <i>Ты можешь получить голду за:</i>\n\n" \
		   "\t➖ <b>Кликер</b>\n" \
		   "\t➖ <b>Выполнение заданий</b>\n" \
		   "\t➖ <b>Приглашение людей</b>"

	invitation = "💰 За каждого приглашенного человека ты будешь получать <b>{balance_for_referral} голды!</b>\n\n" \
				  "💥 Рекламировать ссылку можно в чатах стендофф 2 или же просто отправить ее друзьям!\n\n" \
				  "☀️ Приглашай людей по этой ссылке, как только кто-то перейдет по ней, мы тебя оповестим!\n\n" \
				  "<code>{link}</code>"

	clicker = 'Жми на кнопку <b>"Клик"</b> 👇\n\n' \
			  '<b>Кликать можно раз в 5 секунд!</b>'

	delay_message = "⏳ <b>Ожидайте 5 секунд</b>"

	earn_currency = "✅ Вы успешно получили <b>+{balance_for_click} голды</b>"

	task_text = "<b>Задание №{task_id}</b>\n" \
				"━━━━━━━━━━━━━━━━━━\n" \
				"{description}\n" \
				"━━━━━━━━━━━━━━━━━━\n" \
				"<b>Вы получите +{reward} голды за выполнение данного задания</b>"

	choose_task = "👇 <b>Выбери задание ниже</b>"

	withdraw = "✅ <i>Для вывода необходимо заполнить форму по ссылке:</i> <a href='{link}'>Тебе сюда</a>\n\n" \
			   "<b>После успешного заполнения с вами свяжется админ и передаст баланс в игру</b>"

	new_referrer = "🎉 У вас новый реферал(<code>@{username}</code>), " \
				   "ваш баланс пополнен на <code>{balance_for_referral}</code> голды\n\n На вашем балансе <code>{new_balance}</code> голды"

	enter_promo = "<b>Укажите промокод: </b>"

	class admin:
		admin_menu = "Добро пожаловать в админ меню <b>{name}</b>\n" \
					 "<i>Выбери интересующий тебя пункт меню ниже</i>"

		statistic = "<b>➖ Новых пользователей за час:</b> <code>{hour}</code>\n" \
					"<b>➖ Новых пользователей за день:</b> <code>{day}</code>\n" \
					"<b>➖ Новых пользователей за неделю:</b> <code>{week}</code>\n" \
					"<b>➖ Новых пользователей за месяц:</b> <code>{month}</code>\n" \
					"<b>☠️ Мертвых пользователей:</b> <code>{block}</code>\n" \
					"<b>👥 Всего пользователей:</b> <code>{all}</code>"

		mailing = "<b>Пришлите мне сообщение для рассылки:</b>\n" \
				   "(<i><u>текст, фото, документ, стикер и т.д</u></i>)\n\n" \
				  "<i>Можно использовать форматирование текста</i>"
		send_image = "🖼 <b>Пришли мне фотографию, чтобы получить её file_id</b>"

		class promo:
			add_menu = "<b>Создание промокода</b>\n" \
					   "<i>Заполните параметры ниже.</i>"

			change_reward = "<b>Укажите вознаграждение за промокод: </b>"
			change_promo = "<b>Укажите промокод: </b>"
			added = "👍 Промокод ({promo} | {reward}) был добавлен"
			dont_filled = "⚠️ Не все параметры указаны"
			dont_added = "❌ Не удалось создать промокод"
			delete_promo = "<b>Укажите промокод для удаления: </b>"
			deleted = "👍 Промокод (<code>{promo}</code>) был удален"

		class task:
			add_menu = "<b>Создание задания</b>\n" \
					   "<i>Заполните параметры ниже.</i>"

			change_description = "<b>Укажите описание задания:</b> \n" \
								  "<u>Можно использовать HTML разметку</u>"
			change_reward = "<b>Укажите вознаграждение за задание: </b>"
			change_channelID = "<b>Укажите ID канала:</b>\n\n" \
							   "<u>Ссылку необходимо указать в описании задания</u>\n"
			change_fileID = "📁 Пришлите мне файл или изображение"
			task_id = "<b>Укажите ID задания:</b>"
			not_filled = "⚠️ Необходимо указать описание и вознаграждение"
			incorrect_reward_type = "⚠️ Вознаграждение должно быть числом"
			incorrect_task_type = "️⚠ ID должно быть числом"
			added = "👍 <b>Задание было добавлено</b>"
			deleted = "👍 <b>Задание с ID (<code>{task_id}</code>) было удалено!</b>"

	class successful:
		completed_task = "👍 <b>Вы успешно выполнили задание № {task_id}, вам начислено</b> <code>{reward}</code>"
		used_promo = "👍 <b>Вы успешно активировали промокод, вам начислено</b> <code>{reward}</code>"

	class error:
		not_digit = "❗️ Данный параметр должен быть целым числом"
		no_task = "⚠️ К сожалению задания закончились 😔"
		no_money = "❌ У вас недостаточно голды для вывода. Минимальную сумма вывода - {min_withdraw}"
		no_referrals = "❌ У вас недостаточно рефералов для вывода. Пригласите ещё {referral}"
		uncompleted_task = "❌ Это задание не может быть выполнено!"
		task_not_completed = "❌ Вы ещё не выполнили задание"
		invalid_id = "❌ Неправильный формат Id канала"
		dont_subscribe = "❌ Вы не подписались на канал"
		cant_check_task = "❗️ Произошла ошибка в проверке чата: <code>{channel_id}</code>"
		promo_used = "❌ <b>Промокод уже был использован</b>"
		message_missed = "♦️ Unknown command.\n" \
						 "♦️ Enter /start"
		bot_not_chat_admin = "❌ <b>Бот не является администратором канала</b>\n" \
							  "<i>Сделайте бота админом и попробуйте ещё</i>"
		cant_check_subscription = "😔 Произошла ошибка при проверке подписки. Отпишитесь админу"

	class notExists:
		task = "⚠ <b>К сожалению мне не удалось найти такого задания</b>"
		promo = "⚠ <b>К сожалению мне не удалось найти такого промокода</b>"
