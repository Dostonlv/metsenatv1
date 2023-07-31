run:
	python3 manage.py runserver

mkmgr:
	python3 manage.py makemigrations

mgr:
	python3 manage.py migrate

spruser:
	python3 manage.py createsuperuser