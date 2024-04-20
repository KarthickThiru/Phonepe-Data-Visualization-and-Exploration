# Phonepe-Data-Visualization-and-Exploration
Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly.

# Phonepe
PhonePe is undoubtedly one of the most revolutionary apps since it has managed to transform the way cash is carried around in India.
Here are some of the top noteworthy features of PhonePe:

1. The Country’s First UPI Linked E-wallet
2. No Need for Bank Account Details
3. Easy Transfers, Payments, and Recharges
4. Hassle-free Authentication Method
5. No Need for Frequent Top Ups
6. Increased Limit Per Transaction
7. Higher Security

Here is how you can use PhonePe for all your needs:

1. Shop online with various e-commerce platforms and easily pay using UPI
2. Make utility bill payments
3. Send or receive money using your phone contact list via UPI
4. Recharge prepaid mobile and also pay for DTH connections
5. Regularly check your bank account balance
6. Register a beneficiary
7. Use more than one bank account
8. Explore various cashback
9. Split bills and divide payments

# Data
The data used in PhonePe Pulse is available in this link. The data is divided into different categories, such as transaction data, user data, and top data. The data is stored in JSON format. A complete description of the data is provided in the link below, before proceeding to data visualisation or data processing kindly understand the data completely. data: https://github.com/PhonePe/pulse

# Required Skills:
1. Python scripting
2. Github Cloning
3. Pandas
4. Streamlit
5. Plotly

# Cloning
To clone the Phonepe Pulse Github repository and store its data in a CSV or JSON format: Clone the Phonepe Pulse Github repository using the following command:

https://github.com/phonepe/pulse.git

# Importing Libraries

Before proceeding further importing the necessary libraries is important. In this dashboard, we use streamlit, plotly to visualize our data.

1. import streamlit as st
2. from streamlit_option_menu import option_menu
3. import pandas as pd
4. import mysql.connector
5. import plotly.express as px
6. import requests
7. import json

# Connecting to Database

Next, we connect to the database where we stored our six data frames which are transformed in a way to best suit the visualization.

#SQL Connection

mydb = mysql.connector.connect(host = '', user = '', password = '', database = '')

mycursor = mydb.cursor()

# Streamlit Program

Here use your imagination and create your dashboard using stremlit, If you look at my dashboard function block it has various charts and dataframes displayed using plotly graph. likewise, you could also try to visualize in a more better and efficient way.

You can view your streamlit file by using, streamlit run "YOUR FILE NAME"

# Conclusion

The final product of this project is the live geo visualization dashboard that displays information and insights from the Phonepe pulse Github repository in an interactive and visually appealing manner.








