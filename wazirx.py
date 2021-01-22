### Importing necessary modules

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
import re

from selenium.webdriver.common.keys import Keys

capital =2500

path = "chromedriver.exe"
driver = webdriver.Chrome(path)

wazirx_eth_inr = "https://wazirx.com/exchange/BTC-INR"
wazirx_eth_usdt = "https://wazirx.com/exchange/BTC-USDT"
wazirx_eth_btc = "https://wazirx.com/exchange/BTC-USDT"
whatsapp_web = "https://web.whatsapp.com/"

list_inr = {}
list_usdt = {}

driver.get(wazirx_eth_inr)


wait = WebDriverWait(driver, 20)
inr=wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ticker-item')))

for item in inr:
    text = item.text
    coin_inr = re.findall(r'^[A-Z]+', text)
    price_inr = text.split('₹')
    price_inr = price_inr[1]
    price_inr = price_inr.split(",")
    price_inr = "".join(price_inr)

    list_inr[coin_inr[0]] = float(price_inr)
print(list_inr)

wait = WebDriverWait(driver, 10)
sad =wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'buy')))
j = 0
for i in sad:
    i = i.text
    break
buy_price = i.split('\n')
buy_price = buy_price[0]
buy_price = buy_price.split(' ')
buy_price, buyable_amount = buy_price[1], buy_price[0]
print(f'There is {buyable_amount} BTC to be bought at {buy_price}')

wait = WebDriverWait(driver, 10)
crypto =wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sell')))
j = 0
for i in crypto:
    i = i.text
    break
sell_price = i.split('\n')
sell_price = sell_price[0]
sell_price = sell_price.split(' ')
sell_price, sellable_amount = sell_price[1], sell_price[0]
print(f'There is {sell_price} BTC to be sought at {sellable_amount}')

driver.get(wazirx_eth_usdt)
wait = WebDriverWait(driver, 10)
usdt =wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ticker-item')))

for item in usdt:
    text = item.text
    coin_usdt = re.findall(r'^[A-Z]+', text)
    if coin_usdt[0] in list_inr.keys():
        price_usdt = text.split('₹')
        price_usdt = price_usdt[1]
        price_usdt = price_usdt.split(",")
        price_usdt = "".join(price_usdt)
        list_usdt[coin_usdt[0]] = float(price_usdt)
print(list_usdt)

usdt_price = list_inr.get("USDT")
transaction_fee = .002*capital


for key in list_inr:
    inr_base = list_inr.get(key)


    usdt_base = list_usdt.get(key)




    if inr_base != None and usdt_base != None:
        coin_content_inr = capital/inr_base
        #print(key,coin_content_inr)
        coin_content_usdt = capital/usdt_base
        #print(key, coin_content_usdt)
        #print(f"you can buy {coin_content_inr} {key} @{inr_base} ")
        #print(f"you can buy {coin_content_usdt} {key} @{usdt_base} ")

       # If price of coin in inr is low:
        if coin_content_inr > coin_content_usdt:

            total_worth_in_usd = coin_content_inr*usdt_base
            #print("total amount in inr with usdtoken", total_worth_in_usd)
            after_2_transaction = total_worth_in_usd - (2*transaction_fee)
            #print("after_3_transaction", after_3_transaction)

            if after_2_transaction > capital:

                print(f"Buy {coin_content_inr} {key} at {inr_base} INR ")
                print(f"sell {coin_content_inr}{key} at {usdt_base} INR in USDT ")
                print(f"You'll  have  {after_2_transaction}  worth of USDT")

                earnings = (after_2_transaction/usdt_price)
                profit = after_2_transaction - capital
                print(f"At the current market you'll have {earnings} USDT worth {after_2_transaction} INR after all transaction with a profit of {profit} INR")


            else:
                print(f"Buy {coin_content_usdt} {key} at {coin_content_usdt/usdt_price} USDT ")
                print(f"sell {coin_content_usdt}{key} at {inr_base} INR ")

                print(f"You'll  have  {after_2_transaction} INR")


                profit = after_2_transaction - capital
                print(f"At the current market you'll have {after_2_transaction} INR after all transaction with a profit of {profit} INR")

driver.close()