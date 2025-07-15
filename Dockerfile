FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends binutils

COPY requirements.txt .
RUN pip install --user -r requirements.txt pyinstaller --no-warn-script-location

COPY aps2mqtt/ /app/aps2mqtt
WORKDIR /app
RUN /root/.local/bin/pyinstaller --collect-all tzdata --onefile /app/aps2mqtt/__main__.py -n aps2mqtt

FROM ubuntu:noble AS runner
RUN apt update && apt install tzdata -y && apt clean && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/dist/aps2mqtt /app/

WORKDIR /app
CMD ["./aps2mqtt"]