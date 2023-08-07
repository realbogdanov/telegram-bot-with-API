Share Airplane - Телеграм бот для работы с API AeroDataBox

Share Airplane - это телеграм бот, который позволяет получить информацию о ближайших аэропортах и текущем статусе рейсов по номеру, используя API AeroDataBox. Просто введите команды и получите необходимую информацию о перелетах.
Установка и запуск

    Склонируйте репозиторий на свой компьютер:

bash

git clone https://github.com/realbogdanov/share-airplane-bot.git
cd share-airplane-bot

    Переименуйте файл env.template в .env:

bash

mv env.template .env

    Получите токен для своего телеграм бота у @BotFather и укажите его в файле .env в поле BOT_TOKEN.

    Получите токен API на https://rapidapi.com/airlabsco/api/aerodatabox, выбрав подходящий тарифный план и подписавшись на него. Вставьте полученный токен в поле SITE_API файла config.py.

    Получите хост API на https://rapidapi.com/airlabsco/api/aerodatabox, выбрав подходящий тарифный план и перейдя во вкладку "Code Snippets". Скопируйте значение из поля X-RapidAPI-Host и вставьте его в поле API_HOST файла config.py.

    Установите зависимости:

bash

pip install -r requirements.txt

    Запустите бота:

bash

python main.py

Использование

Просто введите команды в чат с ботом, чтобы получить информацию о ближайших аэропортах и статусе рейсов:

    /start - Запуск бота
    /help - получить список всех доступных команд.
    /hello_world - Тестовый вывод.
    /low - Поиск ближайшего аэропорта по геолокации.
    /high - Поиск аэропортов в выбранном городе.
    /custom - Получение данных о прошедшем.
    /history - История поисков.

Документация

Подробные инструкции по использованию можно найти в каждом файле программы.
Автор

Автор проекта: Богданов Василий Викторович
Контакты

    Почта: realbogdanov@gmail.com
    GitHub: realbogdanov
    Facebook: https://www.facebook.com/yukozar

Share Airplane - Telegram Bot for Working with AeroDataBox API

Share Airplane is a Telegram bot that allows you to get information about the nearest airports and the current flight status by using the AeroDataBox API. Simply enter commands and get the necessary flight information.
Installation and Setup

    Clone the repository to your computer:

bash

git clone https://github.com/realbogdanov/share-airplane-bot.git
cd share-airplane-bot

    Rename the env.template file to .env:

bash

mv env.template .env

    Get a token for your Telegram bot from @BotFather and insert it into the .env file in the BOT_TOKEN field.

    Obtain an API token from https://rapidapi.com/airlabsco/api/aerodatabox by choosing an appropriate plan and subscribing to it. Insert the obtained token into the SITE_API field in the config.py file.

    Get the API host from https://rapidapi.com/airlabsco/api/aerodatabox by selecting the appropriate plan and navigating to the "Code Snippets" tab. Copy the value from the X-RapidAPI-Host field and insert it into the API_HOST field in the config.py file.

    Install the required dependencies:

bash

pip install -r requirements.txt

    Run the bot:

bash

python main.py

Usage

Simply enter commands in the chat with the bot to get information about the nearest airports and flight statuses:

    /start - Start the bot.
    /help - Get a list of all available commands.
    /hello_world - Test output.
    /low - Find the nearest airport based on geolocation.
    /high - Find airports in the selected city.
    /custom - Get data about a past flight.
    /history - Search history.

Documentation

Detailed instructions for usage can be found in each program file.
Author

Project author: Vasily Bogdanov
Contacts

    Email: realbogdanov@gmail.com
    GitHub: realbogdanov
    Facebook: https://www.facebook.com/yukozar