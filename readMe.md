## Steps to run in dev mode:

Requirements: Docker, python

1. Create an .env file (see env.example.txt)

2. Start services with `./dev up`
   That will create a postgres instance and a flask app running in port 5000

3. Stop services with `./dev down`

4. If this is your first time, apply migrations with `./dev migrate`

## TDD the heck out of it

`./dev test`
