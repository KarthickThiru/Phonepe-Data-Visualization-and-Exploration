import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json
from PIL import Image 

#Data Frame Creation

#SQL Connection

mydb = mysql.connector.connect(
    host = '', 
    user = '', 
    password = '', 
    database = '' 
)
mycursor = mydb.cursor()

#DF - aggregated_insurance - Table 1

mycursor.execute('select * from aggregated_insurance')

t1= mycursor.fetchall()
# mydb.commit()

agg_insurance=pd.DataFrame(t1, columns= ("States", "Years", "Quarters", "Trans_type", "Trans_count", "Trans_amount"))

#DF - aggregated_transaction - Table 2

mycursor.execute('select * from aggregated_transaction')

t2= mycursor.fetchall()

agg_transaction=pd.DataFrame(t2, columns= ("States", "Years", "Quarters", "Trans_type", "Trans_count","Trans_amount"))

#DF - aggregated_user - Table 3

mycursor.execute('select * from aggregated_user')

t3= mycursor.fetchall()

agg_user=pd.DataFrame(t3, columns= ("States", "Years", "Quarters", "Brand", "count","Percentage"))

#DF - map_insurance - Table 4

mycursor.execute('select * from map_insurance')

t4= mycursor.fetchall()

map_insu=pd.DataFrame(t4, columns= ("States", "Years", "Quarters", "Districts", "Count","Amount"))

#DF - map_transaction - Table 5

mycursor.execute('select * from map_transaction')

t5= mycursor.fetchall()

map_trans=pd.DataFrame(t5, columns= ("States", "Years", "Quarters", "Districts", "Count","Amount"))

#DF - map_user - Table 6

mycursor.execute('select * from map_user')

t6= mycursor.fetchall()

map_user=pd.DataFrame(t6, columns= ("States", "Years", "Quarters", "Districts", "Registered_Users","App_Opens"))

#DF - top_insurance - Table 7

mycursor.execute('select * from top_insurance')

t7= mycursor.fetchall()

top_insu=pd.DataFrame(t7, columns= ("States", "Years", "Quarters", "Pincodes", "Count","Amount"))

#DF - top_transaction - Table 8

mycursor.execute('select * from top_transaction')

t8= mycursor.fetchall()

top_trans=pd.DataFrame(t8, columns= ("States", "Years", "Quarters", "Pincodes", "Count","Amount"))

#DF - top_user - Table 9

mycursor.execute('select * from top_user')

t9= mycursor.fetchall()

top_user=pd.DataFrame(t9, columns= ("States", "Years", "Quarters", "Pincodes", "Registered_Users"))

