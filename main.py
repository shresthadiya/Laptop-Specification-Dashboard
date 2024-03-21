import streamlit as st
import plotly.express as px 
import plotly.subplots as sp 
import pandas as pd
theme_plotly=None 

#call connection file
from mysql_con import *

#create page config
st.set_page_config("Laptop Specifications Analysis Dashboard",page_icon="",layout="wide")
st.subheader("Laptop Specifications Analysis Dashboard")

#call css style
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

#process data from query
result=view_all_data()
df=pd.DataFrame(result, columns=["laptop_ID", "Company", "Product", "TypeName", "Inches", "ScreenResolution", "CPU", "RAM", "Memory", "GPU", "OpSys", "Weight", "price_in_rupees"])

#print dataframe
#st.dataframe(df,)

#side bar
st.sidebar.header("Filter Company")
Company=st.sidebar.multiselect(
    label="Filter Company",
    options=df["Company"].unique(),
    default=df["Company"].unique(),
)

st.sidebar.header("Filter TypeName")
TypeName=st.sidebar.multiselect(
    label="Filter TypeName",
    options=df["TypeName"].unique(),
    default=df["TypeName"].unique(),
)

st.sidebar.header("Filter RAM")
RAM=st.sidebar.multiselect(
    label="Filter RAM",
    options=df["RAM"].unique(),
    default=df["RAM"].unique(),
)

st.sidebar.header("Filter Inches")
Inches=st.sidebar.multiselect(
    label="FilterInches",
    options=df["Inches"].unique(),
    default=df["Inches"].unique(),
)

st.sidebar.header("Filter OperatingSystem")
OpSys=st.sidebar.multiselect(
    label="Filter OperatingSystem",
    options=df["OpSys"].unique(),
    default=df["OpSys"].unique(),
)

#process query
df_selection = df.query(
    "Company == @Company & TypeName == @TypeName & RAM == @RAM & Inches == @Inches & OpSys == @OpSys"
)

def format_price(price):
    if price >= 100000:
        return "{:.1f} lakhs".format(price / 100000)
    elif price >= 1000:
        return "{:.1f} thousands".format(price / 1000)
    else:
        return "{:.2f} hundreds".format(price)
    

def metrics():
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2=st.columns(2)
    col1.metric("Total Laptops",value=df_selection.laptop_ID.count(),delta="All Laptops")
    
    df_selection['in_numeric'] = pd.to_numeric(df_selection['price_in_rupees'], errors='coerce')
    avg_price = df_selection['in_numeric'].mean()
    formatted_avg_price = format_price(avg_price) 
    col2.metric("Average Price of Laptops", value=formatted_avg_price, delta="All Laptops")

    col11, col22 = st.columns(2)
    # Calculate maximum and minimum values
    maximum_value = df_selection["in_numeric"].max()
    minimum_value = df_selection["in_numeric"].min()
    f_maximum_value=format_price(maximum_value)
    f_minimum_value=format_price(minimum_value)

    #maximum price
    col11.metric("Maximum Price", value=f_maximum_value, delta="High Price")
    #minimum price
    col22.metric("Minimum Price", value=f_minimum_value, delta="Low Price")

    style_metric_cards(background_color="#ffffff",border_left_color="#0F52BA")



div1, div2 = st.columns(2)

def pie():
    with div1:
        theme_plotly = None
        df_selection['price_in_rupees'] = pd.to_numeric(df_selection['price_in_rupees'], errors='coerce')
        # Calculate the average price per laptop type
        avg_price_by_type = df_selection.groupby("TypeName")["price_in_rupees"].mean().reset_index()
        fig = px.pie(avg_price_by_type, values="price_in_rupees", names="TypeName", title="Average Price by Laptop Type")
        fig.update_traces(textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    with div2:
        theme_plotly = None
        df_selection['price_in_rupees'] = pd.to_numeric(df_selection['price_in_rupees'], errors='coerce')
        # Calculate the average price per laptop company
        avg_price_by_company = df_selection.groupby("RAM")["price_in_rupees"].mean().reset_index()
        fig = px.pie(avg_price_by_company, values="price_in_rupees", names="RAM", title="Average Price by RAM Capacity")
        fig.update_traces(textinfo="percent+label", textposition="inside")
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


def bar():
    theme_plotly = None
    df_selection['price_in_rupees'] = pd.to_numeric(df_selection['price_in_rupees'], errors='coerce')
    # Calculate the average price per laptop company
    avg_price_by_company = df_selection.groupby("Company")["price_in_rupees"].mean().reset_index()
    fig = px.bar(avg_price_by_company, y="price_in_rupees", x="Company", text_auto=".2s", title="Price Distribution of Laptops Across Companies")
    fig.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


def scatter():
    theme_plotly = None
    df_selection['price_in_rupees'] = pd.to_numeric(df_selection['price_in_rupees'], errors='coerce')
    
    # Create scatter plot for company versus operating system type
    fig = px.scatter(df_selection, x="OpSys", y="Company", color="price_in_rupees",
                     title="Company-wise Breakdown of Operating Systems",
                     labels={"price_in_rupees": "Price in Rupees"})
    
    fig.update_traces(marker=dict(size=12, opacity=0.8), selector=dict(mode='markers'))
    fig.update_layout(legend_title="Price", legend_y=0.9)
    
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

def scatter1():
    theme_plotly = None
    df_selection['price_in_rupees'] = pd.to_numeric(df_selection['price_in_rupees'], errors='coerce')
    
    # Create scatter plot for company versus operating system type
    fig = px.scatter(df_selection, x="Inches", y="price_in_rupees",
                     title="Price-wise Breakdown of Laptop Inches",
                     labels={"price_in_rupees": "Price in Rupees"})
    
    fig.update_traces(marker=dict(size=12, opacity=0.8), selector=dict(mode='markers'))
    fig.update_layout(legend_title="Price", legend_y=0.9)
    
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


from streamlit_option_menu import option_menu 
with st.sidebar:
    selected=option_menu(
        menu_title="Main Menu",
        options=["Home","Charts"],
        icons=["house","diamond"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
    )
if selected=="Home":
    metrics()

if selected=="Charts":
    pie()
    bar()
    scatter1()
    scatter()




