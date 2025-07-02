import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title = 'Startup Analysis')
df = pd.read_csv('startup cleaned.csv')
df['Date'] = pd.to_datetime(df['Date'],errors='coerce')
df['month'] = df['Date'].dt.month
df['year'] = df['Date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('Startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('Startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['Startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('Avg',str(round(avg_funding)) + ' Cr')

    with col4:
        st.metric('Funded Startups',num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig3)


def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investment of the investor
    last5_df = df[df['Investors'].str.contains(investor)].head()[['Date','Startup','Vertical','City','Round','amount']]
    st.subheader('Most Recent Investor')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest invesments
        big_series = df[df['Investors'].str.contains(investor)].groupby('Startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

        vertical_series = df[df['Investors'].str.contains(investor)].groupby('Round')['amount'].sum()
        st.subheader('Round invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    with col2:
        # biggest invesments
        vertical_series = df[df['Investors'].str.contains(investor)].groupby('Vertical')['amount'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)

        vertical_series = df[df['Investors'].str.contains(investor)].groupby('City')['amount'].sum()
        st.subheader('city invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)

        df['year'] = df['Date'].dt.year
        year_series = df[df['Investors'].str.contains(investor)].groupby('year')['amount'].sum()

        st.subheader('YoY Investment')
        fig2, ax2 = plt.subplots()
        ax2.plot(year_series.index, year_series.values)

        st.pyplot(fig2)

st.sidebar.title('Startup Funding Analysis')
option = (st.sidebar.selectbox('Select one',['Overall Analysis','Startup','Investor']))

if option == 'Overall Analysis':
    st.title('Overall Analysis')

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['Startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')

else:
    selected_investor = st.sidebar.selectbox('Select Startup',sorted(set(df['Investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
