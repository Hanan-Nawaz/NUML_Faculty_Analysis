import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract():
    try:
        #URL of Webpages from NUML Offical Website
        numl_se_url = "https://www.numl.edu.pk/department/273/faculty"
        numl_cs_url = "https://www.numl.edu.pk/department/178/faculty"

        #getting content from URLS
        numl_se_req = requests.get(numl_se_url)
        numl_cs_req = requests.get(numl_cs_url)

        #combing both contents
        combined_faculty = numl_cs_req.content + numl_se_req.content

        # parsing content with BS4
        bsoup = BeautifulSoup(combined_faculty, 'html.parser')

        #finding cards with details
        div_cards = bsoup.find_all('div', {'class': 'courses-wrap'})

        #dataframe to store data
        df_faculty = pd.DataFrame(columns=["Name", "Details", "Dept", "Designation", "Link"])

        #list to store data
        faculty_data = []

        #getting needed data from html
        for data in div_cards:
            main_div = data.find('div', {'class': 'course-content'})
            f_name = main_div.find('h3').find('a').get_text(strip=True)
            f_details = main_div.find('p').get_text(strip=True)
            f_dept = data.find('span', {'class': 'course-instructor'}).get_text(strip=True)
            f_designation = data.find('p', {'class': 'years'}).get_text(strip=True)
            f_link = main_div.find('h3').find('a')['href']
            faculty_data.append({"Name": f_name, "Details": f_details, "Dept": f_dept, "Designation": f_designation, "Link": f_link})

        #adding data to Dataframe
        for data in faculty_data:
            df_faculty = df_faculty._append(data, ignore_index=True)

        #loading data into csv for Transformation phase
        df_faculty.to_csv('DataSets/faculty.csv')
        
        print("Extraction Completed Successfully!")
    
    except requests.exceptions.ConnectionError:
        print("Error! Extraction Failed")


extract()