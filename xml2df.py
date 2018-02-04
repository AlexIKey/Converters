# Gather XML Data


import xml.etree.ElementTree as ET
import pandas as pd


class XML2DataFrame:

    def __init__(self, xml_data):
        self.root = ET.XML(xml_data)

    def parse_root(self, root):
        return [self.parse_element(child) for child in iter(root)]

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()
        for key in element.keys():
            parsed[key] = element.attrib.get(key)
        if element.text:
            parsed[element.tag] = element.text
        for child in list(element):
            self.parse_element(child, parsed)
        return parsed

    def process_data(self):
        structure_data = self.parse_root(self.root)
        return pd.DataFrame(structure_data)

if __name__ == "__main__":
    import requests
    user_agent_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/loan?date=201708'
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
        outputFileName = '3.3-Loans201708.csv'
        xml2df = XML2DataFrame(xml_data)
        xml_dataframe = xml2df.process_data()
        xml_dataframe.to_csv(outputFileName, index=False, sep=';', encoding='cp1251', decimal=',')
    else:
        print("Length of the answer is Zero")
