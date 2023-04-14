#ik vai noob ne code kiya hai...

import requests, re
from requests_html import HTMLSession

def getHTML(url):
    session = HTMLSession()
    response = session.get(url)

    # Render the JavaScript on the page
    response.html.render(timeout=30)

    # Get the rendered HTML
    html = response.html.html
    if "Something went wrong" in html or "You might be having a network connection problem, the link might be expired, or the payment provider cannot be reached at the moment." in html:
        return None
    else:
        return html

def getPK(html):
    regex="pk_live_[0-9a-zA-Z]{99}|pk_live_[0-9a-zA-Z]{34}|pk_live_[0-9a-zA-Z]{24}"
    try:
        return re.findall(regex, html)[0]
    except Exception as e:
        return "Not Found"

def getCS(data):
    regex="cs_live_[0-9a-zA-Z]{58}"
    try:
        return re.findall(regex, data)[0]
    except:
        return "Not Found"
def getRawData(pk, cs):
    h={
    "Host": "api.stripe.com",
    "sec-ch-ua": "\"Chromium\";v\u003d\"112\", \"Google Chrome\";v\u003d\"112\", \"Not:A-Brand\";v\u003d\"99\"",
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "dnt": "1",
    "sec-ch-ua-mobile": "?1",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua-platform": "\"Android\"",
    "origin": "https://checkout.stripe.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://checkout.stripe.com/",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7,hi;q\u003d0.6"
    }
    data=f"key={pk}&eid=NA&browser_locale=en-IN&redirect_type=url"
    url=f"https://api.stripe.com/v1/payment_pages/{cs}/init"
    req=requests.post(url, data=data, headers=h)
    if req.status_code==200:
        return req.json()
    return None

ok=getRawData("pk_live_51Km0kNF7uqYzKRQ39SjLw6OJaIdigSVgAceFTUmtbBxNVqVC16iyeDQcNZCwzI2H4HEcgSDjYkvcInfLfUDP2P8P00s28rE6nG","cs_live_a1QlGP9xvWHvoFN3qmCd5sj1CXFaX7zOdvyqLCVSREc1FSf3sC8fbBmJd7")

def getEmail(raw):
    email=raw.get("customer_email", "Not Found")
    return email

def getAmt(raw):
    try:
        amt=raw.get("line_item_group", {}).get("line_items", {})[0].get("total", "Not Found")
        return str(amt)
    except:
        return "Not Found"

def getCurrency(raw):
    try:
        c=raw.get("line_item_group", {}).get("currency", "Not Found")
        return c
    except:
        return "Not Found"


url=input("Enter Checkout Link:    ")
html=getHTML(url)
if html==None:
    print("Session Expired!")
    exit()
pk=getPK(html)
print(pk)
cs=getCS(url)
print(cs)

raw=getRawData(pk, cs)

print(getEmail(raw))
print(getAmt(raw))
print(getCurrency(raw))
