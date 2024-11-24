# -*- coding: utf-8 -*-
"""Students_Performance.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17RpWu_7weSpWF34owjnHYdXN7_qLvg99
"""

# Import libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error

# Load the dataset from a Google Drive link
@st.cache_data
def load_data():
    """
    Load dataset from a Google Drive link and preprocess it.
    """
    gdrive_link = "https://drive.google.com/uc?id=1HnLCBBbmV3MRrSPARsFOx6kZCqpUCPEo"  # Replace with actual file ID
    try:
        data = pd.read_csv(gdrive_link)
        
        # Encoding categorical columns into numerical values
        le_gender = LabelEncoder()
        le_tutoring = LabelEncoder()
        le_extracurricular = LabelEncoder()
        
        data['Gender'] = le_gender.fit_transform(data['Gender'])  # Male=0, Female=1
        data['Tutoring'] = le_tutoring.fit_transform(data['Tutoring'])  # No=0, Yes=1
        data['Extracurricular'] = le_extracurricular.fit_transform(data['Extracurricular'])  # No=0, Yes=1
        
        # Map GradeClass to numeric
        grade_mapping = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
        data['GradeClass'] = data['GradeClass'].map(grade_mapping)
        return data
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()  # Return empty DataFrame if error occurs

# Load the dataset
student_data = load_data()

# Train a model (Random Forest Regressor) to predict GPA and Grade
def train_model(data):
    """
    Train Random Forest models for GPA and Grade prediction.
    """
    # Features: Gender, Age, StudyTimeWeekly, Absences, Tutoring, Extracurricular
    X = data[['Gender', 'Age', 'StudyTimeWeekly', 'Absences', 'Tutoring', 'Extracurricular']]
    y_gpa = data['GPA']
    y_grade = data['GradeClass'].apply(lambda x: ['A', 'B', 'C', 'D', 'E'].index(x))  # Convert grades to numeric
    
    # Split data into training and testing sets
    X_train, X_test, y_train_gpa, y_test_gpa, y_train_grade, y_test_grade = train_test_split(
        X, y_gpa, y_grade, test_size=0.2, random_state=42)
    
    # Initialize the RandomForest models for GPA and Grade prediction
    model_gpa = RandomForestRegressor(n_estimators=100, random_state=42)
    model_grade = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Train the models
    model_gpa.fit(X_train, y_train_gpa)
    model_grade.fit(X_train, y_train_grade)
    
    # Predict on test data
    predictions_gpa = model_gpa.predict(X_test)
    predictions_grade = model_grade.predict(X_test)
    
    # Calculate Mean Squared Error for evaluation
    mse_gpa = mean_squared_error(y_test_gpa, predictions_gpa)
    mse_grade = mean_squared_error(y_test_grade, predictions_grade)
    
    return model_gpa, model_grade, mse_gpa, mse_grade

# Train the model once the data is loaded
model_gpa, model_grade, mse_gpa, mse_grade = train_model(student_data)

# Role-based Views
role = st.selectbox("Choose", ["Student", "Teacher", "Administrator"])

if role == "Administrator":
    st.subheader("Administrator Dashboard")
    total_students = len(student_data['StudentID'].unique())
    avg_gpa = student_data['GPA'].mean()
    grade_counts = student_data['GradeClass'].value_counts()

    st.write(f"**Total Students:** {total_students}")
    st.write(f"**Average GPA:** {avg_gpa:.2f}")
    st.write("**Students by Grade:**")
    st.bar_chart(grade_counts)

elif role == "Teacher":
    st.subheader("Teacher Dashboard")
    student_ids = student_data["StudentID"].tolist()
    selected_id = st.selectbox("Select Student ID", student_ids)
    if selected_id:
        details = student_data[student_data["StudentID"] == selected_id]
        st.write("Student Details:")
        st.write(details)

elif role == "Student":
    st.subheader("Student Performance Prediction")

    # Dropdown for Gender
    gender = st.selectbox("Select Gender", ["Male", "Female"])
    gender_binary = 0 if gender == "Male" else 1

    # Dropdown for Age
    age = st.selectbox("Select Age", sorted(student_data['Age'].unique()))

    # Dropdown for Study Time Weekly
    study_time = st.selectbox("Study Time Weekly (hours)", ["0-5", "5-10", "10-15", "15-20"])
    study_time_range = [int(x) for x in study_time.split("-")]

    # Dropdown for Absences
    absences = st.selectbox("Absences", ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30"])
    absences_range = [int(x) for x in absences.split("-")]

    # Dropdown for Tutoring
    tutoring = st.selectbox("Tutoring", ["No", "Yes"])
    tutoring_binary = 0 if tutoring == "No" else 1

    # Dropdown for Extracurricular
    extracurricular = st.selectbox("Extracurricular", ["No", "Yes"])
    extracurricular_binary = 0 if extracurricular == "No" else 1

    # Use trained model to predict GPA and Grade
    prediction_gpa = model_gpa.predict([[gender_binary, age, study_time_range[0], absences_range[0], tutoring_binary, extracurricular_binary]])
    prediction_grade = model_grade.predict([[gender_binary, age, study_time_range[0], absences_range[0], tutoring_binary, extracurricular_binary]])

    st.write(f"Predicted GPA: {prediction_gpa[0]:.2f}")
    st.write(f"Predicted Grade: {['A', 'B', 'C', 'D', 'E'][int(prediction_grade[0])]}")

    # Graph 1: Grade distribution graph
    st.write("**Overall Grade Distribution:**")
    grade_counts = student_data['GradeClass'].value_counts()
    st.bar_chart(grade_counts)

    # Graph 2: Prediction visualization
    st.write("**Input-Based Prediction Graph:**")
    graph_data = pd.DataFrame({
        "Factors": ["Age", "Study Time", "Absences", "Tutoring", "Extracurricular", "Predicted GPA"],
        "Values": [
            age, study_time_range[0], absences_range[0], 
            tutoring_binary, extracurricular_binary, prediction_gpa[0]
        ]
    })
    st.bar_chart(graph_data.set_index("Factors"))
