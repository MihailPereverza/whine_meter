# Whine meter

Нытьеметр позволяет находить нытиков в telegram чатах с помощью NLP-модели и прожаривать их. Также умеет рисовать графики по дням недели, по участникам чата и пр.

Ссылка на презентацию https://docs.google.com/presentation/d/1HrLE4Z6Mz4iyOCSAAcU-mm7oN-BnOqglS7hdHt994Gk/edit?usp=sharing

## Dev setup

Для запуска нужно создать Telegram бота и положить его токен в `TG_BOT_TOKEN` в переменных среды (например, с помощью `.env` файла).
Также нужно настроить бота, чтобы он смотрел на тексты сообщений (через botfather'а).

* Установка: `pip install -r requirements.txt`
* Запуск: `run_all.sh` (Mac OS/Linux) (требует Docker Compose для базы данных)
* Либо запуск 3 команд руками:
  * `docker-compose up postgres`
  * `DB_URL=postgresql+psycopg://user:password@localhost:25432/whinemeter python -m whine_meter` из папки `backend`
  * `BACKEND_URL=http://localhost:8080 python -m tgbot.init_bot.run` из папки `tgbot/src`

## 'Prod' setup

См. про создание бота выше.

* `docker-compose up`
