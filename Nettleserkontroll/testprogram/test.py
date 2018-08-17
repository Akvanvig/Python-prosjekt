#Åpner opp nettleser ved hjelp av selenium, og åpner gitt nettside
#Merk at geckodriver må ligge i Path-variabel på windows (her c:/python)
from selenium import webdriver
browser = webdriver.Firefox() #Åpner nettleser vindu
browser.get('https://github.com/akvanvig')
