run_db() {
  docker-compose up postgres
}

run_backend() {
  (sleep 2 && cd backend && DB_URL=postgresql+psycopg://user:password@localhost:25432/whinemeter python -m whine_meter)
}

run_tgbot() {
  (sleep 4 && cd tg_bot/src && BACKEND_URL=http://localhost:8080 python -m tgbot.init_bot.run)
}

(trap 'kill 0' SIGINT; run_db & run_backend & run_tgbot & wait)
docker-compose down
