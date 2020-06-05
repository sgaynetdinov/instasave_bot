[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/sgaynetdinov/instasave_bot) ![CircleCI](https://img.shields.io/circleci/build/github/sgaynetdinov/instasave_bot/master.svg?label=build%20master)

# Бот для Вконтакте

Отправлям боту ссылку на фото из Instagram, в ответ бот пресылает фото.

- https://vk.com/instasave_bot — группа
- https://vk.me/instasave_bot — чат

Получаем сообщения от Вконтакте через [Callback API](https://vk.com/dev/callback_api).

Необходимо в `environment`, добавить следующие ключи:
- SECRET_KEY
- CONFIRMATION_KEY
- GROUP_ID
- GROUP_TOKE
- SENTRY_DSN
- SESSION_ID
