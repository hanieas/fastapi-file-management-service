FROM python:3.11
 
WORKDIR /var/www

COPY /src ./

RUN pip install --no-cache-dir --upgrade -r /var/www/requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "8000"]