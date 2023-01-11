echo '>>> Do migrations'
python app/manage.py makemigrations
python app/manage.py migrate


echo '>>> Create super user'
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python app/manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

$@
echo '>>> super user created'

echo '>>> Starting server and telegramm-bot'

python app/manage.py runserver 0.0.0.0:8000 & python app/manage.py runbot


