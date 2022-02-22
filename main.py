import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os

EMAIL = os.environ["email"]
PASSWORD = os.environ["password"]
TO_EMAIL = os.environ["to_email"]

URL = "https://www.amazon.com/Samsung-Galaxy-Single-Factory-Unlocked/dp/B09GT79LPT/ref=sr_1_3?crid=3ATYYMZ2ZCW22&keywords=flip+3&qid=1645486612&refinements=p_n_condition-type%3A6503240011&rnid=6503239011&s=wireless&sprefix=flip+%2Caps%2C631&sr=1-3"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.62",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(URL, headers=headers)
contents = response.text

soup = BeautifulSoup(contents, "lxml")
price = soup.find(name="span", class_="a-offscreen").text
price_without_currency = float(price.split("$")[1])  # needed for comparison later
print(price)
print(price_without_currency)

item_title = soup.find(name="span", id="productTitle").text.strip()
print(item_title)

if price_without_currency < 750:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=TO_EMAIL,
            msg=f"SUBJECT: LOW PRICE!!\n\n{item_title} is now {price} \n {URL}".encode("utf-8")
        )
