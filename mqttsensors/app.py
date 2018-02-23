from .settings import location


if location == 'home':
    from .home import upload_list
elif location == 'pitv':
    from .pitv import upload_list
elif location == 'domek':
    from .domek import upload_list
