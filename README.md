# Setup

```bash
$ docker compose run --rm app pipenv install
$ docker compose run --rm app pipenv run python manage.py migrate
```

# Run

```bash
$ docker compose up -d
```

Open http://localhost:8000

# Stop

```bash
$ docker compose down
# or faster
$ docker compose kill && docker compose rm -f 
```

# Logs

```bash
$ docker compose logs -f
```