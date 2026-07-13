from Lm.crpyto_utills import decrypt_token
import requests
def get_github_script(user):
    git = bool(
        user.github_repo
        and user.github_path
        and user.github_owner
        and user.github_token
    )
    if git:
        repo=user.github_repo
        owner=user.github_owner
        path=user.github_path
    else:
        return []
    