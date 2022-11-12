FROM python:3.9.15-bullseye

WORKDIR /app

RUN python -m pip install --no-cache-dir --upgrade pip setuptools

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN rm requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
