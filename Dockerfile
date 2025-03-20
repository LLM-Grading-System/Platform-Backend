FROM python:3.11-slim AS base

FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project --no-dev

FROM base AS production
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY /src /app/src
EXPOSE 8000
CMD ["granian", "--interface", "asgi", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
