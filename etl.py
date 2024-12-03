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

def transform():
    #getting data from CSV
    df_faculty = pd.read_csv("DataSets/faculty.csv", usecols=["Name", "Details", "Dept", "Designation", "Link"])
    
    #start index from 0
    df_faculty.index = range(1, len(df_faculty) + 1) 

    #extracting email from details, Phone number of all are same with almost 6 different Extensions for All Teachers
    df_faculty.insert(2, "Email", df_faculty["Details"].str.extract(r"([a-zA-Z_.+]+@[a-zA-Z-]+\.[a-zA-Z-.]+)"))
    
    #removing extra details from name
    df_faculty["Name"] = df_faculty["Name"].str.split('(').str[0]

    #adding column for Phd on the base of Dr. in name
    df_faculty.insert(6, "Phd", df_faculty["Name"].str.contains("Dr."))

    #removing different designations
    df_faculty["Designation"] = df_faculty["Designation"].str.split('(').str[0].str.split('/').str[0].str.split('&').str[0]
    df_faculty["Designation"] = df_faculty["Designation"].replace("Acting Director IT, ", "Assistant Professor")
    df_faculty["Designation"] = df_faculty["Designation"].replace("Coordinator ", "Lecturer")
    df_faculty["Designation"] = df_faculty["Designation"].replace("Head of Department", "Associate Professor")
    df_faculty["Designation"] = df_faculty["Designation"].replace("Associate Lecturer", "Lecturer")
    df_faculty["Designation"] = df_faculty["Designation"].str.strip()
    df_faculty["Designation"] = df_faculty["Designation"].replace("Associate  Professor", "Associate Professor")
    
    #deleting details column 
    df_faculty = df_faculty.drop(columns=["Details"])

    # print(df_faculty["Designation"].unique()) checking unique designations (TESTING ONLY)
    print("Transformation Completed Successfully!")

    return df_faculty
    
def load(df_transformed):
    df_transformed.to_csv('DataSets/faculty.csv')
    print("Loading Completed Successfully!")

def main():  
    extract()
    df_transformed = transform()
    load(df_transformed)

if __name__ == "__main__":
    main()
