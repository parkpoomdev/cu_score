import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Configure Google Sheets authentication
def setup_google_sheets():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    json_keyfile = 'student-score-442208-6dfbb6e6f681.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    return gspread.authorize(creds)

# Fetch data from Google Sheets
def get_sheet_data(client):
    try:
        spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1sx8K1aGjC9uFQHgAz7t11a3QC3Z7Smlk-IBYJ9qWwoM/edit'
        spreadsheet = client.open_by_url(spreadsheet_url)
        worksheet = spreadsheet.worksheet('SHEET5602105I20241')

        data = worksheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df

    except Exception as e:
        st.error(f"Error reading Google Sheet: {str(e)}")
        return None

# Fetch student credentials from CSV
def load_student_credentials():
    try:
        # Load the CSV file into a pandas DataFrame
        student_df = pd.read_csv('student_details.csv')  # Ensure the CSV file is in the same directory
        return student_df
    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")
        return None

# Define the login page
def login_page(credentials_df):
    st.title("5602105 Coding for Entrepreneurs: Class Attendance and Assignments")
    username = st.text_input("Enter your Student ID")
    password = st.text_input("Enter your Password", type="password")

    if st.button("Login"):
        if username and password:
            # Debug: Display the credentials DataFrame
            st.write("Debugging: Credentials DataFrame")
            st.write(credentials_df)

            # Verify if the Student ID exists
            try:
                user_data = credentials_df.loc[credentials_df['Student ID'].astype(str) == username]
                if not user_data.empty:
                    correct_password = user_data['Password'].values[0]
                    if str(password) == str(correct_password):
                        st.success("Login successful!")
                        st.session_state.logged_in = True
                        st.session_state.student_id = username
                        st.rerun()
                    else:
                        st.error("Incorrect password. Please try again.")
                else:
                    st.error("Student ID not found. Please check and try again.")
            except Exception as e:
                st.error(f"An error occurred during login: {str(e)}")
        else:
            st.error("Please enter both Student ID and Password.")

# Define the dashboard page
def dashboard_page():
    st.title("Student Dashboard")

    # Get the logged-in student's data
    student_data = st.session_state.df[st.session_state.df['Student_ID'] == st.session_state.student_id]

    # Remove empty rows (if any) from the student's data
    student_data = student_data.dropna(how="all").reset_index(drop=True)

    if student_data.empty:
        st.error("No data found for the logged-in student. Please contact your instructor.")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.student_id = None
            st.rerun()
        return

    # Define "In-Class" and "Lab" columns
    in_class_columns = [
        "Week_1_In-Class", "Week_2_In-Class", "Week_3_In-Class", "Week_4_In-Class", "Week_5_In-Class",
        "Week_6_In-Class", "Week_7_In-Class", "Week_8-9_In-Class", "Week_10_In-Class", "Week_11_In-Class"
    ]
    lab_columns = [
        "Week_1_Lab_Homework", "Week_2_Lab_Homework", "Week_3_Lab_Homework", "Week_4_Lab_Homework",
        "Week_5_Lab_Homework", "Week_6_Lab_Homework", "Week_7_Lab_Homework", "Week_8-9_Lab_Homework",
        "Week_10_Lab_Homework", "Week_11_Lab_Homework"
    ]

    # Calculate the total scores for "In-Class" and "Lab"
    try:
        in_class_total = student_data[in_class_columns].astype(int).sum(axis=1).values[0]
    except IndexError:
        in_class_total = 0

    try:
        lab_total = student_data[lab_columns].astype(int).sum(axis=1).values[0]
    except IndexError:
        lab_total = 0

    # Calculate the combined total
    combined_total = in_class_total + lab_total

    # Display the summary
    st.subheader("Summary")
    summary_data = pd.DataFrame({
        "Metric": ["Total In-Class Score", "Total Lab Score", "Combined Total Score"],
        "Details": [in_class_total, lab_total, combined_total]
    })
    st.table(summary_data)

    # Filter and display the student's data in a vertical table
    st.subheader("Score")
    vertical_data = student_data.transpose()  # Transpose the data to make it vertical
    vertical_data.columns = ["Details"]  # Rename the column to "Value"
    st.table(vertical_data)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.student_id = None
        st.rerun()


# Main function to control the app flow
def main():
    st.set_page_config(layout="wide")

    # Load student credentials
    student_df = load_student_credentials()
    if student_df is None:
        return

    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'student_id' not in st.session_state:
        st.session_state.student_id = None
    if 'df' not in st.session_state:
        client = setup_google_sheets()
        st.session_state.df = get_sheet_data(client)

    # Display the appropriate page based on login status
    if st.session_state.logged_in:
        dashboard_page()
    else:
        login_page(student_df)

if __name__ == "__main__":
    main()
