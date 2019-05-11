import requests
import json
import xml.etree.ElementTree as ET

#Variabler
#Søkstekst
Sted = input('Hvilket sted ønsker du å sjekke været for?\n')




def hentKoordinater(sokSted):
    #https://developer.here.com/api-explorer/rest/places/places-search-by-query
    #Nåværende sted (Standard er tilfeldig sted i Norge for bedre relaterte søk)
    xcor = '61.6638'
    ycor = '8.1171'
    stedHeader = "at={}%2C{}".format(xcor, ycor)

    #Søkstekst
    sokHeader = "q={}".format(sokSted)

    #app_id
    appId = 'DemoAppId01082013GAL'
    appIdHeader = "app_id={}".format(appId)

    #app_code
    appCode = 'AJKnXv84fjrb0KIHawS0Tg'
    appCodeHeader = "app_code={}".format(appCode)

    #Lager tilkoblingsurl
    url = "https://places.demo.api.here.com/places/v1/discover/search?{}&{}&{}&{}".format(stedHeader, sokHeader, appIdHeader, appCodeHeader)
    print(url)

    #Henter info
    respons = requests.get(url)
    resJSON = json.loads(respons.text)
    print(resJSON['results']['items'][0]['position'])
    xCorMaal = resJSON['results']['items'][0]['position'][0]
    yCorMaal = resJSON['results']['items'][0]['position'][1]

    #Returnerer koordinater
    return xCorMaal, yCorMaal

def hentVaer(posXCor, posYCor):
    #https://api.met.no/weatherapi/locationforecastlts/1.3/documentation
    xHeader = "lat={}".format(posXCor)
    yHeader = "lon={}".format(posYCor)

    url = "https://api.met.no/weatherapi/locationforecastlts/1.3/?{}&{}".format(xHeader,yHeader)
    print(url)

    #Henter vær-info
    print('Leser data:')
    respons = requests.get(url)
    resXML = ET.fromstring((respons.text))

    #Finner nyttige meldinger
    tempTid = ''
    tempNedbørTid = ''
    meldinger = []
    for item in resXML[1]:
        if item.attrib['to'] != tempTid:
            tempTid = item.attrib['to']
            tempNedbørTid = ''
            try:
                dict = {
                    "tid": item.attrib['to'],
                    "grader": item[0][0].attrib['value'],
                    "vindretning": item[0][1].attrib['name'],
                    "vind": item[0][2].attrib['name'],
                    "høyde": item[0].attrib['altitude'],
                    "xCor": item[0].attrib['latitude'],
                    "yCor": item[0].attrib['longitude']
                }
                #print(dict['tid'], dict['grader'])
                meldinger.append(dict)
            except Exception as e:
                print('err: {}'.format(item.attrib['to']) )
                print(e)
        elif item[0][0].tag == 'precipitation' and item.attrib['from'] >= tempNedbørTid:
            try:
                meldinger[-1]['nedbør'] = item[0][0].attrib['value']
                #meldinger[-1]['minnedbør'] = item[0][0].attrib['minvalue']
                #meldinger[-1]['maxnedbør'] = item[0][0].attrib['maxcalue']

                #print(meldinger[-1]['tid'], meldinger[-1]['grader'], meldinger[-1]['nedbør'])
            except Exception as e:
                print('err: {}'.format(item.attrib['to']) )
                print(e)
    return meldinger


resXCor, resYCor = hentKoordinater(Sted)
print(resXCor)
print(resYCor)

vaerMeldinger = hentVaer(resXCor, resYCor)
