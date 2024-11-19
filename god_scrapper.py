import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import csv
import time

filename = "vulnerabilities.csv"
rows = []

driver = webdriver.Firefox()

def nvidia():
    row_data = []
    driver.get('https://www.nvidia.com/en-us/security/')
    time.sleep(3)

    # Reject cookies popup if necessary
    element = driver.find_element(By.ID, "onetrust-reject-all-handler")
    element.click()
    
    html = driver.page_source
    soup = bs(html, 'html.parser')

    # Find the vulnerability table
    table = soup.find('table', class_='responsive compare-table')
    
    for row in table.tbody.find_all('tr', class_='content'):
        columns = row.find_all('td')
        if columns:
            prod_name = columns[0].text.strip()  # Product name
            prod_ver = "N/A"  # Version
            oem = "NVIDIA"  # OEM
            vuln = columns[3].text.strip()  # Vulnerability description
            sev = columns[2].text.strip()  # Severity level
            mit_strat = columns[0].a['href'] if columns[0].a else "N/A"  # Mitigation strategy (link)
            pub_date = columns[4].text.strip()  # Published date
            unique_id = columns[5].text.strip() if len(columns) > 5 else "N/A"  # UniqueID (e.g., CVE)
            
            row_data.append([prod_name, prod_ver, oem, sev, vuln, mit_strat, pub_date, unique_id])
    
    return row_data

nvidia_data = nvidia()

with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['ProductName', 'Version', 'OEM', 'SeverityLevel', 'Vulnerability', 'MitigationStrategy', 'PublishedDate', 'UniqueID'])
    
    csvwriter.writerows(nvidia_data)

driver.quit()
