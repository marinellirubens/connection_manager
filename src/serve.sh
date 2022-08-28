gunicorn \
--chdir . \
--log-config config/gunicorn.logs.conf \
--env ADMIN_PASSWORD=admin \
--env TESTE=asd \
--config config/gunicorn.conf.py "main:main()" 