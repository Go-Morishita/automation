import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

API_ENDPOINT = os.getenv("WORDPRESS_API_ENDPOINT")
WP_USERNAME = os.getenv("WORDPRESS_USERNAME")
WP_APP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD")

def create_post(data):    
    acf = data.get("acf")
    if isinstance(acf, dict):
        acf["overviewimage"] = None
        
    response = requests.post(
        API_ENDPOINT,
        json=data,
        auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD),
        timeout=30,
    )

    if response.status_code in (200, 201):
        print("投稿成功")
        print(response.json())
    else:
        print("投稿失敗:", response.status_code)
        print(response.text)

if __name__ == "__main__":
    create_post()
