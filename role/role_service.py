from . import role_repository


def get_role_by_id(role_id):
    return role_repository.get_role_by_id(role_id)
