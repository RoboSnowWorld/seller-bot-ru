# seller-bot-ru
telegram бот для продажи аккаунтов

# Как установить
* Введите ваши реквизиты в **creditionals.txt**
* Загрузите ваши аккаунты в папку **accounts**
* Напишите **название** для аккаунтов и **цену** в первой строке каждого файла
```
simple_accounts 4
account_1
account_2
account_3
```
* Введите ваше имя пользователя в main.py
<img src="https://i.imgur.com/JjL5Mys.jpg" alt="From your telegram profile" width="320" height="160">

```
admin_username = имя пользователя
```
* Введите ваш токен в main.py
```
bot = telebot.TeleBot('токен')
```
* Запустите бот и отправьте сообщение "chat_id"

<img src="https://i.imgur.com/nEwTAJC.jpg" alt="Exaple" width="320" height="160">

* Введите ответ в main.py
```
admin_chat_id = 'ответ'
```
* Настройте ответы бота по вашему вкусу в main.py
```
bot.send_message(message.chat.id, 'Telegram bot for buying accounts\nSupport [your contacts]')
```
* Укажите вашу валюту в main.py
```
currency = 'р'
```

# Использование
* Вы увидите сообщение что кто-то купил аккаунты
<img src="https://i.imgur.com/oqWDcYz.jpg" alt="Exaple" width="320" height="160">

* Вы можете использовать команду **accept_buy [номер заказа]** если вы получили деньги
<img src="https://i.imgur.com/hLhRGS6.jpg" alt="Exaple" width="320" height="160">

* Вы можете использовать команду **decline_buy [номер заказа]** если вы не получили деньги
<img src="https://i.imgur.com/QpA0YRp.jpg" alt="Exaple" width="320" height="160">
