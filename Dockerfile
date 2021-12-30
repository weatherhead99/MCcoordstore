FROM python:3.9-slim-bullseye as base
FROM base as builder
WORKDIR /app
COPY . .
RUN python3 setup.py bdist_wheel

FROM base
COPY --from=builder /app/dist/MCcoordstore-*-py3-none-any.whl  /app/
WORKDIR /app
ENV PYTHONDONTWRITEBITECODE 1
ENV PYTHONUNBUFFERED 1
RUN groupadd -r app -g 433 && \
    useradd -u 431 -r -g app -s /sbin/nologin -c "Docker Image User" app \
    && mkdir /home/app && chown app:app /home/app
USER app
RUN pip install --no-cache-dir gunicorn
RUN pip install ./MCcoordstore-*-py3-none-any.whl --no-cache-dir
ENV PATH /home/app/.local/bin
ENTRYPOINT ["gunicorn", "MCcoordstore.app:app", "--worker-tmp-dir=/dev/shm", "--log-file=-"]
CMD ["-w 4", "-t 4", "-k gthread", "-b 0.0.0.0:5000"]

