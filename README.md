[![api style and tests](https://github.com/otzhora/science-reader/actions/workflows/api-workflow.yml/badge.svg)](https://github.com/otzhora/science-reader/actions/workflows/api-workflow.yml)

# This is my graduation assignment from the python course

## How to run this

First, run this

```
cp .env.example .env
docker-compose build
docker-compose run api flask init-db
docker-compose up 
```

Now somewhere (hopefully on localhost) on port 5000 is cozy
