FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /internal
COPY uv.lock /uv.lock
COPY pyproject.toml /pyproject.toml

# Создаем и активируем виртуальное окружение
RUN python -m venv /internal/.venv
ENV PATH="/internal/.venv/bin:$PATH"

# Install the application dependencies.
WORKDIR /internal
# Install the project's dependencies using the lockfile and settings
RUN uv sync --frozen --no-install-project --no-dev

# Run the application.
CMD ["uvicorn", "internal.main:app", "--host", "0.0.0.0", "--reload"]