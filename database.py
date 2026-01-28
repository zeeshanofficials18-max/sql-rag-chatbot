import pyodbc
import streamlit as st

def get_sql_data():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={st.secrets['SQL_SERVER']};"
        f"DATABASE={st.secrets['SQL_DATABASE']};"
        f"UID={st.secrets['SQL_USERNAME']};"
        f"PWD={st.secrets['SQL_PASSWORD']};"
    )

    cursor = conn.cursor()
    cursor.execute("""
    SELECT content 
    FROM dbo.employee_text_view
    WHERE content IS NOT NULL
""")


    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]
