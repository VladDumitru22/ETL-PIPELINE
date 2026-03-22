import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

LOG_FILE = "log_file.txt"
TARGET_FILE = "transformed_data.csv"


def extract_from_csv(file_name):
    dataframe = pd.read_csv(file_name)
    return dataframe

def extract_from_json(file_name):
    dataframe = pd.read_json(file_name, lines=True) #lines=True to enable to read the file as a JSON object on line to line.
    return dataframe

def extract_from_xml(file_name):
    dataframe = pd.DataFrame(columns=["name", "height", "weight"])
    tree = ET.parse(file_name)
    root = tree.getroot()
    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)
        dataframe = pd.concat([dataframe, pd.DataFrame([{"name": name, "height": height, "weight": weight}])], ignore_index=True)
    return dataframe

def extract():
    #create an empty data frame
    extracted_data = pd.DataFrame(columns=["name", "height", "weight"]) 

    #process all csv files, excet the target file
    for csvfile in glob.glob("./source/*csv"):
        if csvfile != TARGET_FILE:
            extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_csv(csvfile))], ignore_index=True)

    #process all json files
    for jsonfile in glob.glob("./source/*.json"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_json(jsonfile))], ignore_index=True)

    #process all xml files
    for xmlfile in glob.glob("./source/*.xml"):
        extracted_data = pd.concat([extracted_data, pd.DataFrame(extract_from_xml(xmlfile))], ignore_index=True)
    
    #return all extracted data
    return extracted_data