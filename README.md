[![api style and tests](https://github.com/otzhora/science-reader/actions/workflows/api-workflow.yml/badge.svg)](https://github.com/otzhora/science-reader/actions/workflows/api-workflow.yml)

# This is my graduation assignment from the python course

## How to run this

First, create venv and install dependecies 
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

If `manage.py` is not executable you need to do
```
chmod 755 manage.py
```

Then build containers and initialize database 
```
./manage.py compose build
./manage.py compose run migrations
./manage.py create-initial-db
./manage.py compose down
```

Now you are ready to run this
```
./manage.py compose up -d
```
