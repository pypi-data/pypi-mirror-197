from .python_util import execute

def gopass_field_from_path (path, field):
    credential = None
    if path and field:
        print('get field for: ' + path + ', ' + field)
        credential = execute(['gopass', 'show', path, field])
    return credential

def gopass_password_from_path (path):
    credential = None
    if path:
        print('get password for: ' + path)
        credential = execute(['gopass', 'show', '--password', path])
    return credential
