FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends binutils

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install project dependencies and pyinstaller using poetry
RUN poetry install --no-root --no-dev

# Install pyinstaller globally if it's not a project dependency
RUN pip install pyinstaller --no-warn-script-location

COPY aps2mqtt/ /app/aps2mqtt
WORKDIR /app
# Use poetry run for pyinstaller to ensure it uses the correct environment
RUN poetry run pyinstaller --collect-all tzdata --onefile /app/aps2mqtt/__main__.py -n aps2mqtt

FROM ubuntu:noble AS runner
RUN apt update && apt install tzdata -y && apt clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/dist/aps2mqtt /app/

WORKDIR /app
CMD ["./aps2mqtt"]