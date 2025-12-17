## Steps to run in dev mode:

Requirements: Docker

1. Create an .env file (see env.example.txt)

2. Start services with `docker compose up`

That will create a postres instance and a flask up running in port 5000

3. If this is your first time, apply migrations with `docker compose exec flask-app flask db upgrade`

## TDD the heck out of it

`sh run_tests.sh`
