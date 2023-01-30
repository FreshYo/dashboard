import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

df = pd.read_csv('sales.csv', encoding = 'unicode_escape')

df2 = df

df2['REVENUE'] = df2['QUANTITYORDERED']*df2['PRICEEACH']
df3 = df2
df3=df3.sort_values(by='ORDERDATE')
df3=df3.reset_index(drop=True)
df3['ORDERDATE'] = pd.to_datetime(df3['ORDERDATE'], errors='coerce').dt.date


st.set_page_config(
  page_title="BaileyP Dash",
  page_icon="✅"
)

st.title(':star: Sales Dashboard :star:')
st.caption('Bailey P')





st.sidebar.title("Filter data")

productid_list = st.sidebar.multiselect("Select Product code", df['PRODUCTCODE'].unique())
status_list = st.sidebar.multiselect("Select a status", df['STATUS'].unique())
country_list = st.sidebar.multiselect("Select a country", df['COUNTRY'].unique())
productline_list = st.sidebar.multiselect("Select a product", df['PRODUCTLINE'].unique())



start_date=df3['ORDERDATE'].iloc[0]
end_date=df3['ORDERDATE'].iloc[len(df3['ORDERDATE'])-1]
start_date = st.sidebar.date_input('Start Date', start_date)
end_date = st.sidebar.date_input('End date', end_date)
if start_date < end_date :
    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')

df_filtered = df3
if productid_list!=[]:
    df_filtered = df_filtered[(df_filtered['PRODUCTCODE'].isin(productid_list))]
if status_list!=[]:
    df_filtered = df_filtered[(df_filtered['STATUS'].isin(status_list))]
if country_list!=[]:
    df_filtered = df_filtered[(df_filtered['COUNTRY'].isin(country_list))]
if productline_list!=[]:
    df_filtered = df_filtered[(df_filtered['PRODUCTLINE'].isin(productline_list))]

if start_date!=[] and end_date!=[]:
    if df_filtered.empty==0:
        start=df_filtered[df_filtered['ORDERDATE'] == start_date].index.tolist()
        if start!=[]:
            start_index=start[0]
        if start==[]:
            for i in range(1,len(df3['ORDERDATE']),1):
                j=1
                start_date=pd.to_datetime(start_date)+datetime.timedelta(days=j)
                start1 = df_filtered[df_filtered['ORDERDATE'] == start_date].index.tolist()
                if start1!=[]:
                    break
            start_index=start1[0]
        
        end = df_filtered[df_filtered['ORDERDATE'] == end_date].index.tolist()
        if end!=[]:
            end_index = end[len(end) - 1]
        if end==[]:
            for i in range(1,len(df3['ORDERDATE']),1):
                j = -1
                end_date = pd.to_datetime(end_date) + datetime.timedelta(days=j)
                end1 = df_filtered[df_filtered['ORDERDATE'] == end_date].index.tolist()
                if end1!=[]:
                    break
            end_index=end1[0]
        df_filtered=df_filtered.loc[start_index:end_index]
    if df_filtered.empty == 1:
        st.subheader("No Revenue Earned")

df4=pd.DataFrame()
is_check = st.sidebar.checkbox("Apply Filter")
df4=df3
check=0
if is_check:
    check=1
    df4=df_filtered
    st.sidebar.subheader('Filter Applied')

df5 = df4['REVENUE'].sum()
df5 = round(df5, 2)

col1, col2 = st.columns(2)
with col1:
    col1.metric(label="Revenue",
                value='${:,}'.format(df5),
                delta='$10,000')
with col2:
    col2.metric(
        label="Best Product",
        value="Vintage Car"
    )


is_check = st.checkbox("Display Dataframe")
if is_check:
    st.dataframe(df4)

def create_barplot(df4,rev_count2):
    st.header("Products in Barplot by orders")
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    rev_count2=df4.groupby(['PRODUCTLINE']).sum()['QUANTITYORDERED']
    if rev_count2.empty==0:
        ax.bar(
            rev_count2.nlargest(rev_count2.shape[0]).index, \
            rev_count2.nlargest(rev_count2.shape[0])
        )
        plt.xticks(rotation=90)
        st.write(fig)
    if rev_count2.empty==1:
        st.subheader('No Revenue Earned')


is_check = st.checkbox("Show the bar graph")
if is_check:
    rev_count2=df4.groupby(['PRODUCTLINE']).sum()['QUANTITYORDERED']
    create_barplot(df4,rev_count2)
