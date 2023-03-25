# Run Command : streamlit run app.py


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def load_data(file):
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Category'] = df['Category'].astype('category')
    return df

def create_dashboard(df):
    fig = go.Figure()
    net_worth = df.groupby('Date')['Amount'].sum().cumsum()
    fig.add_trace(go.Scatter(x=net_worth.index, y=net_worth.values, name='Net Worth'))
    expenses = df[df['Amount'] < 0].groupby('Category')['Amount'].sum().abs()
    fig.add_trace(go.Pie(labels=expenses.index, values=expenses.values, name='Expenses'))
    income = df[df['Amount'] > 0].groupby(['Year', 'Month'])['Amount'].sum()
    expenses = df[df['Amount'] < 0].groupby(['Year', 'Month'])['Amount'].sum().abs()
    fig.add_trace(go.Bar(x=income.index, y=income.values, name='Income'))
    fig.add_trace(go.Bar(x=expenses.index, y=expenses.values, name='Expenses'))
    fig.update_layout(
        updatemenus=[
            dict(
                type='dropdown',
                direction='down',
                x=0.1,
                y=1.2,
                buttons=[
                    dict(label='Year',
                         method='update',
                         args=[{'visible': [True, False, False]},
                               {'title': 'Net Worth by Year',
                                'xaxis': {'title': 'Year'},
                                'yaxis': {'title': 'Net Worth'}
                                }]
                         ),
                    dict(label='Expenses by Category',
                         method='update',
                         args=[{'visible': [False, True, False]},
                               {'title': 'Expenses by Category',
                                'legend': {'orientation': 'h'}
                                }]
                         ),
                    dict(label='Income and Expenses by Month',
                         method='update',
                         args=[{'visible': [False, False, True]},
                               {'title': 'Income and Expenses by Month',
                                'xaxis': {'title': 'Month'},
                                'yaxis': {'title': 'Amount'}
                                }]
                         )
                ]
            )
        ]    
    )
    return fig

def save_data(df, filename):
    df.to_csv(filename, index=False)

def main():
    df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
    st.set_page_config(page_title='Financial Dashboard')
    st.title('Financial Dashboard')
    st.markdown('This dashboard shows your financial data.')
    file = st.file_uploader('Upload your financial data (CSV)', type='csv')
    if file is not None:
        df = load_data(file)
        st.subheader('Financial Summary')
        st.write('Total Income:', df[df['Amount'] > 0]['Amount'].sum())
        st.write('Total Expenses:', abs(df[df['Amount'] < 0]['Amount'].sum()))
        st.write('Total Investments:', df[df['Category'] == 'Investment']['Amount'].sum())
        st.write('Total Savings:', df[df['Category'] == 'Savings']['Amount'].sum())
        st.subheader('Financial Transactions')
        st.write(df)
        st.subheader('Financial Dashboard')
        fig = create_dashboard(df)
        st.plotly_chart(fig)

    st.subheader('Enter a New Transaction')
    date = st.date_input('Date')
    amount = st.number_input('Amount', value=0.0, step=0.01)
    category = st.selectbox('Category', ['Income', 'Expense', 'Investment', 'Savings'])
    description = st.text_input('Description')
    if st.button('Add Transaction'):
        if category == 'Income':
            amount = abs(amount)
        else:
            amount = -abs(amount)
        new_data = {'Date': date, 'Category': category, 'Amount': amount, 'Description': description}
        df = df.append(new_data, ignore_index=True)
        st.success('Transaction added!')
        st.subheader('Updated Financial Transactions')
        st.write(df)
        st.subheader('Updated Financial Summary')
        st.write('Total Income:', df[df['Amount'] > 0]['Amount'].sum())
        st.write('Total Expenses:', np.abs(df[df['Amount'] < 0]['Amount'].sum()))
        st.write('Total Investments:', df[df['Category'] == 'Investment']['Amount'].sum())
        st.write('Total Savings:', df[df['Category'] == 'Savings']['Amount'].sum())
        save_data(df, 'financial_data.csv')

if __name__ == '__main__':
    main()