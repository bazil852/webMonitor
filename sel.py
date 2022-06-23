from numpy import source
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
from collections import defaultdict
import requests
from discord import Webhook, RequestsWebhookAdapter
import time

chrome_options = Options()
#chrome_options.add_argument("--headless")

# https://github.com/ZeframLou - Look for the word “ve” , “partner” , “partnership” , “launch date”
# Https://governance.aave.com - Look for the word “ve” , “partnership” “partner”
# https://github.com/andrecronje - Look for the word “buyback” , “launch” , “new” , “partnership” , “partner” , “ contract address”
# https://substack.com/profile/8555922-cobie - Look for the word “token”
# https://github.com/andrecronje/crv.finance - Look for the word “ve” , “partnership” “partner”
# https://github.com/andrecronje/synthetix - Look for the word “ve” , “partnership” “partner”
# https://github.com/andrecronje/cream-docs - Look for the word “ve” , “partnership” “partner” , “buyback”
# https://github.com/andrecronje/yearn-vaults - Look for the word “ve” , “partnership” “partner” , “buyback”
# https://github.com/andrecronje/compound-protocol Look for the word “ve” , “partnership” “partner” , “buyback”
url_list=['https://forum.balancer.fi/',
    'https://github.com/ZeframLou',
    'Https://governance.aave.com'
    'https://github.com/andrecronje',
    'https://substack.com/profile/8555922-cobie',
    'https://github.com/andrecronje/crv.finance',
    'https://github.com/andrecronje/synthetix',
    'https://github.com/andrecronje/cream-docs',
    'https://github.com/andrecronje/yearn-vaults',
    'https://github.com/andrecronje/compound-protocol'
]

text_list=[['ve','partner','partnership'],
    ['ve','partner','partnership','launch date'],
    ['ve','partner','partnership'],
    ['buyback','launch','new','partnership','partner','contract address'],
    ['token'],
    ['ve','partner','partnership'],
    ['ve','partner','partnership'],
    ['ve','partner','partnership','buyback'],
    ['ve','partner','partnership','buyback'],
    ['ve','partner','partnership','buyback']
    ]

def string_found(string1, string2):
   if re.search(r"\b" + re.escape(string1) + r"\b", string2):
      return True
   return False

driver = webdriver.Chrome(options=chrome_options)
dic=defaultdict(lambda: defaultdict(dict))
sourceUpdate=True
filesUpdate=False
startTime=time.time()
count=0
while (True):
    print (count)
    if (sourceUpdate==True):
        i=0
        for url in url_list:
            try:
                f = open("source"+str(i)+".html")
                print ("Working on: "+"file://C:/Users/Lenovo T14/Documents/jo/sel/source"+str(i)+".html")
                driver.get("file://C:/Users/Lenovo T14/Documents/jo/sel/source"+str(i)+".html")
                get_source = driver.page_source
                for word in text_list[i]:
                    if (string_found(word,get_source)):
                        dic[url][word]=len(re.findall(word, get_source))
                        

            except FileNotFoundError:
                print(url, "  is page down")
            i+=1
        sourceUpdate=False
    else:
        i=0
        for url in url_list:
            try:
                driver.get(url)
                print("Working on: ",url)
                get_source = driver.page_source
                if (count%3000==0 or count==0):
                    print ("=================Updateing Files=====================")
                    f = open(("source"+str(i)+".html"), "a", encoding="utf-8")
                    f.write(get_source)
                    f.close()
                else:
                    for word in text_list[i]:
                        if (string_found(word,get_source)):
                            newLen=len(re.findall(word, get_source))
                            if (newLen>dic[url][word]): 
                                print(word,'  is preseent in URL: ',url)
                                webhook = Webhook.from_url("https://discord.com/api/webhooks/989480958162006027/8o0Y3p62FkGt_lyoKcP28Hztc8Y6B6OvSwNZS0KO1XqDhTwZVQoCNbRyeLRf0YTpERfm", adapter=RequestsWebhookAdapter()) 
                                webhook.send(word+" PRESENT ON URL: "+url)
                                dic[url][word]=newLen
            except WebDriverException:
                print(url, "  is page down")
        
            i+=1
    count+=1
        

    