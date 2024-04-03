[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-blue.svg)](https://github.com/aiogram/aiogram)
[![Лицензия: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Игровой бот-кликер для Telegram
### 📃 | О боте
  - 👇 **Кликай**
  - 📖 **Выполяняй задания**
  - 👥 **Приглашай друзей**
  - 📤 **Выводи баланс**
### 🛠 | Для запуска бота
  - Установите python 3.x (Протестировано на 3.11)
  - Далее, установите все библиотеки из файла requirements.txt
    ```
    # Windows or Linux
    pip install -r requirements.txt
    ```
  - <details>
    <summary>Настройка конфига</summary>
    <b>Открываем файл config.ini</b><br>
    - <b><i>admin_id</i></b> | Указываем id админ(а/ов)<br>
    - <b><i>token</i></b> | Указываем токер бота. Можно получить у @BotFather<br>
    - <b><i>balance_for_referral</i></b> | Баланс за каждого рефералла<br>
    - <b><i>balance_for_clicking</i></b> | Баланс за 1 клик<br>
    - <b><i>min_withdraw</i></b> | Минимальная сумма вывода<br>
    - <b><i>min_referral_withdraw</i></b> | Минимальное кол-во рефераллов для вывода<br>
    - <b><i>redirect_link</i></b> | Ссылка переадресации при выводе баланса<br>
    - <b><i>feedback_link</i></b> | Ссылка на отзывы (Опцианально)<br>
    - <b><i>bot_username</i></b> | UserName бота<br>
    </details>
- <details>
  <summary>Настройка изображений</summary>
  - <b>В меню бота можно добавить собственные изображения</b><br><br>
    <b>В файле bot/data/config.py нужно будет изменить Mode в соответствии с выбранным методом<br>
    Предпочтительно использовать FileID - это самый быстрый способ отправки изображений пользователю</b>
    
    <br><i>Есть 3 способа это сделать: file_id, url, файлы</i><br>
    <b>1) Файлы:</b><br>
      - Закидываем файлы в папку images с названиями [welcome, promocode, tasks, withdraw, admin_menu, profile]<br>
    <b>2) URL:</b><br>
      - Загружаем файл на фото-хостинг и передаем ссылку в словарь в файле bot/data/config.py<br>
    <b>3) FileID:</b><br>
      - Запускаем бота, вводим комманду /file_id, отправляем фотографию и получаем photoID. Передаём его в словарь файла bot/data/config.py
  </details>
- Запустите файл main.py и наслаждайтесь!
## ❤️ Вклад и поддержка

Если у вас есть предложения по улучшению этого проекта или вы столкнулись с проблемами, пожалуйста, создайте новый issue или отправьте pull request.
