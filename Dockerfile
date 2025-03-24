# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Устанавливаем зависимости
WORKDIR /app
COPY pyproject.toml ./
RUN pip install uv

# Копируем исходники
COPY ./internal /app/internal

# Пробрасываем порты
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "internal.main:app", "--host", "0.0.0.0", "--port", "8000"]
