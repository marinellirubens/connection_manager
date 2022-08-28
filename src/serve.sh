WORK_DIR=$1
if [ -z "$1"]; then
    WORK_DIR=$(pwd)
fi
echo "Initiating gunicorn using directory: $WORK_DIR"

gunicorn \
--chdir ./src \
--log-config ./config/gunicorn.logs.conf \
--env ADMIN_PASSWORD=admin \
--env TESTE=asd \
--config ./src/config/gunicorn.conf.py "main:main(cwd='$WORK_DIR')" 