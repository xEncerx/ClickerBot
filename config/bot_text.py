from config.bot_data import money_name, balance_for_referral, balance_for_click

class Text:
    welcome: str = "✅ <b>Добро пожаловать в StandClix!</b>\n" \
                   "➡️ <b>Здесь ты можешь поднять голды абсолютно без вложений</b>\n" \
                   "<i>Тебе лишь нужно выполнять простые действия</i>\n\n" \
                   "<i>Жми кнопку</i> <b>Начать!</b>"

    main_menu: str = "👻 <b>Пункт управления ботом</b>\n\n"\
                     "🔥 <i>Для начала рекомендую покликать {money_name}, потом переходи на выполнение заданий и приглашение друзей!</i>"

    profile: str = "<b>Профиль:</b>\n" \
                   "➖➖➖➖➖➖➖➖➖\n" \
                   "<b>ID:</b> <code>{ID}</code>\n" \
                   "<b>Username:</b> <code>{username}</code>\n" \
                   "<b>Balance:</b> <code>{balance}</code>\n" \
                   "<b>Рефералов:</b> <code>{referrer}</code>\n" \
                   "➖➖➖➖➖➖➖➖➖"

    earn: str = "🔥 <i>Ты можешь получить голду за:</i>\n\n" \
                "\t➖ <b>Кликер</b>\n" \
                "\t➖ <b>Выполнение заданий</b>\n" \
                "\t➖ <b>Приглашение людей</b>"

    invite: str = f"💰 За каждого приглашенного человека ты будешь получать <b>{balance_for_referral} {money_name}!</b>\n\n" \
                  f"💥 Рекламировать ссылку можно в чатах стендофф 2 или же просто отправить ее друзьям!\n\n" \
                  f"☀️ Приглашай людей по этой ссылке, как только кто-то перейдет по твоей ссылке мы тебя оповестим!\n\n" \
                  "<code>{link}</code>"

    clicker: str = 'Жми на кнопку <b>"Клик"</b> 👇\n\n' \
                   '<b>Кликать можно раз в 5 секунд!</b>'

    sleep_message: str = "⏳ <b>Ожидайте 5 секунд</b>"

    pay_click: str = f"✅ Вы успешно получили <b>+{balance_for_click} {money_name}</b>"

    task_text: str = "<b>Задание №{task_id}</b>\n" \
                     "━━━━━━━━━━━━━━━━━━\n" \
                     "{description}\n" \
                     "━━━━━━━━━━━━━━━━━━\n" \
                     "<b>Вы получите +{reward} {money_name} за выполнение данного задания</b>"

    no_task: str = "⚠️ <b>К сожалению задания закончились</b> 😔"

    task_not_exist: str = "⚠ <b>К сожалению мне не удалось найти такого задания</b>"

    promo_not_exist: str = "⚠ <b>К сожалению мне не удалось найти такого промокода</b>"

    no_money: str = "❌ У вас недостаточно {money_name} для вывода. Минимальную сумма вывода - {min_withdraw}"

    no_referrals: str = "❌ У вас недостаточно рефералов для вывода. Пригласите ещё {referral}"

    choose_task: str = "👇 <b>Выбери задание ниже</b>"

    withdraw: str = "✅ <i>Для вывода необходимо заполнить форму по ссылке:</i> <a href='{link}'>https://docs.google.com/forms/</a>\n\n" \
                    "<b>После успешного заполнения с вами свяжется админ и передаст баланс в игру</b>"

    uncompleted_task: str = "❌ Это задание не может быть выполнено!"

    task_not_complete: str = "❌ Вы ещё не выполнили задание"

    not_valid_id: str = "❌ Неправильный формат Id канала"

    successful_task: str = "👍 Вы успешно выполнили задание {task_id}"

    dont_subscribe: str = "❌ Вы не подписались на канал"

    error_with_task: str = "❗️ Произошла ошибка в проверке чата: <code>{channel_id}</code>"

    admin_menu: str = "Добро пожаловать в админ меню <b>{name}</b>\n" \
                      "<i>Выбери интересующий тебя пункт меню ниже</i>"

    statistic: str = "<b>Новых пользователей за час:</b> <code>{hour}</code>\n" \
                     "<b>Новых пользователей за день:</b> <code>{day}</code>\n" \
                     "<b>Новых пользователей за месяц:</b> <code>{month}</code>\n" \
                     "<b>Мертвых пользователей:</b> <code>{block}</code>\n" \
                     "<b>Всего пользователей:</b> <code>{all}</code>"

    add_task_menu: str = "<b>Создание задания</b>\n" \
                         "<i>Заполните параметры ниже.</i>"

    add_promo_menu: str = "<b>Создание промокода</b>\n" \
                          "<i>Заполните параметры ниже.</i>"

    task_change_description: str = "<b>Укажите описание задания:</b>"

    task_change_reward: str = "<b>Укажите вознаграждение за задание: </b>"

    promo_change_reward: str = "<b>Укажите вознаграждение за промокод: </b>"

    promo_change_promo: str = "<b>Укажите промокод: </b>"

    task_change_channel_link: str = "<b>Укажите ссылку на канал:</b>"

    task_change_channel_id: str = "<b>Укажите ID канала:</b>"

    task_id: str = "<b>Укажите ID задания:</b>"

    task_not_filled: str = "⚠️ Необходимо указать описание и вознаграждение"

    incorrect_reward_type: str = "⚠️ Вознаграждение должно быть числом"

    incorrect_task_type: str = "️⚠ ID должно быть числом"

    task_added: str = "👍 Задание было добавлено"

    promo_added: str = "👍 Промокод был добавлен"

    promo_dont_filled: str = "⚠️ Не все параметры указаны"

    mailing: str = "<b>Пришлите мне сообщение для рассылки</b>\n" \
                   "<i>Формат: текст, фото, фото(+подпись)\n\n" \
                   "Можно использовать HTML разметку</i>"

    successful_promo: str = "👍 <b>Вы успешно активировали промокод, вам начислено</b> <code>{reward}</code>"

    promo_used: str = "❌ <b>Промокод уже был использован</b>"


text = Text()
