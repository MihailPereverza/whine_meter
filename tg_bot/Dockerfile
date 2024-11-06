FROM python:3.11.6
WORKDIR /app/src
RUN cd ..
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "tgbot.init_bot.run"]
