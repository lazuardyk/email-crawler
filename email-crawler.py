import requests
import re
from fake_useragent import UserAgent
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

print("Email Crawler\nCreated by Lazuardy Khatulistiwa\n")
keyword = input("Keyword:\n")
batas = int(input("How much of Bing page you want to scrape?: (example: 15)\n"))
print("\nProcessing...")
ua = UserAgent(verify_ssl=False)
angka = 1
batas = batas*10
links = set()
emails = set()
email_regex = re.compile('([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})', re.IGNORECASE)
url_regex = re.compile('<a\s.*?href=[\'"](.*?)[\'"].*?>')
while angka < batas:
    reqbing = requests.get("https://www.bing.com/search?q="+keyword+"&first="+str(angka), headers={'User-Agent':ua.random})
    regexlink = re.findall(r'<h2><a href="(.*?)" h="ID', reqbing.text)
    for x in regexlink:
        links.add(x)
    angka += 10
print("Link count:"+str(len(links))+"\n")
for link in links:
    linksin = list()
    warnings.simplefilter('ignore',InsecureRequestWarning)
    try:
        requrl = requests.get(link, headers={'User-Agent':ua.random}, timeout=3, verify=False)
        print("Processing web => "+link)
        for email in email_regex.findall(requrl.text):
            emails.add(email)
        try:
            for linkcuy in url_regex.findall(requrl.text):
                reqlagi = requests.get(linkcuy, headers={'User-Agent':ua.random}, timeout=3, verify=False)
                print("Processing page => "+linkcuy)
                for email in email_regex.findall(reqlagi.text):
                    emails.add(email)
        except:
            pass
    except:
        pass
print("\nEmail total:"+str(len(emails)))
for imel in emails:
    file = open('results.txt', 'a')
    file.write(imel+'\n')
file.close()
input("Done.")