def Insurance_amount_count_Year(df,year):

    #yact=year,amount,count,transaction
    yact=df[df["Years"] == year]
    yact.reset_index(drop=True, inplace=True)

    yactgroup=yact.groupby("States")[["Trans_count","Trans_amount"]].sum()
    yactgroup.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(yactgroup, x="States", y="Trans_amount",title=f"TRANSACTION AMOUNT BASED ON STATES - YEAR: {year}",
                        color_discrete_sequence=px.colors.sequential.Cividis_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(yactgroup, x="States", y="Trans_count",title=f"TRANSACTION COUNT BASED ON STATES - YEAR: {year}",
                        color_discrete_sequence=px.colors.sequential.Blues_r, height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)

    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        res=requests.get(url)
        data1=json.loads(res.content)
        state_names=[]
        for feature in data1["features"]:
            state_names.append(feature["properties"]["ST_NM"])
        state_names.sort()

        fig_india_1=px.choropleth(yactgroup, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Trans_amount", color_continuous_scale="temps",
                                range_color=(yactgroup["Trans_amount"].min(), yactgroup["Trans_amount"].max()),
                                hover_name="States", title=f"MAP VIEW:   TRANSACTION AMOUNT BASED ON STATES - YEAR: {year}",
                                fitbounds= "locations",  height=1000, width=650)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_2=px.choropleth(yactgroup, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Trans_count", color_continuous_scale="ylgn",
                                range_color=(yactgroup["Trans_count"].min(), yactgroup["Trans_count"].max()),
                                hover_name="States", title=f"MAP VIEW:   TRANSACTION COUNT BASED ON STATES - YEAR: {year}",
                                fitbounds= "locations",  height=1000, width=650)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    return yact

def Insurance_amount_count_Year_Map(df,year):

    yact=df[df["Years"] == year]
    yact.reset_index(drop=True, inplace=True)

    yactgroup=yact.groupby("States")[["Count","Amount"]].sum()
    yactgroup.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(yactgroup, x="States", y="Amount",title=f"TRANSACTION AMOUNT BASED ON STATES - YEAR: {year}",
                        color_discrete_sequence=px.colors.sequential.Cividis_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(yactgroup, x="States", y="Count",title=f"TRANSACTION COUNT BASED ON STATES - YEAR: {year}",
                        color_discrete_sequence=px.colors.sequential.Blues_r, height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)

    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        res=requests.get(url)
        data1=json.loads(res.content)
        state_names=[]
        for feature in data1["features"]:
            state_names.append(feature["properties"]["ST_NM"])
        state_names.sort()

        fig_india_1=px.choropleth(yactgroup, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Amount", color_continuous_scale="temps",
                                range_color=(yactgroup["Amount"].min(), yactgroup["Amount"].max()),
                                hover_name="States", title=f"MAP VIEW:   TRANSACTION AMOUNT BASED ON STATES - YEAR: {year}",
                                fitbounds= "locations",  height=1000, width=650)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_2=px.choropleth(yactgroup, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Count", color_continuous_scale="ylgn",
                                range_color=(yactgroup["Count"].min(), yactgroup["Count"].max()),
                                hover_name="States", title=f"MAP VIEW:   TRANSACTION COUNT BASED ON STATES - YEAR: {year}",
                                fitbounds= "locations",  height=1000, width=650)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    return yact

def Insurance_amount_count_Quarters(df, quarter):
    yact=df[df["Quarters"] == quarter]
    yact=yact.drop_duplicates()
    yact.reset_index(drop=True, inplace=True)

    yactgroup=yact.groupby("States")[["Trans_count","Trans_amount"]].sum()
    yactgroup.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_amount=px.bar(yactgroup, x="States", y="Trans_amount",title=f"TRANSACTION AMOUNT BASED ON YEAR: {yact['Years'].max()}, Q{quarter}",
                          color_discrete_sequence=px.colors.sequential.Cividis_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(yactgroup, x="States", y="Trans_count",title=f"TRANSACTION AMOUNT BASED ON YEAR: {yact['Years'].max()}, Q{quarter}",
                        color_discrete_sequence=px.colors.sequential.Blues_r, height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)

    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        res=requests.get(url)
        data1=json.loads(res.content)
        state_names=[]
        for feature in data1["features"]:
            state_names.append(feature["properties"]["ST_NM"])
        state_names.sort()

        fig_india_1=px.choropleth(yactgroup, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Trans_amount", color_continuous_scale="temps",
                                range_color=(yactgroup["Trans_amount"].min(), yactgroup["Trans_amount"].max()),
                                hover_name="States", title=f"MAP VIEW:   TRANSACTION AMOUNT BASED ON YEAR ALL STATES: {yact['Years'].max()}, Q{quarter}",
                                fitbounds= "locations",  height=1000, width=650)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(yactgroup, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Trans_count", color_continuous_scale="ylgn",
                                range_color=(yactgroup["Trans_count"].min(), yactgroup["Trans_count"].max()),
                                hover_name="States", title=f"MAP VIEW:   TRANSACTION AMOUNT BASED ON YEAR ALL STATES: {yact['Years'].max()}, Q{quarter}",
                                fitbounds= "locations",  height=1000, width=650)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    
    return yact

def Insurance_amount_count_Quarters_Map(df, quarter):
    yact=df[df["Quarters"] == quarter]
    yact=yact.drop_duplicates()
    yact.reset_index(drop=True, inplace=True)

    yactgroup=yact.groupby("States")[["Count","Amount"]].sum()
    yactgroup.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_amount=px.bar(yactgroup, x="States", y="Amount",title=f"TRANSACTION AMOUNT BASED ON YEAR: {yact['Years'].max()}, Q{quarter}",
                          color_discrete_sequence=px.colors.sequential.Cividis_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(yactgroup, x="States", y="Count",title=f"TRANSACTION AMOUNT BASED ON YEAR: {yact['Years'].max()}, Q{quarter}",
                        color_discrete_sequence=px.colors.sequential.Blues_r, height=650, width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)

    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        res=requests.get(url)
        data1=json.loads(res.content)
        state_names=[]
        for feature in data1["features"]:
            state_names.append(feature["properties"]["ST_NM"])
        state_names.sort()

        fig_india_1=px.choropleth(yactgroup, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Amount", color_continuous_scale="temps",
                                range_color=(yactgroup["Amount"].min(), yactgroup["Amount"].max()),
                                hover_name="States", title=f"MAP VIEW:   TRANSACTION AMOUNT BASED ON YEAR ALL STATES: {yact['Years'].max()}, Q{quarter}",
                                fitbounds= "locations",  height=1000, width=650)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(yactgroup, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Count", color_continuous_scale="ylgn",
                                range_color=(yactgroup["Count"].min(), yactgroup["Count"].max()),
                                hover_name="States", title=f"MAP VIEW:   TRANSACTION AMOUNT BASED ON YEAR ALL STATES: {yact['Years'].max()}, Q{quarter}",
                                fitbounds= "locations",  height=1000, width=650)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    
    return yact


def agg_trans_type(df, state):

    yact=df[df["States"] == state]
    yact=yact.drop_duplicates()
    yact.reset_index(drop=True, inplace=True)
    yactgroup=yact.groupby("Trans_type")[["Trans_count","Trans_amount"]].sum()
    yactgroup.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:
        fig_pie_1=px.pie(data_frame= yactgroup, names= "Trans_type", values= "Trans_amount",
                        width=550, title= f"TRANSACTION AMOUNT BASED ON TYPE - {state.upper()}", hole= 0.35,color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2=px.pie(data_frame= yactgroup, names= "Trans_type", values= "Trans_count",
                        width=550, title= f"TRANSACTION COUNT BASED ON TYPE - {state.upper()}", hole= 0.35, color_discrete_sequence=px.colors.sequential.Sunsetdark_r)
        st.plotly_chart(fig_pie_2)

#Transaction Based on Brand - Analysis 1
def Agg_user_plot_1(df, year):

    agg_user_y= df[df["Years"] == year]
    agg_user_y = agg_user_y.drop_duplicates()
    agg_user_y.reset_index(drop=True, inplace= True)

    agg_user_y_group= pd.DataFrame(agg_user_y.groupby("Brand")["count"].sum())
    agg_user_y_group.reset_index(inplace= True)


    fig_bar_1= px.area(agg_user_y_group, x= "Brand", y= "count", title= f"TRANSACTION COUNT BASED ON BRAND & YEAR {year}",
                    width = 1234, color_discrete_sequence= px.colors.sequential.tempo, hover_name="Brand")
    st.plotly_chart(fig_bar_1)

    return agg_user_y  

#Transaction Based on Brand - Analysis 2
def Agg_user_plot_2(df, quarter):

    try:
        agg_user_yq= df[df["Quarters"] == quarter]
        agg_user_yq.drop_duplicates()
        agg_user_yq.reset_index(drop=True, inplace= True)

        agg_user_yqg = pd.DataFrame(agg_user_yq.groupby("Brand")["count"].sum())
        agg_user_yqg.reset_index(inplace= True)

        fig_bar_1= px.area(agg_user_yqg, x= "Brand", y= "count", title= f"TRANSACTION COUNT BASED ON BRAND  - YEAR: {agg_user_yq['Years'].max()}, Q{quarter}",
                        width = 1234, color_discrete_sequence= px.colors.sequential.Inferno, hover_name="Brand")
        st.plotly_chart(fig_bar_1)
    
    except Exception as err:
        print("No Data Available for the selected time period!")

    return agg_user_yq

#Transaction Based on Brand - Analysis 3 

def Agg_user_plot_3(df, state):
    try:
        auyqs=df[df["States"] == state]
        auyqs.reset_index(drop= True, inplace= True)
        auyqs = auyqs.drop_duplicates()

        fig_line_1=px.line(auyqs, x = "Brand", y = "count", hover_data = "Percentage",
                        title = f"TRANSACTION COUNT & PERCENTAGE BASED ON BRAND, STATE:    {state.upper()}", width = 1000, markers=True)
        st.plotly_chart(fig_line_1)
    except Exception as err:
        print("No Data Available for the selected time period!")

#Map_Insurance_District

def Map_insur_Districts(df, state):

    yact=df[df["States"] == state]
    yact.reset_index(drop=True, inplace=True)
    yactgroup=yact.groupby("Districts")[["Count","Amount"]].sum()
    yactgroup = yactgroup.drop_duplicates()
    yactgroup.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:    
        fig_bar_1=px.bar(yactgroup, x = "Amount", y = "Districts", orientation= "h",
                        title= f"TRANSACTION AMOUNT BASED ON DISTRICT - {state.upper()}", color_discrete_sequence=px.colors.sequential.Sunset_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2=px.bar(yactgroup, x = "Count", y = "Districts", orientation= "h",
                        title= f"TRANSACTION COUNT BASED ON DISTRICT - {state.upper()}", color_discrete_sequence=px.colors.sequential.Sunsetdark_r)
        st.plotly_chart(fig_bar_2)

#map_user_plot_1:

def map_user_plot_1(df, year):

    map_user_year= df[df["Years"] == year]
    map_user_year = map_user_year.drop_duplicates()
    map_user_year.reset_index(drop=True, inplace= True)

    map_user_year_group= map_user_year.groupby("States")[["Registered_Users", "App_Opens"]].sum()
    map_user_year_group.reset_index(inplace= True)

    fig_line_1=px.line(map_user_year_group, x = "States", y = ["Registered_Users", "App_Opens"],
                    title = f"USER REGISTRATION AND APP OPENS BASED ON STATES IN YEAR {year}", width = 1234, height= 800, markers=True, 
                    color_discrete_sequence=px.colors.sequential.solar_r)
    st.plotly_chart(fig_line_1)

    return map_user_year

#map_user_plot_2:

def map_user_plot_2(df, quarters):

    map_user_year_Q= df[df["Quarters"] == quarters]
    map_user_year_Q = map_user_year_Q.drop_duplicates()
    map_user_year_Q.reset_index(drop=True, inplace= True)

    map_user_year_group_Q= map_user_year_Q.groupby("States")[["Registered_Users", "App_Opens"]].sum()
    map_user_year_group_Q.reset_index(inplace= True)

    fig_line_1=px.line(map_user_year_group_Q, x = "States", y = ["Registered_Users", "App_Opens"],
                    title = f"USER REGISTRATION AND APP OPENS BASED ON STATES IN {df['Years'].min()},Q{quarters}", width = 1234, height= 800, markers=True, color_discrete_sequence=px.colors.sequential.Darkmint)
    st.plotly_chart(fig_line_1)

    return map_user_year_Q

#map_user_plot_3

def map_user_plot_3(df, states):

    map_user_yqs = df[df["States"] == states]
    map_user_yqs.reset_index(drop=True, inplace= True)

    fig_map_user_area_1=px.line(map_user_yqs, x= "Districts", y= "Registered_Users", title=f"Count of User Registration Based on District - {states.upper()}", height = 800, width= 1400, color_discrete_sequence=px.colors.sequential.Aggrnyl_r, markers=True)
    st.plotly_chart(fig_map_user_area_1)

    fig_map_user_area_2=px.line(map_user_yqs, x= "Districts", y= "App_Opens", title=f"Count of App Opened Based on District - {states.upper()}", height = 800, width= 1400, color_discrete_sequence=px.colors.sequential.Aggrnyl, markers=True)
    st.plotly_chart(fig_map_user_area_2)

#top_insurance_plot_1

def top_insurance_plot_1(df, state):

    top_insu_year= df[df["States"] == state]
    top_insu_year = top_insu_year.drop_duplicates()
    top_insu_year.reset_index(drop=True, inplace= True)

    fig_top_insu_line_1=px.bar(top_insu_year, x = "Quarters", y = "Amount", hover_data= "Pincodes",
                    title = f"TOP AMOUNT BASED ON QUARTERS & PINCODES - STATE: {state.upper()}", width = 1234, height= 1234, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
    st.plotly_chart(fig_top_insu_line_1)

    fig_top_insu_line_2=px.bar(top_insu_year, x = "Quarters", y = "Count", hover_data= "Pincodes",
                    title = f"TOP COUNT BASED ON QUARTERS & PINCODES - STATE: {state.upper()}", width = 1234, height= 1234, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig_top_insu_line_2)

#top_user_plot_1

def top_user_plot_1(df, year):

    top_user_y= df[df["Years"] == year]
    top_user_y.reset_index(drop=True, inplace= True)
    top_user_y = top_user_y.drop_duplicates()

    top_user_y_group= pd.DataFrame(top_user_y.groupby(["States", "Quarters"])["Registered_Users"].sum())
    top_user_y_group.reset_index(inplace= True)

    fig_top_plot_1=px.bar(top_user_y_group, x= "States", y= "Registered_Users", color= "Quarters", 
                        title = f"REGISTERED USERS BASED ON STATES AND IN THE YEAR {year}", width= 1111, height= 1234, 
                        color_discrete_sequence= px.colors.sequential.Reds, hover_name= "States")
    st.plotly_chart(fig_top_plot_1)

    return top_user_y

#top_user_plot_2

def top_user_plot_2(df, state):

    top_user_year_s = df[df["States"] == state]
    top_user_year_s = top_user_year_s.drop_duplicates()
    top_user_year_s.reset_index(drop=True, inplace= True)

    fig_top_plot_2 = px.bar(top_user_year_s, x= "Quarters", y= "Registered_Users", title = f"REGISTERED USERS BASED ON PINCODE AND STATE: {state.upper()}",
                            width= 1111, height= 1234, color= "Registered_Users", hover_data= "Pincodes", 
                            color_continuous_scale= px.colors.sequential.Redor)
    st.plotly_chart(fig_top_plot_2)

#SQL Connection - Top Chart - 1

def top_chart_transaction_amount(table_name):

    mydb = mysql.connector.connect(
        host = '', 
        user = '', 
        password = '', 
        database = '' 
    )
    mycursor = mydb.cursor()

    #plot_query_1
    query_1= f'''select states, sum(trans_amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount desc
                limit 10;'''

    mycursor.execute(query_1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    col1, col2 = st.columns(2)

    with col1:
        fig_amount_1=px.bar(df_1, x="states", y="transaction_amount",title="TOP 10 STATES IN TRANSACTION AMOUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Cividis_r, height=650, width=550)
        st.plotly_chart(fig_amount_1)

    #plot_query_2
    query_2= f'''select states, sum(trans_amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount
                limit 10;'''

    mycursor.execute(query_2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_amount"))

    with col2:
        fig_amount_2=px.bar(df_2, x="states", y="transaction_amount",title="BOTTOM 10 STATES IN TRANSACTION AMOUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=716, width=700)
        st.plotly_chart(fig_amount_2)

    #plot_query_3
    query_3= f'''select states, avg(trans_amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount;'''

    mycursor.execute(query_3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3=px.bar(df_3, x="states", y="transaction_amount",title="STATE'S AVERAGE IN TRANSACTION AMOUNT", hover_name= "states",
                         color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=1212)
    st.plotly_chart(fig_amount_3)

def top_chart_transaction_amount_new(table_name):

    mydb = mysql.connector.connect(
        host = '', 
        user = '', 
        password = '', 
        database = '' 
    )
    mycursor = mydb.cursor()

    #plot_query_1
    query_1= f'''select states, sum(amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount desc
                limit 10;'''

    mycursor.execute(query_1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    col1, col2 = st.columns(2)

    with col1:
        fig_amount_1=px.bar(df_1, x="states", y="transaction_amount",title="TOP 10 STATES IN TRANSACTION AMOUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Cividis_r, height=650, width=550)
        st.plotly_chart(fig_amount_1)

    #plot_query_2
    query_2= f'''select states, sum(amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount
                limit 10;'''

    mycursor.execute(query_2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_amount"))

    with col2:
        fig_amount_2=px.bar(df_2, x="states", y="transaction_amount",title="BOTTOM 10 STATES IN TRANSACTION AMOUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=716, width=700)
        st.plotly_chart(fig_amount_2)

    #plot_query_3
    query_3= f'''select states, avg(amount) as transaction_amount 
                from {table_name}
                group by states
                order by transaction_amount;'''

    mycursor.execute(query_3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3=px.bar(df_3, x="states", y="transaction_amount",title="STATE'S AVERAGE IN TRANSACTION AMOUNT", hover_name= "states",
                    color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=1212)
    st.plotly_chart(fig_amount_3)

def top_chart_transaction_count(table_name):

    mydb = mysql.connector.connect(
        host = '', 
        user = '', 
        password = '', 
        database = '' 
    )
    mycursor = mydb.cursor()

    #plot_query_1
    query_1= f'''select states, sum(trans_count) as transaction_count 
                from {table_name}
                group by states
                order by transaction_count desc
                limit 10;'''

    mycursor.execute(query_1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_count"))

    col1, col2 = st.columns(2)

    with col1:
        fig_amount_1=px.bar(df_1, x="states", y="transaction_count",title="TOP 10 STATES IN TRANSACTION COUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Cividis_r, height=650, width=550)
        st.plotly_chart(fig_amount_1)

    #plot_query_2
    query_2= f'''select states, sum(trans_count) as transaction_count 
                from {table_name}
                group by states
                order by transaction_count
                limit 10;'''

    mycursor.execute(query_2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_count"))

    with col2:
        fig_amount_2=px.bar(df_2, x="states", y="transaction_count",title="BOTTOM 10 STATES IN TRANSACTION COUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=716, width=700)
        st.plotly_chart(fig_amount_2)

    #plot_query_3
    query_3= f'''select states, avg(trans_count) as transaction_count 
                from {table_name}
                group by states
                order by transaction_count;'''

    mycursor.execute(query_3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3=px.bar(df_3, x="states", y="transaction_count",title="STATE'S AVERAGE IN TRANSACTION COUNT", hover_name= "states",
                         color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=1212)
    st.plotly_chart(fig_amount_3)

def top_chart_transaction_count_new(table_name):

    mydb = mysql.connector.connect(
        host = '', 
        user = '', 
        password = '', 
        database = '' 
    )
    mycursor = mydb.cursor()

    #plot_query_1
    query_1= f'''select states, sum(count) as transaction_count 
                from {table_name}
                group by states
                order by transaction_count desc
                limit 10;'''

    mycursor.execute(query_1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_count"))

    col1, col2 = st.columns(2)

    with col1:
        fig_amount_1=px.bar(df_1, x="states", y="transaction_count",title="TOP 10 STATES IN TRANSACTION COUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Cividis_r, height=650, width=550)
        st.plotly_chart(fig_amount_1)

    #plot_query_2
    query_2= f'''select states, sum(count) as transaction_count 
                from {table_name}
                group by states
                order by transaction_count
                limit 10;'''

    mycursor.execute(query_2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_count"))

    with col2:
        fig_amount_2=px.bar(df_2, x="states", y="transaction_count",title="BOTTOM 10 STATES IN TRANSACTION COUNT", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=716, width=700)
        st.plotly_chart(fig_amount_2)

    #plot_query_3
    query_3= f'''select states, avg(count) as transaction_count 
                from {table_name}
                group by states
                order by transaction_count;'''

    mycursor.execute(query_3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3=px.bar(df_3, x="states", y="transaction_count",title="STATE'S AVERAGE IN TRANSACTION COUNT", hover_name= "states",
                    color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=1212)
    st.plotly_chart(fig_amount_3)

def top_chart_registereduser(table_name, state):

    mydb = mysql.connector.connect(
        host = '', 
        user = '', 
        password = '', 
        database = '' 
    )
    mycursor = mydb.cursor()

    #plot_query_1
    query_1= f'''select districts, sum(Registered_Users) as registereduser
                from {table_name}
                where states = '{state}'
                group by districts
                order by registereduser desc
                limit 10'''

    mycursor.execute(query_1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("districts", "registereduser"))

    col1,col2=st.columns(2)

    with col1:
        fig_amount_1=px.bar(df_1, x="districts", y="registereduser",title=f"{state.upper()}'S TOP 10 DISTRICTS IN USER REGISTRATION", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Cividis_r, height=745, width=650)
        st.plotly_chart(fig_amount_1)

    #plot_query_2
    query_2= f'''select districts, sum(Registered_Users) as registereduser
                from {table_name}
                where states = '{state}'
                group by districts
                order by registereduser
                limit 10'''

    mycursor.execute(query_2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("districts", "registereduser"))

    with col2:
        fig_amount_2=px.bar(df_2, x="districts", y="registereduser",title=f"{state.upper()}'S BOTTOM 10 DISTRICTS IN USER REGISTRATION", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=716, width=700)
        st.plotly_chart(fig_amount_2)

    #plot_query_3
    query_3= f'''select districts, avg(Registered_Users) as registereduser
                from {table_name}
                where states = '{state}'
                group by districts
                order by registereduser'''

    mycursor.execute(query_3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("districts", "registereduser"))

    fig_amount_3=px.bar(df_3, x="districts", y="registereduser",title=f"{state.upper()} STATE'S AVERAGE USER REGISTRATION BASED ON DISTRICTS", hover_name= "districts",
                    color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=1212)
    st.plotly_chart(fig_amount_3)

def top_chart_appopens(table_name, state):

    mydb = mysql.connector.connect(
        host = '', 
        user = '', 
        password = '', 
        database = '' 
    )
    mycursor = mydb.cursor()

    #plot_query_1
    query_1= f'''select districts, sum(App_Opens) as appopens
                from {table_name}
                where states = '{state}'
                group by districts
                order by appopens desc
                limit 10'''

    mycursor.execute(query_1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    col1,col2 = st.columns(2)
    with col1:
        df_1 = pd.DataFrame(table_1, columns=("districts", "appopens"))

        fig_amount_1=px.bar(df_1, x="districts", y="appopens",title=f"{state.upper()}'S TOP 10 DISTRICTS IN APP INSTALLATION", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Cividis_r, height=650, width=550)
        st.plotly_chart(fig_amount_1)

    #plot_query_2
    query_2= f'''select districts, sum(App_Opens) as appopens
                from {table_name}
                where states = '{state}'
                group by districts
                order by appopens
                limit 10'''

    mycursor.execute(query_2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("districts", "appopens"))

    with col2:
        fig_amount_2=px.bar(df_2, x="districts", y="appopens",title=f"{state.upper()}'S BOTTOM 10 DISTRICTS IN APP INSTALLATION", hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=716, width=700)
        st.plotly_chart(fig_amount_2)

    #plot_query_3
    query_3= f'''select districts, avg(App_Opens) as appopens
                from {table_name}
                where states = '{state}'
                group by districts
                order by appopens'''

    mycursor.execute(query_3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("districts", "appopens"))

    fig_amount_3=px.bar(df_3, x="districts", y="appopens",title=f"{state.upper()} STATE'S AVERAGE APP INSTALLATIONS BASED ON DISTRICTS", hover_name= "districts",
                    color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=1212)
    st.plotly_chart(fig_amount_3)

def top_chart_registereduser_state(table_name):

    mydb = mysql.connector.connect(
        host = '', 
        user = '', 
        password = '', 
        database = '' 
    )
    mycursor = mydb.cursor()

    #plot_query_1
    query_1= f'''select states, sum(Registered_Users) as registeredusers
                from {table_name}
                group by states
                order by registeredusers desc
                limit 10;'''

    mycursor.execute(query_1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("states", "registeredusers"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1, x="states", y="registeredusers",title="TOP 10 STATES IN USER REGISTRATION", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=550)
        st.plotly_chart(fig_amount_1)

    #plot_query_2
    query_2= f'''select states, sum(Registered_Users) as registeredusers
                from {table_name}
                group by states
                order by registeredusers
                limit 10;'''

    mycursor.execute(query_2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("states", "registeredusers"))

    with col2:
        fig_amount_2=px.bar(df_2, x="states", y="registeredusers",title="BOTTOM 10 STATES IN USER REGISTRATION", hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Agsunset_r, height=716, width=700)
        st.plotly_chart(fig_amount_2)

    #plot_query_3
    query_3= f'''select states, avg(Registered_Users) as registeredusers
                from {table_name}
                group by states
                order by registeredusers;'''

    mycursor.execute(query_3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("states", "registeredusers"))

    fig_amount_3=px.bar(df_3, x="states", y="registeredusers",title="AVERAGE USER REGISTRATION BASED ON STATES", hover_name= "states",
                    color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=1212)
    st.plotly_chart(fig_amount_3)

def top_brand_count(table_name):

    mydb = mysql.connector.connect(
        host = '', 
        user = '', 
        password = '', 
        database = '' 
    )
    mycursor = mydb.cursor()

    #plot_query_1
    query_1= f'''select brand, sum(count) as count
                from {table_name}
                group by brand
                order by count desc
                limit 10;'''

    mycursor.execute(query_1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("brand", "count"))

    col1,col2=st.columns(2)

    with col1:
        fig_amount_1=px.bar(df_1, x="brand", y="count",title="TOP 10 BRANDS", hover_name= "brand",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=550)
        st.plotly_chart(fig_amount_1)

    #plot_query_2
    query_2= f'''select brand, sum(count) as count
                from {table_name}
                group by brand
                order by count
                limit 10;'''

    mycursor.execute(query_2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("brand", "count"))

    with col2:
        fig_amount_2=px.bar(df_2, x="brand", y="count",title="BOTTOM 10 BRANDS", hover_name= "brand",
                        color_discrete_sequence=px.colors.sequential.Agsunset_r, height=716, width=700)
        st.plotly_chart(fig_amount_2)

    #plot_query_3
    query_3= f'''select brand, avg(count) as count
                from {table_name}
                group by brand
                order by count;'''

    mycursor.execute(query_3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("brand", "count"))

    fig_amount_3=px.bar(df_3, x="brand", y="count",title="AVERAGE BRANDS USED BASED ON COUNT", hover_name= "brand",
                    color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=1212)
    st.plotly_chart(fig_amount_3)   

def top_brand_percentage(table_name):

    mydb = mysql.connector.connect(
        host = '', 
        user = '', 
        password = '', 
        database = '' 
    )
    mycursor = mydb.cursor()

    #plot_query_1
    query_1= f'''select brand, sum(percentage) as percentage
                from {table_name}
                group by brand
                order by percentage desc
                limit 10;'''

    mycursor.execute(query_1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("brand", "percentage"))

    col1,col2=st.columns(2)

    with col1:
        fig_amount_1=px.bar(df_1, x="brand", y="percentage",title="TOP 10 BRAND BASED ON PERCENTAGE", hover_name= "brand",
                    color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=550)
        st.plotly_chart(fig_amount_1)

    #plot_query_2
    query_2= f'''select brand, sum(percentage) as percentage
                from {table_name}
                group by brand
                order by percentage
                limit 10;'''

    mycursor.execute(query_2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("brand", "percentage"))

    with col2:
        fig_amount_2=px.bar(df_2, x="brand", y="percentage",title="BOTTOM 10 BRAND BASED ON PERCENTAGE", hover_name= "brand",
                        color_discrete_sequence=px.colors.sequential.Agsunset_r, height=716, width=700)
        st.plotly_chart(fig_amount_2)

    #plot_query_3
    query_3= f'''select brand, avg(percentage) as percentage
                from {table_name}
                group by brand
                order by percentage;'''

    mycursor.execute(query_3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("brand", "percentage"))

    fig_amount_3=px.bar(df_3, x="brand", y="percentage",title="AVERAGE BRAND BASED ON PERCENTAGE", hover_name= "brand",
                    color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=1212)
    st.plotly_chart(fig_amount_3)   

def top_brand_transaction_type(table_name):

    mydb = mysql.connector.connect(
        host = '', 
        user = '', 
        password = '', 
        database = '' 
    )
    mycursor = mydb.cursor()

    #plot_query_1
    query_1= f'''select trans_type, sum(trans_count) as count
                from {table_name}
                group by trans_type
                order by count;'''

    mycursor.execute(query_1)
    table_1 = mycursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1, columns=("trans_type", "count"))

    col1,col2=st.columns(2)
    
    with col1:
        fig_amount_1=px.bar(df_1, x="trans_type", y="count",title="TRANSACTION TYPE BASED ON COUNT", hover_name= "trans_type",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=550)
        st.plotly_chart(fig_amount_1)

    #plot_query_2
    query_2= f'''select trans_type, avg(trans_count) as count
                from {table_name}
                group by trans_type
                order by count;'''

    mycursor.execute(query_2)
    table_2 = mycursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2, columns=("trans_type", "count"))

    with col2:
        fig_amount_2=px.bar(df_2, x="trans_type", y="count",title="AVERAGE TRANSACTION TYPE BASED ON COUNT", hover_name= "trans_type",
                        color_discrete_sequence=px.colors.sequential.Agsunset_r, height=716, width=700)
        st.plotly_chart(fig_amount_2)

    #plot_query_3
    query_3= f'''select trans_type, sum(trans_amount) as amount
                    from {table_name}
                    group by trans_type
                    order by amount;'''

    mycursor.execute(query_3)
    table_3 = mycursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3, columns=("trans_type", "amount"))

    col3, col4 = st.columns(2)

    with col3:
        fig_amount_3=px.bar(df_3, x="trans_type", y="amount",title="TRANSACTION TYPE BASED ON AMOUNT", hover_name= "trans_type",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=716, width=700)
        st.plotly_chart(fig_amount_3)

    #plot_query_4
    query_4= f'''select trans_type, avg(trans_amount) as amount
                    from {table_name}
                    group by trans_type
                    order by amount;'''

    mycursor.execute(query_4)
    table_4 = mycursor.fetchall()
    mydb.commit()

    df_4 = pd.DataFrame(table_4, columns=("trans_type", "amount"))

    with col4:
        fig_amount_4=px.bar(df_4, x="trans_type", y="amount",title="AVERAGE TRANSACTION TYPE BASED ON AMOUNT", hover_name= "trans_type",
                        color_discrete_sequence=px.colors.sequential.Agsunset_r, height=716, width=700)
        st.plotly_chart(fig_amount_4)

# Streamlit UI

st.set_page_config(layout="wide")

st.title("PhonePe Data Visualization and Exploration")
st.write(" 🧑‍💻 Tech Used: Github Cloning, Python, Pandas, MySQL, MySQL Connector, Streamlit and Plotly.")
    
select=option_menu(
    menu_title= None,
    options= ["About PhonePe","Data Exploration","Data Analyzation","Process Followed"],
    icons=["bank2", "bar-chart-steps", "body-text", "bounding-box"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal")

if select == "About PhonePe":
    
    col1,col2=st.columns(2)

    with col1:
        st.image(Image.open(r"K:\DS\PhonePe_Logo_with_text.jpeg"))

    with col2:

        st.header(":violet[PhonePe - India's best Payment Transaction App]")
        st.markdown("PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016.")
        st.markdown("The app is accessible in 11 Indian languages. It enables users to perform various financial transactions such as sending and receiving money, recharging mobile and DTH, making utility payments, conducting in-store payments.")
        st.markdown("In August 2016, the company partnered with Yes Bank to launch a UPI-based mobile payment app, based on the government-backed UPI platform.")
        st.markdown("In January 2018, the app garnered ten million downloads.In August 2017, the PhonePe app surpassed BHIM in UPI transactions.")
        st.markdown("PhonePe helps merchants to accept payments through all UPI-based apps, debit and credit cards, as well as wallet (Including third party wallets) on the app.")

    col3,col4=st.columns(2)

    with col3:

        st.markdown(" ")
        st.header(":violet[India's best Payment App]")
        st.markdown("Transfer money")
        st.markdown("Pay bills")
        st.markdown("Make easy payments at stores and invest smartly")
        st.markdown("All on the app you trust!")
        st.markdown(" ")
        st.markdown(" ")
        st.download_button("JOIN US NOW BY DOWNLOADING THE APP", "https://www.phonepe.com/app-download/")

    with col4:
        
        st.markdown(" ")
        st.video("K:\DS\PhonePe_video.mp4")   

elif select == "Data Exploration":

    tab1, tab2, tab3 =st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:
        method_1 = st.radio("Choose any method",["Aggregated Insurance","Aggregated Transaction","Aggregated User"])

        if method_1 == "Aggregated Insurance":

            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Chose the Insurance Year",agg_insurance["Years"].min(), agg_insurance["Years"].max(), agg_insurance["Years"].min())
            yact_Y = Insurance_amount_count_Year(agg_insurance, years)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Chose the Insurance Quarter",yact_Y["Quarters"].min(), yact_Y["Quarters"].max(), yact_Y["Quarters"].min())
            Insurance_amount_count_Quarters(yact_Y, quarters)

        elif method_1 == "Aggregated Transaction":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Chose the Transaction Year",agg_transaction["Years"].min(), agg_transaction["Years"].max(), agg_transaction["Years"].min())
            agg_trans_yact_Y = Insurance_amount_count_Year(agg_transaction, years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the desired State to view Aggregated Transaction", agg_trans_yact_Y["States"].unique())
            agg_trans_type(agg_trans_yact_Y, states)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Chose the Transaction Quarter",agg_trans_yact_Y["Quarters"].min(), agg_trans_yact_Y["Quarters"].max(), agg_trans_yact_Y["Quarters"].min())
            agg_trans_yact_Y_Q= Insurance_amount_count_Quarters(agg_trans_yact_Y, quarters)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the desired State to be viewed based on Transaction Type", agg_trans_yact_Y_Q["States"].unique())
            agg_trans_type(agg_trans_yact_Y_Q, states)

        elif method_1 == "Aggregated User":
            
            try:
                col1,col2=st.columns(2)
                with col1:
                    years= st.slider("Chose the User Year",agg_user["Years"].min(), agg_user["Years"].max(), agg_user["Years"].min())
                Agg_user_year = Agg_user_plot_1(agg_user, years)

                col1,col2=st.columns(2)
                with col1:
                    quarters= st.slider("Chose the User Quarter",Agg_user_year["Quarters"].min(), Agg_user_year["Quarters"].max(), Agg_user_year["Quarters"].min())
                Agg_user_year_Q= Agg_user_plot_2(Agg_user_year, quarters)

                col1,col2=st.columns(2)
                with col1:
                    states=st.selectbox("Select the desired State to view Aggregated User", Agg_user_year_Q["States"].unique())
                Agg_user_plot_3(Agg_user_year_Q, states)
            except Exception as err:
                print("No Data Available for the selected time period!")
                pass
            

    with tab2:
        method_2 = st.radio("Choose any method",["Map Insurance","Map Transaction","Map User"])

        if method_2 == "Map Insurance":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Chose the Desired Map Insurance Year",map_insu["Years"].min(), map_insu["Years"].max(), map_insu["Years"].min())
            map_insu_yact_Y = Insurance_amount_count_Year_Map(map_insu, years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the desired State to be viewed based on Districts", map_insu_yact_Y["States"].unique())
            Map_insur_Districts(map_insu_yact_Y, states)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Chose the Map Insurance Quarter",map_insu_yact_Y["Quarters"].min(), map_insu_yact_Y["Quarters"].max(), map_insu_yact_Y["Quarters"].min())
            map_insu_yact_Y_Q= Insurance_amount_count_Quarters_Map(map_insu_yact_Y, quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the desired State to be viewed in Quarters based on District", map_insu_yact_Y_Q["States"].unique())
            Map_insur_Districts(map_insu_yact_Y_Q, states)

        elif method_2 == "Map Transaction":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Chose the Desired Map Transaction Year",map_trans["Years"].min(), map_trans["Years"].max(), map_trans["Years"].min())
            map_tran_yact_Y = Insurance_amount_count_Year_Map(map_trans, years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the desired State to be viewed based on District's Transaction", map_tran_yact_Y["States"].unique())
            Map_insur_Districts(map_tran_yact_Y, states)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Chose the Map Transaction Quarter",map_tran_yact_Y["Quarters"].min(), map_tran_yact_Y["Quarters"].max(), map_tran_yact_Y["Quarters"].min())
            map_tran_yact_Y_Q= Insurance_amount_count_Quarters_Map(map_tran_yact_Y, quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the desired State to be viewed in Quarters based on District's Transaction", map_tran_yact_Y_Q["States"].unique())
            Map_insur_Districts(map_tran_yact_Y_Q, states)

        elif method_2 == "Map User":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Chose the Desired Map User Year",map_user["Years"].min(), map_user["Years"].max(), map_user["Years"].min())
            map_user_Y = map_user_plot_1(map_user, years)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Chose the Quarter to view the map users",map_user_Y["Quarters"].min(), map_user_Y["Quarters"].max(), map_user_Y["Quarters"].min())
            map_user_Y_Q= map_user_plot_2(map_user_Y, quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the desired State to view User Registration and App Opened", map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, states)

    with tab3:
        method_3 = st.radio("Choose any method",["Top Insurance","Top Transaction","Top User"])

        if method_3 == "Top Insurance":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Top Insurance Year",top_insu["Years"].min(), top_insu["Years"].max(), top_insu["Years"].min())
            top_insu_yact_Y = Insurance_amount_count_Year_Map(top_insu, years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the desired State to view the Top Insurance based on Quarters and Pincode", top_insu_yact_Y["States"].unique())
            top_insurance_plot_1(top_insu_yact_Y, states)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Chose the Quarter to view the top insurance",top_insu_yact_Y["Quarters"].min(), top_insu_yact_Y["Quarters"].max(), top_insu_yact_Y["Quarters"].min())
            top_insu_yact_Y_Q= Insurance_amount_count_Quarters_Map(top_insu_yact_Y, quarters)

        elif method_3 == "Top Transaction":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Top Transaction Year",top_trans["Years"].min(), top_trans["Years"].max(), top_trans["Years"].min())
            top_tran_yact_Y = Insurance_amount_count_Year_Map(top_trans, years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the desired State to view the Top Transaction based on Quarters and Pincode", top_tran_yact_Y["States"].unique())
            top_insurance_plot_1(top_tran_yact_Y, states)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Chose the Quarter to view the Top Transaction",top_tran_yact_Y["Quarters"].min(), top_tran_yact_Y["Quarters"].max(), top_tran_yact_Y["Quarters"].min())
            top_tran_yact_Y_Q= Insurance_amount_count_Quarters_Map(top_tran_yact_Y, quarters)

        elif method_3 == "Top User":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Top User Year",top_user["Years"].min(), top_user["Years"].max(), top_user["Years"].min())
            top_user_yact_Y = top_user_plot_1(top_user, years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the desired State to view the Top Users based on Quarters and Pincode", top_user_yact_Y["States"].unique())
            top_user_plot_2(top_user_yact_Y, states)

elif select == "Data Analyzation":
    
    Question = st.selectbox("Select the Question", ["1. Based on Amount and Count of Aggregated Insurance show top 10, bottom 10 and Average States performance",
                                                    "2. Based on Amount and Count of Map Insurance show top 10, bottom 10 and Average States performance",
                                                    "3. Based on Amount and Count of Top Insurance show top 10, bottom 10 and Average States performance",
                                                    "4. Based on Amount and Count of Aggregated Transaction show top 10, bottom 10 and Average States performance",
                                                    "5. Based on Amount and Count of Map Transaction show top 10, bottom 10 and Average States performance",
                                                    "6. Based on Amount and Count of Top Transaction show top 10, bottom 10 and Average States performance",
                                                    "7. Based on Count of Aggregated User show top 10, bottom 10 and Average States performance",
                                                    "8. Based on Districts show top 10, bottom 10 and Average User Registeration of Map User",
                                                    "9. Based on Districts show top 10, bottom 10 and Average APP Installations",
                                                    "10. Based on States show top 10, bottom 10 and Average User Registration",
                                                    "11. Based on Count and Percentage of Aggregated user show top 10, bottom 10 and Average Brand preference",
                                                    "12. Based on Count and Amount show the Transaction Type used"])
    
    if Question == "1. Based on Amount and Count of Aggregated Insurance show top 10, bottom 10 and Average States performance":
        
        st.subheader("TRANSACTION AMOUNT IN AGGREGATED INSURANCE")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT IN AGGREGATED INSURANCE")
        top_chart_transaction_count("aggregated_insurance")

    elif Question == "2. Based on Amount and Count of Map Insurance show top 10, bottom 10 and Average States performance":
        
        st.subheader("TRANSACTION AMOUNT IN MAP INSURANCE")
        top_chart_transaction_amount_new("map_insurance")

        st.subheader("TRANSACTION COUNT IN MAP INSURANCE")
        top_chart_transaction_count_new("map_insurance")

    elif Question == "3. Based on Amount and Count of Top Insurance show top 10, bottom 10 and Average States performance":
        
        st.subheader("TRANSACTION AMOUNT IN TOP INSURANCE")
        top_chart_transaction_amount_new("top_insurance")

        st.subheader("TRANSACTION COUNT IN TOP INSURANCE")
        top_chart_transaction_count_new("top_insurance")

    elif Question == "4. Based on Amount and Count of Aggregated Transaction show top 10, bottom 10 and Average States performance":
        
        st.subheader("TRANSACTION AMOUNT IN AGGREGATED TRANSACTION")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT IN AGGREGATED TRANSACTION")
        top_chart_transaction_count("aggregated_transaction")

    elif Question == "5. Based on Amount and Count of Map Transaction show top 10, bottom 10 and Average States performance":
        
        st.subheader("TRANSACTION AMOUNT IN MAP TRANSACTION")
        top_chart_transaction_amount_new("map_transaction")

        st.subheader("TRANSACTION COUNT IN MAP TRANSACTION")
        top_chart_transaction_count_new("map_transaction")

    elif Question == "6. Based on Amount and Count of Top Transaction show top 10, bottom 10 and Average States performance":
        
        st.subheader("TRANSACTION AMOUNT IN TOP TRANSACTION")
        top_chart_transaction_amount_new("top_transaction")

        st.subheader("TRANSACTION COUNT IN TOP TRANSACTION")
        top_chart_transaction_count_new("top_transaction")

    elif Question == "7. Based on Count of Aggregated User show top 10, bottom 10 and Average States performance":
        
        st.subheader("TRANSACTION COUNT IN AGGREGATED USER")
        top_chart_transaction_count_new("aggregated_user")

    elif Question == "8. Based on Districts show top 10, bottom 10 and Average User Registeration of Map User":
        
        states= st.selectbox("Kindly select the State for further analysis", map_user["States"].unique())
        st.subheader("USER REGISTRATION BASED ON DISTRICTS")
        top_chart_registereduser("map_user", states)

    elif Question == "9. Based on Districts show top 10, bottom 10 and Average APP Installations":
        
        states= st.selectbox("Kindly select the State for further analysis", map_user["States"].unique())
        st.subheader("APP INSTALLATIONS BASED ON DISTRICTS")
        top_chart_appopens("map_user", states)
    
    elif Question == "10. Based on States show top 10, bottom 10 and Average User Registration":
        
        st.subheader("USER REGISTERATION")
        top_chart_registereduser_state("top_user")

    elif Question == "11. Based on Count and Percentage of Aggregated user show top 10, bottom 10 and Average Brand preference":
        
        st.subheader("BRANDS PREFERANCE BASED ON COUNT")
        top_brand_count("aggregated_user")

        st.subheader("BRAND PREFERANCE BASED ON PERCENTAGE")
        top_brand_percentage("aggregated_user")
    
    elif Question == "12. Based on Count and Amount show the Transaction Type used":
        
        st.subheader("TRANSACTION TYPE")
        top_brand_transaction_type("aggregated_transaction")

elif select == "Process Followed":

    st.markdown("## :red[About the project]")
    st.markdown("#### Step1: Cloned the phonepe pulse data from git respirotory")
    st.markdown("#### Step2: After that analysed the data and transformed the data from Json to Data Frame")
    st.markdown("#### Step3: After that stored the datas into MYSQL DataBase")
    st.markdown("#### Step4: Then Created a Streamlit app and extrated the datas from MYSQL Database")
    st.markdown("#### Step5: Completed the analysis using streamlit and ploty")
    st.markdown(" ")
    st.markdown("## :blue[Libraries Used]")
    st.markdown("#### 1. Streamlit")
    st.markdown("#### 2. Streamlit option menu")
    st.markdown("#### 3. Pandas")
    st.markdown("#### 4. MySQL Connector")
    st.markdown("#### 5. Plotly Express")
    st.markdown("#### 6. Requests ")
    st.markdown("#### 7. Json ")
    st.markdown("#### 8. PIL")
    st.markdown(" ")
    st.markdown("## :green[Feedback]")
    st.markdown("##### Kindly provide your valuable feedback for further developments")










# # streamlit run phonepe.py 
