# fabtecuida_api

> FABTECT API for FABTECuida project.

### Usage

```
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser --email admin --username admin

python manage.py runserver
```

* Django Admin namespace: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* Api namespace: [http://localhost:8000/api/](http://localhost:8000/api/)

### Resources

* https://docs.djangoproject.com/en/3.0/
* https://www.django-rest-framework.org/
* https://github.com/SimpleJWT/django-rest-framework-simplejwt
