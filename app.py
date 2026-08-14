import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Student Predictor", page_icon="🎓", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load("student_performance_model.pkl")

model = load_model()

with st.sidebar:
    st.title("Project")
    st.write("Student performance prediction using Random Forest.")
    st.divider()
    st.write("Developer: Amit Sharma")
    st.write("Course: B.Tech CSE - Data Science")
    st.write("College: Greater Noida Institute of Technology")

st.title("Student Performance Predictor")
st.write("Enter the details below.")
st.divider()

st.subheader("Student Details")

col1, col2, col3 = st.columns(3)

with col1:
    attendance = st.number_input("Attendance (%)", 0.0, 100.0, 85.0)
    prev_exam = st.number_input("Previous Exam", 0.0, 100.0, 75.0)
    prev_sem = st.number_input("Previous Semester", 0.0, 100.0, 75.0)

with col2:
    assignments = st.number_input("Assignment", 0.0, 100.0, 80.0)
    internal = st.number_input("Internal Assessment", 0.0, 100.0, 78.0)
    study_hours = st.number_input("Study Hours", 0.0, 14.0, 4.0)

with col3:
    participation = st.number_input("Participation (%)", 0.0, 100.0, 70.0)
    sleep = st.number_input("Sleep Hours", 4.0, 10.0, 7.0)
    st.write("")
    predict = st.button("Predict")

if predict:
    data = pd.DataFrame({
        "Attendance Percentage": [attendance],
        "Previous Exam Score": [prev_exam],
        "Previous Semester Score": [prev_sem],
        "Assignment Score": [assignments],
        "Internal Assessment Score": [internal],
        "Study Hours per Day": [study_hours],
        "Class Participation Percentage": [participation],
        "Sleep Hours per Day": [sleep]
    })

    prediction = model.predict(data)[0]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Result")
        st.metric("Final Score", f"{prediction:.1f} / 100")

        if prediction >= 85:
            st.success("Excellent")
        elif prediction >= 70:
            st.info("Good")
        else:
            st.warning("Needs Improvement")

    with col2:
        st.subheader("Feature Importance")

        importance = pd.DataFrame({
            "Feature": data.columns,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=True)

        st.bar_chart(importance.set_index("Feature"))
