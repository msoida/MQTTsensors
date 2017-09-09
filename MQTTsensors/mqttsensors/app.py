from .settings import location


if location == 'home':
    from .home import upload_sensors
elif location == 'domek':
    from .domek import upload_sensors
