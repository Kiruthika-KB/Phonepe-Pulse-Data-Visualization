import os
import pandas as pd
import mysql.connector
import plotly.express as px
import streamlit as st
from datetime import datetime

# Extract and Load the Data
data = {
    'id': [1, 2, 3],
    'region': ['North', 'South', 'East'],
    'metric_name': ['Metric1', 'Metric2', 'Metric3'],
    'value': [100, 200, 300],
    'date': ['2025-01-01', '2025-01-02', '2025-01-03']
}

# Create the DataFrame 
transformed_df = pd.DataFrame(data)

# Transform the Data 
transformed_df['date'] = pd.to_datetime(transformed_df['date'])

# Converting the 'date' column to string in 'YYYY-MM-DD' format
transformed_df['date'] = transformed_df['date'].dt.strftime('%Y-%m-%d')

def insert_data_to_mysql(df):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="phonepe_pulse"
    )

    cursor = db.cursor()

    # SQL query to check if the id already exists
    check_query = "SELECT COUNT(*) FROM phonepe_data WHERE id = %s"

    # SQL query to insert data
    insert_query = """
    INSERT INTO phonepe_data (id, region, metric_name, value, date)
    VALUES (%s, %s, %s, %s, %s)
    """

    # Iterate over each row in the DataFrame and insert into the database
    for _, row in df.iterrows():
        cursor.execute(check_query, (row['id'],))
        result = cursor.fetchone()

        if result[0] == 0:  
            cursor.execute(insert_query, tuple(row))
        else:
            print(f"Duplicate id found: {row['id']}. Skipping insert.")

    db.commit()
    cursor.close()
    db.close()


# Insert data into MySQL
insert_data_to_mysql(transformed_df)

#Create Streamlit Dashboard to Visualize Data
def create_dashboard():
    df = transformed_df

    st.title("Phonepe Pulse Dashboard")

    x_column = st.selectbox("Select X axis", df.columns)
    y_column = st.selectbox("Select Y axis", df.columns)

    fig = px.bar(df, x=x_column, y=y_column, title=f"{x_column} vs {y_column}")
    st.plotly_chart(fig)

    st.subheader("Raw Data")
    st.write(df)

if __name__ == "__main__":
    create_dashboard()
