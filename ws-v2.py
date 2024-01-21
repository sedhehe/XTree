import pandas as pd
from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, storage

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(
    cred, {'storageBucket': 'genai-404319.appspot.com'})
db = firestore.client()


def scrape_data(data):
    link = data.get("url")
    tag = data.get("tag")
    cont = data.get("class_name")
    print(data)

    response = requests.get(link, timeout=10)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    results = []

    for a in soup.find_all(attrs={"class": cont}):
        for paragraph in a.find_all(tag):
            name = paragraph.text
            if name not in results:
                results.append(name)

    # Save results to CSV file
    df = pd.DataFrame({'Requested Data': results})
    df.to_csv("output.csv")

    bucket = storage.bucket()
    blob = bucket.blob("output.csv")
    blob.upload_from_filename("output.csv")
    blob.acl.all().grant_read()
    blob.make_public()

    return {"message": f"Scraping completed successfully! \n Download at: {blob.public_url}"}


print(scrape_data({
    "url": "https://en.wikipedia.org/wiki/Web_scraping",
    "tag": "a",
    "class_name": "mw-content-ltr mw-parser-output"
}))
