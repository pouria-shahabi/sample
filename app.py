
# =================================================
# Tehran House Price Prediction - Streamlit App
# =================================================

import streamlit as st
import pandas as pd
import joblib

data = pd.read_csv("tehranhouses.csv")

addresses=data.Address.value_counts()
small_addresses=addresses[addresses<5].index.to_list()
large_addresses=addresses[addresses>=5].index.to_list()
def Area_to_number(X):
  X=X.copy()
  X['Area']=X['Area'].str.replace('\D+','',regex=True).astype(int)
  return X

def clip_Area(X):
  X=X.copy()
  X['Area']=X['Area'].clip(20,1000)
  return X

def map_Address(X):
  X=X.copy()
  for i in X.Address:
    if i in small_addresses or i=='Other':
      X.loc[X.Address==i,'Address']='Other'
    elif i in large_addresses:
      X.loc[X.Address==i,'Address']=i
    else:
      X.loc[X.Address==i,'Address']='Other'
  return X
# ------------------------
# Load مدل و دیتاست
# ------------------------
model = joblib.load("Best_Model.pkl")



# ------------------------
# عنوان و توضیح اپ
# ------------------------
st.title("Tehran House Price Prediction 🏠")
st.write("لطفاً ویژگی‌های خانه را وارد کنید:")

# ------------------------
# ورودی کاربر
# ------------------------
area = st.text_input("متراژ (متر مربع)", "100")  # پیش‌فرض 100

room = st.number_input("تعداد اتاق", min_value=0, max_value=5, value=2)
elevator = st.selectbox("آسانسور دارد؟", [0, 1])
parking = st.selectbox("پارکینگ دارد؟", [0, 1])
warehouse = st.selectbox("انباری دارد؟", [0, 1])
address_options = data['Address'].unique().tolist()
address = st.selectbox("محله", address_options)

# ------------------------
# پیش‌بینی با مدل
# ------------------------
if st.button("پیش‌بینی قیمت"):
    input_data = pd.DataFrame({
        'Area': [area],
        'Room': [room],
        'Elevator': [elevator],
        'Parking': [parking],
        'Warehouse': [warehouse],
        'Address': [address]
    })

    prediction = model.predict(input_data)
    st.success(f"قیمت پیش‌بینی شده: {prediction[0]:,.0f} تومان")
