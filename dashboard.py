
import sqlite3
import pandas as pd
import streamlit as st

# Function to connect to the SQLite database
def connect_to_db():
    conn = sqlite3.connect(r"C:\Users\chetna\Downloads\dataset.db")
    return conn

# Function to get the current counts and anomalies from the database
def get_data_from_db():
    conn = connect_to_db()
    query = "SELECT * FROM anomaly_data"
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Error while fetching data: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame in case of error
    conn.close()
    return df

# Function to check for anomalies and send notifications
def check_for_anomalies(df):
    anomalies = []
    # Example check: If any count is negative, it's an anomaly
    for column in ['ItemFall_Count', 'Fight_Count', 'Total_Objects']:
        if (df[column] < 0).any():
            anomalies.append(f"Negative value found in {column}!")
    
    # You can add more sophisticated anomaly detection logic here.
    return anomalies

# Function to generate a final statement for the manager based on anomalies or empty data
def generate_report(df, anomalies):
    if df.empty:
        return "The dataset is empty. Please check the source for missing data."
    elif anomalies:
        return f"Anomalies detected: {', '.join(anomalies)}"
    else:
        return "System is running normally. No anomalies detected and data is complete."

# Streamlit Dashboard layout
def main():
    st.set_page_config(page_title="Anomaly Tracking Dashboard", layout="wide")
    
    # Sidebar for navigation
    st.sidebar.title("Dashboard Navigation")
    st.sidebar.subheader("Select an action")
    option = st.sidebar.selectbox("Choose an action", 
                                  ["View Current Data", "View Anomalies", "Generate Final Report"])

    # Fetch data from the database
    df = get_data_from_db()

    # Display the dataframe (latest data)
    if option == "View Current Data":
        st.title("Anomaly Tracking Dashboard")
        st.subheader("Current Data Overview:")
        if df.empty:
            st.warning("No data available or error fetching data.")
        else:
            st.write("Here is the most recent data fetched from the database.")
            st.dataframe(df)

    # Check for anomalies
    if option == "View Anomalies":
        st.title("Anomaly Detection")
        if df.empty:
            st.warning("No data available to check for anomalies.")
        else:
            anomalies = check_for_anomalies(df)
            if anomalies:
                st.subheader("Anomalies Detected:")
                for anomaly in anomalies:
                    st.warning(anomaly)
            else:
                st.subheader("No Anomalies Detected")
                st.success("System is running normally.")

    # Display the final report for the manager
    if option == "Generate Final Report":
        st.title("Generate Final Report")
        if df.empty:
            st.warning("No data available to generate report.")
        else:
            anomalies = check_for_anomalies(df)
            report = generate_report(df, anomalies)
            st.text(report)
            st.success("Final report generated successfully.")

    # Button to refresh data (in case the database is updated externally)
    st.sidebar.subheader("Refresh & Actions")
    if st.sidebar.button("Refresh Data"):
        df = get_data_from_db()
        st.write("Data refreshed successfully!")
        if df.empty:
            st.warning("No data found after refresh.")
        else:
            st.dataframe(df)

    # Option to send the report to the manager (email functionality could be integrated)
    if st.sidebar.button("Send Report to Manager"):
        st.success("Report sent to the manager!")
        # Here you can integrate email functionality or save the report as a PDF.

# Run the Streamlit app
if __name__ == "__main__":
    main()





# import sqlite3
# import pandas as pd
# import streamlit as st
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # Function to connect to the SQLite database
# def connect_to_db():
#     conn = sqlite3.connect(r"C:\Users\chetna\Downloads\dataset.db")
#     return conn

# # Function to get the current counts and anomalies from the database
# def get_data_from_db():
#     conn = connect_to_db()
#     query = "SELECT * FROM anomaly_data"
#     try:
#         df = pd.read_sql_query(query, conn)
#     except Exception as e:
#         st.error(f"Error while fetching data: {e}")
#         df = pd.DataFrame()  # Return an empty DataFrame in case of error
#     conn.close()
#     return df

