from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from sortedcontainers import SortedSet
import re
import time
import datetime
import smtplib
from email.message import EmailMessage

def sendEmail():
    sender_email = "sender_email"
    rec_emails = {"rec_emails"}
    password = "password"
    message = f"The after-hours lab sign-up sheet has updated."

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    for rec_email in rec_emails:
        server.sendmail(sender_email, rec_email, message)
    server.quit()

sheetUrl = "https://app.smartsheet.com/b/publish?EQBCT=1fb10103a37c4383b3e11b5e50c5a50d"
options = Options()
options.headless = True
options.add_argument("window-size=1920x1480")
options.add_argument("disable-dev-shm-usage")
def getDates(url):
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    driver.get(url)
    time.sleep(5)
    page = driver.find_element_by_tag_name('html')
    html = driver.page_source # Here is your populated data.

    # Now, we could simply apply bs4 to html variable 
    soup = BeautifulSoup(html, "html.parser")
    date_divs = set(soup.find_all('div', text=re.compile('.:.'), attrs={'class' : "gridCellContent"}))

    for x in range(0,10):
        page.send_keys(Keys.PAGE_DOWN)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        other_divs = set(soup.find_all('div', text=re.compile('.:.'), attrs={'class' : "gridCellContent"}))
        for div in other_divs:
            date_divs.add(div)
    driver.quit()

    dates = SortedSet()
    for div in date_divs:
        dates.add(div.text)
    return dates

prev_dates = getDates(sheetUrl)
while True:
    new_dates = getDates(sheetUrl)
    ct = datetime.datetime.now()
    print("--------------------------------")
    print("LAST COMPARISON:", ct)
    print("Previous dates: ", prev_dates)
    print("New Dates:      ", new_dates)
    if (prev_dates != new_dates):
        print("Dates changed")
        sendEmail()
    else:
        print("No change in Dates")
    print("--------------------------------")
    prev_dates = new_dates
    time.sleep(300)