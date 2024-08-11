FROM python:3.11

WORKDIR /var/www

COPY /src ./
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN pip install --no-cache-dir --upgrade -r /var/www/requirements.txt \
    && pip install supervisor

# Start supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
