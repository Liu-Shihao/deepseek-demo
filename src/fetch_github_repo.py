import requests



def fetch_content():
    url = "https://api.github.com/repos/Liu-Shihao/deepseek-demo/contents"

    payload = {}
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer <TOKEN>',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
