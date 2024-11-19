
# VulScrapper
VulScrapper is a Python-based web scraping tool that collects vulnerability data from web pages. It stores the extracted information in a database file and provides a user-friendly Streamlit web application for data visualization and reporting. It is integrated with an automatic alert system and an AI-powered feature for suggesting mitigation strategies automatically.










## Deployment

To deploy this application locally, follow these steps:

#### Clone this repository
```bash
     git clone https://github.com/FATEH02/VulScrapper.git
     cd VulScrapper
```
#### Install requirements

```bash
    pip install -r requirements.txt
```
#### run god_scrapper.py
```bash
    python3 god_scrapper.py
```
This tool uses Selenium to scrape websites and BeautifulSoup for parsing the HTML content. The scraped data is stored in a CSV file using Python's csv module, and Pandas is used for managing and analyzing the dataset
#### run stream.py
```bash
    streamlit run stream.py
```
### This script creates a web application using Streamlit 
#### a csv database show that will show a list of all vulnarebilities colums like
|ProductName|Version|OEM|SeverityLevel|Vulnerability|MitigationStrategy|PublishedDate|UniqueID|
|:--|---|---|---|---|---|--|--|

### Features Of Website  
![App Screenshot](https://github.com/FATEH02/VulScrapper/blob/main/images/csvdatabase.png)

## Filters
![App Screenshot](https://github.com/FATEH02/VulScrapper/blob/main/images/filterpannel.png)

##  Detail of Vulnerability
![App Screenshot](https://github.com/FATEH02/VulScrapper/blob/main/images/specificdetail.png)

## Email Send
a email will be send to user about severity and a attachment visulaized data 
![App Screenshot](https://github.com/FATEH02/VulScrapper/blob/main/images/email%20send.png)

## Email Received
<div style="display: flex; justify-content: space-between;">
    <img src="https://github.com/FATEH02/VulScrapper/blob/main/images/WhatsApp%20Image%202024-09-23%20at%202.50.47%20PM.jpeg" alt="Screenshot 1" width="400"/>
    <img src="https://github.com/FATEH02/VulScrapper/blob/main/images/WhatsApp%20Image%202024-09-23%20at%202.51.51%20PM.jpeg" alt="Screenshot 2" width="400"/>
</div>


## Genrative Explaination
![App Screenshot](https://github.com/FATEH02/VulScrapper/blob/main/images/genratedbyai.png)

## visualize scraped data
![App Screenshot](https://github.com/FATEH02/VulScrapper/blob/main/images/visualization.png)


## Algorithm
this a visulaized Algorithm for this problem 
![App Screenshot](https://github.com/FATEH02/VulScrapper/blob/main/images/algori.png)


## Features

- #### Scrapes vulnerability data from the NVIDIA security page.
- #### Stores data in a CSV format for easy access and manipulation.
- #### Provides interactive filters for viewing vulnerabilities by severity and OEM.
- #### Generates visualizations of vulnerability data, including pie charts and line graphs.
- #### Sends email reports with generated PDF attachments.
- #### Uses Google’s Generative AI to provide explanations for specific vulnerabilities.

## API Reference
use Gemini Api in this code

| AI | Model     | Description                |
| :-------- | :------- | :------------------------- |
| `Gemini` | `Gemini-1,5-flash` | **Required**. Your API key |





### Tech Stack 

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3776AB?style=for-the-badge&logo=matplotlib&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Gmail](https://img.shields.io/badge/Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white)
![Google Generative AI](https://img.shields.io/badge/Google_Generative_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)

 


