from database import User, Lock


def user_has_access(user: User, lock: Lock) -> bool:
    """
    Checks to see if the provided user has the ability to unlock the provided lock.

    return: True if the user can unlock the lock, false otherwise
    """
    return user.user_id in [accepted_user.user_id for accepted_user in lock.accepted_users]
