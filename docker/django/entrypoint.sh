echo "Let's create django environment settings"
skey=`dd if=/dev/urandom bs=45 count=1 | base64`
echo "DJANGO_SECRET_KEY=$skey" > /sid/config/.env
cat /etc/environment >> ~/.bashrc
cd /sid/src/django/web
python manage.py runserver 0.0.0.0:8080