import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

link = input("URL: ")
driver = webdriver.Chrome()
driver.get("https://"+link)
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
results = []

tag = input("Tag: ")
cont = input("class name: ")
for a in soup.find_all(attrs={"class": cont}):
    for paragraph in a.find_all(tag):
        name = paragraph.text
        if name not in results:
            results.append(name)

df = pd.DataFrame({'Requested Data': results})
fname = input("Enter file name: ")
df.to_csv(fname+".csv")

driver.quit()
