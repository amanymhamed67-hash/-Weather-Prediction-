import streamlit as st
import pandas as pd
import joblib

# 1. ضبط إعدادات الصفحة
st.set_page_config(
    page_title="Weather Prediction App",
    page_icon="🌤️",
    layout="centered"
)

st.title("🌤️ Weather Prediction App")
st.write("Predict whether it will rain tomorrow using machine learning.")

# 2. تحميل الموديل
@st.cache_resource
def load_model():
    return joblib.load("weather_stacking_model.pkl")

model = load_model()

# 3. اختيار المدينة الأساسي (الواجهة الرئيسية)
location = st.selectbox("📍 Select Location", ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"])

# 4. إخفاء بقية البيانات المعقدة جوه قائمة Expander
with st.expander("⚙️ Advanced Weather Parameters (Default values set)"):
    st.caption("Adjust parameters below if you want to test custom weather conditions:")
    
    col1, col2 = st.columns(2)

    with col1:
        min_temp = st.number_input("Min Temperature (°C)", value=15.0)
        max_temp = st.number_input("Max Temperature (°C)", value=25.0)
        rainfall = st.number_input("Rainfall (mm)", value=0.0)
        temp9am = st.number_input("Temperature at 9 AM (°C)", value=18.0)
        temp3pm = st.number_input("Temperature at 3 PM (°C)", value=24.0)
        humidity9am = st.slider("Humidity at 9 AM (%)", 0, 100, 60)
        humidity3pm = st.slider("Humidity at 3 PM (%)", 0, 100, 50)

    with col2:
        pressure9am = st.number_input("Pressure at 9 AM", value=1015.0)
        pressure3pm = st.number_input("Pressure at 3 PM", value=1012.0)
        wind_gust_speed = st.number_input("Wind Gust Speed", value=30.0)
        wind_speed9am = st.number_input("Wind Speed at 9 AM", value=15.0)
        wind_speed3pm = st.number_input("Wind Speed at 3 PM", value=20.0)
        wind_gust_dir = st.selectbox("Wind Gust Direction", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        wind_dir9am = st.selectbox("Wind Direction at 9 AM", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        wind_dir3pm = st.selectbox("Wind Direction at 3 PM", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        rain_today = st.selectbox("Rain Today?", ["No", "Yes"])
        rain_yesterday = st.selectbox("Rain Yesterday?", ["No", "Yes"])

st.write("") # مسافة صغيرة

# 5. زر التوقع والنتيجة
if st.button("🚀 Predict Weather", use_container_width=True):

    input_data = pd.DataFrame([{
        'Location': location,
        'MinTemp': min_temp,
        'MaxTemp': max_temp,
        'Rainfall': rainfall,
        'Temp9am': temp9am,
        'Temp3pm': temp3pm,
        'Humidity9am': humidity9am,
        'Humidity3pm': humidity3pm,
        'Pressure9am': pressure9am,
        'Pressure3pm': pressure3pm,
        'WindGustSpeed': wind_gust_speed,
        'WindSpeed9am': wind_speed9am,
        'WindSpeed3pm': wind_speed3pm,
        'WindGustDir': wind_gust_dir,
        'WindDir9am': wind_dir9am,
        'WindDir3pm': wind_dir3pm,
        'RainToday': rain_today,
        'RainYestarDay': rain_yesterday
    }])

    prediction = model.predict(input_data)[0]

    st.markdown("---")

    if prediction == 'Yes' or prediction == 1:
        st.error(f"🌧️ **Prediction: High Chance of Rain Tomorrow in {location}!**")
    else:
        st.success(f"☀️ **Prediction: No Rain Expected Tomorrow in {location}!**")