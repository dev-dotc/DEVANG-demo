import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess
import plotly.graph_objects as go
import smtplib
import google.generativeai as genai
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
genai.configure(api_key="AIzaSyCQcQG3AAS1t-36y5euLycv2N4Ds9Vkofo")

#creating pdf by taking inputs 
def create_pdf(filename, severity_labels, severity_values, date_group): 
    pdf = PdfPages(filename)

    plt.figure()
    fig_pie = px.pie(
        names=severity_labels,
        values=severity_values,
        title="Vulnerability Severity Distribution",
        hole=0.3  
    )
    #save image to use in pdf we are saving image so we can use it in pdf
    fig_pie.write_image("severity_distribution.png")  
    plt.close()
    
    # now we will add pie chat to pdf
    plt.figure()
    plt.imshow(plt.imread("severity_distribution.png"))
    plt.axis('off')
    pdf.savefig()
    plt.close()

  #creating line chart so we can add it in pdf
    plt.figure()
    plt.plot(date_group['PublishedDate'], date_group['Count'], marker='o')
    plt.title("Vulnerabilities Reported Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Vulnerabilities")
    pdf.savefig()
    plt.close()

    pdf.close()

#this function taking input and preparing for sending email (preparing email)
def send_email(subject, message, sender_email, receiver_email, smtp_server, smtp_port, sender_password, attachment_path=None):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        msg.attach(MIMEText(message, 'plain'))

        if attachment_path:
            with open(attachment_path, 'rb') as f:
                attach = MIMEApplication(f.read(), _subtype='pdf')
                attach.add_header('Content-Disposition', 'attachment', filename=attachment_path)
                msg.attach(attach)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable security
            server.login(sender_email, sender_password)  # Log in
            server.send_message(msg)

        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")


st.set_page_config(page_title="Vulnerability Tracker", layout="wide")

if st.button("Scrap Websites"):
    try:
        subprocess.run(["python3", "god_scrapper.py"], check=True)
        st.success("The script was executed successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")


st.title("Critical Sector Vulnerability Tracker")

data = pd.read_csv("vulnerabilities.csv")#reading csv file 

st.sidebar.header("Filter Vulnerabilities")#filters 
severity_filter = st.sidebar.multiselect("Select Severity Levels", options=data["SeverityLevel"].unique(), default=data["SeverityLevel"].unique())
oem_filter = st.sidebar.multiselect("Select OEMs", options=data["OEM"].unique(), default=data["OEM"].unique())

# Filter data
filtered_data = data[(data["SeverityLevel"].isin(severity_filter)) & (data["OEM"].isin(oem_filter))]

st.write(f"Displaying {len(filtered_data)} vulnerabilities based on the current filters:")
st.dataframe(filtered_data)

# Select a row
selected_row = st.selectbox("Select a vulnerability to view details", filtered_data.index, format_func=lambda x: f"{filtered_data.loc[x, 'ProductName']} - {filtered_data.loc[x, 'SeverityLevel']}")

if selected_row is not None:
    product_name = filtered_data.loc[selected_row, 'ProductName']
    version = filtered_data.loc[selected_row, 'Version']
    oem = filtered_data.loc[selected_row, 'OEM']
    severity = filtered_data.loc[selected_row, 'SeverityLevel']
    vulnerability_desc = filtered_data.loc[selected_row, 'Vulnerability']
    mitigation = filtered_data.loc[selected_row, 'MitigationStrategy']
    published_date = filtered_data.loc[selected_row, 'PublishedDate']
    cve_id = filtered_data.loc[selected_row, 'UniqueID']

    st.subheader(f"Details for {product_name}")
    st.write(f"**Product Version:** {version}")
    st.write(f"**OEM Name:** {oem}")
    st.write(f"**Severity Level:** {severity}")
    st.write(f"**Vulnerability Description:** {vulnerability_desc}")
    st.write(f"**Mitigation Strategy:** {mitigation}")
    st.write(f"**Published Date:** {published_date}")
    st.write(f"**CVE ID:** {cve_id}")

# Prepare data for PDF generation
severity_counts = data["SeverityLevel"].value_counts()
severity_labels = severity_counts.index.to_list()
severity_values = severity_counts.to_list()

data['PublishedDate'] = pd.to_datetime(data['PublishedDate'], errors='coerce')
date_group = data.groupby(data['PublishedDate'].dt.to_period('M')).size().reset_index(name='Count')
date_group['PublishedDate'] = date_group['PublishedDate'].dt.strftime('%Y-%m')

if st.button("Send Email with Visualizations"):
    pdf_filename = "vulnerability_report.pdf"
    create_pdf(pdf_filename, severity_labels, severity_values, date_group)  # Create the PDF with visualizations

    # Create the detailed message
    email_message = f"""\
    Please find the attached PDF report containing visualizations of vulnerabilities.

    Vulnerability Details:
    - **Product Name:** {product_name}
    - **Product Version:** {version}
    - **OEM Name:** {oem}
    - **Severity Level:** {severity}
    - **Vulnerability Description:** {vulnerability_desc}
    - **Mitigation Strategy:** {mitigation}
    - **Published Date:** {published_date}
    - **CVE ID:** {cve_id}
    """

    email_subject = "Vulnerability Report with Visualizations"
    
    sender_email = "your email"
    receiver_email = "target email"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_password = "app security key" #go your goole account 2fa auth and find app security key copy and past here  

    send_email(email_subject, email_message, sender_email, receiver_email, smtp_server, smtp_port, sender_password, attachment_path=pdf_filename)

if st.button("Generate AI Explanation"):
        prompt = f"Explain the following vulnerability in detail:\n\nProduct: {product_name}\nVersion: {version}\nOEM: {oem}\nSeverity: {severity}\nDescription: {vulnerability_desc}\nMitigation: {mitigation}\nCVE ID: {cve_id}\nPublished Date: {published_date}"

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        st.subheader("Generated AI Explanation")
        st.write(response.text)


# Plotting
col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(
        names=severity_labels,
        values=severity_values,
        title="Vulnerability Severity Distribution",
        hole=0.3  
    )
    st.plotly_chart(fig_pie)

with col2:
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=date_group['PublishedDate'], 
        y=date_group['Count'],
        mode='lines+markers',
        name='Vulnerabilities Over Time'
    ))

    fig_line.update_layout(
        title="Vulnerabilities Reported Over Time",
        xaxis_title="Date",
        yaxis_title="Number of Vulnerabilities"
    )

    st.plotly_chart(fig_line)

oem_counts = data['OEM'].value_counts()
fig_oem = px.bar(oem_counts, x=oem_counts.index, y=oem_counts.values, title="Vulnerabilities by OEM")
st.plotly_chart(fig_oem)

oem_severity = data.groupby(['OEM', 'SeverityLevel']).size().unstack()
fig_stacked = px.bar(oem_severity, title="Severity Level by OEM", barmode='stack')
st.plotly_chart(fig_stacked)

product_counts = data['ProductName'].value_counts()
fig_product = px.bar(product_counts, x=product_counts.values, y=product_counts.index, orientation='h', title="Vulnerabilities by Product")
st.plotly_chart(fig_product)
