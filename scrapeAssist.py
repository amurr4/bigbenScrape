from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

print("This .py is working!")

## we dont need DEFENSE anymore ONLY PASSING, RUSHING, FUMBLE so fix that tmr 
def scrapePage(url,year):
    yr_table=[]
    yr_table_titles=[]

    try:
        client = uReq(url)
        pg = client.read()  # Entire HTML page
        client.close()
        page_soup=soup(pg,features="lxml")

        #Find Data
        subtitles=page_soup.findAll('h3',{"class":"d3-o-section-sub-title"}) # Subsection (Opponents by team)
        for item in subtitles:
            clean_section=item.text.strip()
            if clean_section == "Opponents by Team": 
            # Assuming current_subtitle is found, find the parent element of the subtitle
                parent_div = item.find_parent()
                parent_div_id=parent_div.find_parent(id=True).get('id')
                # Find the next table within the same parent element
                table = parent_div.find_next('table')
                frame=makeDF(table,year,parent_div_id)
                yr_table.append(frame)
                yr_table_titles.append(parent_div_id)
        
        return yr_table,yr_table_titles
    
    except Exception as e:
        print("Error:", e)
        return None

# Pass in the table and the year to create a data frame
def makeDF(table,year,type):
    headers = []
    for i in table.find_all('th'):
                    title = i.text.strip()
                    headers.append(title)

    headers.append('Year')
    mydataframe = pd.DataFrame(columns = headers)

    # Create a for loop to fill mydataframe
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text.strip() for i in row_data]
        row.append(year)
        length = len(mydataframe)
        mydataframe.loc[length] = row

    return mydataframe



    




