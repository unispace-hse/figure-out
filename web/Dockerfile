FROM python:3.9

ENV PYTHONUNBUFFERED=1

# Копируем файлы веб-приложения из корня проекта внутрь контейнера
COPY . /web_app

# Задаем рабочую директорию
WORKDIR /web_app

# Устанавливаем зависимости из файла requirements.txt
RUN pip install -r requirements.txt

# Команда для запуска сервера Django при старте контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
