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
