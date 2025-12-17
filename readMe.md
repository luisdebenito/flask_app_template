## Steps to run in dev mode:

Requirements: Docker, python

1. Create an .env file (see env.example.txt)

2. Start services with `python dev.py up`

3. Stop services with `python dev.py down`

That will create a postres instance and a flask up running in port 5000

3. If this is your first time, apply migrations with `python dev.py migrate`

## TDD the heck out of it

`python dev.py test`
