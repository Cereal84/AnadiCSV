FROM python:3.11-alpine
LABEL authors="apischedda"

RUN mkdir anadi && mkdir -p /root/.config/anadi && mkdir /data/

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.


COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY anadi ./anadi
COPY docker/entrypoint.sh entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
