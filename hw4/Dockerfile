FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock


RUN pip install pipenv && cd /app && pipenv install --deploy --system

#COPY model2.bin /app/model2.bin
#COPY model.bin /app/model.bin
COPY starter.py /app/starter.py

RUN python starter.py 2023 5

