FROM python:3.13-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends binutils \
    && rm -rf /var/lib/apt/lists/*

COPY . /build
WORKDIR /build
RUN pip install --no-cache-dir --user . pyinstaller --no-warn-script-location
RUN SITE_PACKAGES=$(python -c "import sysconfig; print(sysconfig.get_path('purelib', 'posix_user'))") \
    && /root/.local/bin/pyinstaller --collect-all tzdata --onefile "$SITE_PACKAGES/aps2mqtt/__main__.py" -n aps2mqtt

FROM ubuntu:noble AS runner

LABEL org.opencontainers.image.source="https://github.com/fligneul/aps2mqtt" \
      org.opencontainers.image.description="Access APSystems ECU data over MQTT" \
      org.opencontainers.image.licenses="GPL-3.0-or-later"

RUN apt-get update && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r aps2mqtt && useradd -r -g aps2mqtt aps2mqtt

COPY --from=builder /build/dist/aps2mqtt /app/

USER aps2mqtt
WORKDIR /app
CMD ["./aps2mqtt"]