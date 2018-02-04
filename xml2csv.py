from  xml2df import XML2DataFrame

user_agent_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/loan?date=201707'
outputFileName = '3.3-Loans201707.csv'

if __name__ == "__main__":
    import requests
    try:
        r = requests.get(user_agent_url, timeout=None)
        r.raise_for_status()
        print(r)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


    xml_data = r.content

    if len(xml_data) > 0:

        xml2df = XML2DataFrame(xml_data)
        xml_dataframe = xml2df.process_data()
        xml_dataframe.to_csv(outputFileName, index=False, sep=';', encoding='cp1251', decimal=',')
    else:
        print("Length of the answer is Zero")
