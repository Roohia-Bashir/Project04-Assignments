import streamlit as st

st.set_page_config(page_title="BMI Calculator", layout="centered")

st.title("🧮 BMI Calculator")
st.write("Calculate your **Body Mass Index (BMI)** easily with different units!")

# Unit Selection
st.subheader("Select Units")

height_unit = st.selectbox("Height Unit", ["Meters", "Feet & Inches", "Feet (e.g., 5.5)"])
weight_unit = st.selectbox("Weight Unit", ["Kilograms", "Pounds"])

# Height Input
if height_unit == "Meters":
    height_m = st.number_input("Enter your height (in meters):", min_value=0.5, max_value=2.5, step=0.01)

elif height_unit == "Feet & Inches":
    feet = st.number_input("Feet:", min_value=0, max_value=8, step=1)
    inches = st.number_input("Inches:", min_value=0, max_value=11, step=1)
    total_inches = feet * 12 + inches
    height_m = total_inches * 0.0254  # Convert to meters

else:  # Feet (decimal)
    feet_decimal = st.number_input("Enter your height in feet (e.g., 5.5):", min_value=1.0, max_value=8.0, step=0.01)
    height_m = feet_decimal * 0.3048  # Convert to meters

# Weight Input
if weight_unit == "Kilograms":
    weight_kg = st.number_input("Enter your weight (in kg):", min_value=10.0, max_value=300.0, step=0.5)
else:
    weight_lb = st.number_input("Enter your weight (in pounds):", min_value=22.0, max_value=660.0, step=0.5)
    weight_kg = weight_lb * 0.453592  # Convert to kg

# BMI Calculation
if st.button("Calculate BMI"):
    if height_m > 0 and weight_kg > 0:
        bmi = weight_kg / (height_m ** 2)
        st.success(f"Your BMI is: {bmi:.2f}")

        # Interpretation
        if bmi < 18.5:
            st.warning("You are underweight.")
        elif 18.5 <= bmi < 24.9:
            st.info("You have a normal weight.")
        elif 25 <= bmi < 29.9:
            st.warning("You are overweight.")
        else:
            st.error("You are obese.")
    else:
        st.error("Please enter valid height and weight.")