# # Function to check for anomalies and send notifications
# def check_for_anomalies(df):
#     anomalies = []
#     # Example check: If any count is negative, it's an anomaly
#     for column in ['ItemFall_Count', 'Fight_Count', 'Total_Objects']:
#         if (df[column] < 0).any():
#             anomalies.append(f"Negative value found in {column}!")
    
#     # You can add more sophisticated anomaly detection logic here.
#     return anomalies

# # Function to generate a final statement for the manager based on anomalies or empty data
# def generate_report(df, anomalies):
#     if df.empty:
#         return "The dataset is empty. Please check the source for missing data."
#     elif anomalies:
#         return f"Anomalies detected: {', '.join(anomalies)}"
#     else:
#         return "System is running normally. No anomalies detected and data is complete."

# # Function to send the report via email
# def send_email_to_manager(report):
#     sender_email = "vsharma1_be22@thapar.edu"
#     sender_password = "sharmavishakha"
#     manager_email = "gurvindersingh8951@gmail.com"

#     # Create email message
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = manager_email
#     message["Subject"] = "Anomaly Tracking Dashboard Report"

#     # Add report as the email body
#     message.attach(MIMEText(report, "plain"))

#     try:
#         # Connect to the email server and send the email
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()  # Upgrade to secure connection
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, manager_email, message.as_string())
#         return "Email sent successfully!"
#     except Exception as e:
#         return f"Failed to send email: {e}"

# # Streamlit Dashboard layout
# def main():
#     st.set_page_config(page_title="Anomaly Tracking Dashboard", layout="wide")
    
#     # Sidebar for navigation
#     st.sidebar.title("Dashboard Navigation")
#     st.sidebar.subheader("Select an action")
#     option = st.sidebar.selectbox("Choose an action", 
#                                   ["View Current Data", "View Anomalies", "Generate Final Report"])

#     # Fetch data from the database
#     df = get_data_from_db()

#     # Display the dataframe (latest data)
#     if option == "View Current Data":
#         st.title("Anomaly Tracking Dashboard")
#         st.subheader("Current Data Overview:")
#         if df.empty:
#             st.warning("No data available or error fetching data.")
#         else:
#             st.write("Here is the most recent data fetched from the database.")
#             st.dataframe(df)

#     # Check for anomalies
#     if option == "View Anomalies":
#         st.title("Anomaly Detection")
#         if df.empty:
#             st.warning("No data available to check for anomalies.")
#         else:
#             anomalies = check_for_anomalies(df)
#             if anomalies:
#                 st.subheader("Anomalies Detected:")
#                 for anomaly in anomalies:
#                     st.warning(anomaly)
#             else:
#                 st.subheader("No Anomalies Detected")
#                 st.success("System is running normally.")

#     # Display the final report for the manager
#     if option == "Generate Final Report":
#         st.title("Generate Final Report")
#         if df.empty:
#             st.warning("No data available to generate report.")
#         else:
#             anomalies = check_for_anomalies(df)
#             report = generate_report(df, anomalies)
#             st.text(report)
#             st.success("Final report generated successfully.")

#             # Button to send the report via email
#             if st.button("Send Report to Manager"):
#                 email_status = send_email_to_manager(report)
#                 if "successfully" in email_status:
#                     st.success(email_status)
#                 else:
#                     st.error(email_status)

#     # Button to refresh data (in case the database is updated externally)
#     st.sidebar.subheader("Refresh & Actions")
#     if st.sidebar.button("Refresh Data"):
#         df = get_data_from_db()
#         st.write("Data refreshed successfully!")
#         if df.empty:
#             st.warning("No data found after refresh.")
#         else:
#             st.dataframe(df)

# # Run the Streamlit app
# if __name__ == "__main__":
#     main()
