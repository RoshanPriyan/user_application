user_app/
    |- api/
        |- user/
            |- views/   -> contain api logic
                |- __init__.py
                |- register_api.py
            |- models.py    -> contain user related models
            |- routers.py   -> contain user related router
            |- schemas.py   -> contain user related schema
            |- __init__.py
        |- __init__.py
    |- __init__.py
    |- package/     ->environment contain all packaged related to this application
    |- database.py  -> db connective
    |- main.py      -> fastapi application instance
    |- readme.txt   -> contain project structure
    |- requirements.txt     -> application requirement
    |- background_task/ this directory all related to celery
        |- celery.py
        |- beat_schedule.py
        |- example_tasks.py
        |- __init__.py


celery command to run in terminal
worker=>  celery -A background_task.celery_app.celery_app worker --loglevel=info --pool=solo
beat=> celery -A background_task.celery_app.celery_app beat --loglevel=info

db migration command
PS C:\Program Files\MySQL\MySQL Server 8.0\bin> .\mysqldump.exe -u root -p user_app > "$HOME\backup.sql"