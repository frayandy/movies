Movies service
==============
Service is created to render Movies with peoples from Ghibli API

Checkout
---
    git clone https://github.com/frayandy/movies.git
    
Run service
---
    python3 -m venv /path/to/env
    . /path/to/env
    pip install -r requirements/requirements.txt
    APP_ENV=prod python manage.py runserver -h <host> -p <port>
  
Run unittests
---
    python3 -m venv /path/to/env
    . /path/to/env
    pip install -r requirements/test_requirements.txt
    APP_ENV=test pytest -x --ff tests/
