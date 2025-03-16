FROM python:3.11-slim as base

FROM base AS dev
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project
EXPOSE 8000
CMD ["uv", "run", "fastapi", "dev", "src/app.py", "--port", "8000", "--host", "0.0.0.0", "--reload"]
