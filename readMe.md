## Steps to run in dev mode:

Requirements: Docker

1. Create an .env file (see env.example.txt)

2. Start services with `make up`
   That will create a postgres instance and a flask app running in port 5000

3. Stop services with `make down`

4. If this is your first time, apply migrations with `make migrate`

## TDD the heck out of it

`make test`
