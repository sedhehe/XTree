import os
from firebase_functions import https_fn
from firebase_admin import initialize_app
import pandas as pd
from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(
    cred, {'storageBucket': 'genai-404319.appspot.com'})
db = firestore.client()


@https_fn.on_call()
def scrape(req: https_fn.CallableRequest):
    print("on call function data:", req)
    link = req.data["url"]
    tag = req.data["tag"]
    cont = req.data["cont"]
    fname = req.data["fname"]

    response = requests.get(link, timeout=10)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    results = []

    for a in soup.find_all(attrs={"class": cont}):
        for paragraph in a.find_all(tag):
            name = paragraph.text
            if name not in results:
                results.append(name)

    df = pd.DataFrame({'Requested Data': results})
    df.to_csv(f"{fname}.csv")
    bucket = storage.bucket()
    blob = bucket.blob(f"{fname}.csv")
    blob.upload_from_filename(f"{fname}.csv")
    blob.acl.all().grant_read()
    blob.make_public()
    os.remove(f"{fname}.csv")

    print(
        f"Scraping completed successfully! \n Download at: {blob.public_url}")
    return {"message": blob.public_url}
