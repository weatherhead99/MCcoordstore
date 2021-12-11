FROM python:3.9-slim-bullseye as base
FROM base as builder
WORKDIR /app
COPY . .
RUN python3 setup.py bdist_wheel

FROM base
COPY --from=builder /app/dist/MCcoordstore-0.0.1.dev0-py3-none-any.whl  /app/
WORKDIR /app
RUN pip install ./MCcoordstore-0.0.1.dev0-py3-none-any.whl --no-cache-dir
RUN pip install --no-cache-dir gunicorn
CMD ["gunicorn", "-w 4", "MCcoordstore.app:app"]

