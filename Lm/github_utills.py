from Lm.crpyto_utills import decrypt_token
import requests
def get_github_script(user):
    git = bool(
        user.github_repo
        and user.github_owner
        and user.github_token
    )
    if git:
        repo=user.github_repo
        owner=user.github_owner
        path=user.github_path or ""
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

        palintext=decrypt_token(user.github_token)
        headers = {
            "Authorization": f"token {palintext}",
            "Accept": "application/vnd.github.v3+json" 
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            items = response.json()
            scripts = []
            count =0
            for item in items:
                if item["type"] == "file" and item["name"].endswith('.py'):
                    script = {
                        'name': item['name'],
                        'description': "Github Script",
                        'url': item['html_url'],
                        'status': "Ok"
                    }
                    scripts.append(script)
                    count=count+1
            return scripts,count
        else:

            return [],0
    else:
        return [],0
    