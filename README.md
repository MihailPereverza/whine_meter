# Whine meter

## Dev setup

* Установка: `pip install -r requirements.txt`
* Запуск: `run_all.sh` (Mac OS/Linux) (требует Docker Compose для базы данных)
* Либо запуск 3 команд руками:
  * `docker-compose up postgres`
  * `DB_URL=postgresql+psycopg://user:password@postgres/whinemeter python -m whine_meter` из папки `backend`
  * `BACKEND_URL=http://localhost:8080 python -m bot` из папки `frontend`

## 'Prod' setup

* `docker-compose up`
