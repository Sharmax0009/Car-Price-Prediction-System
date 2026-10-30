"""Streamlit web UI.  Run:  streamlit run app.py"""
import json
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent / "src"))
from config import CURRENCY, METRICS_PATH  # noqa: E402
from predict import load_model, predict_price  # noqa: E402


@st.cache_resource(show_spinner="Preparing model (first launch only)...")
def get_model():
    return load_model()


get_model()

st.set_page_config(page_title="Car Price Predictor", page_icon="🚗")
st.title("🚗 Car Price Prediction")

c1, c2 = st.columns(2)
brand = c1.selectbox("Brand", ["Maruti", "Hyundai", "Honda", "Toyota", "Ford",
                               "Volkswagen", "BMW", "Mercedes", "Audi"])
fuel = c2.selectbox("Fuel type", ["Petrol", "Diesel", "CNG", "Electric"])
trans = c1.selectbox("Transmission", ["Manual", "Automatic"])
owner = c2.selectbox("Owner", ["First", "Second", "Third"])
age = c1.slider("Age (years)", 0, 20, 5)
km = c2.number_input("Kilometres driven", 0, 500000, 50000, step=1000)
engine = c1.number_input("Engine (cc, 0 for EV)", 0, 6000, 1500, step=100)
power = c2.number_input("Power (hp)", 30.0, 700.0, 110.0)
mileage = c1.number_input("Mileage (km/l, 0 for EV)", 0.0, 40.0, 18.0)
seats = c2.selectbox("Seats", [2, 4, 5, 7], index=2)

if st.button("Predict price", type="primary"):
    r = predict_price(dict(brand=brand, fuel_type=fuel, transmission=trans, owner_type=owner,
                           age=age, km_driven=km, engine_cc=engine, power_hp=power,
                           mileage_kmpl=mileage, seats=seats))
    st.metric("Estimated price", f"{CURRENCY}{r['price']:,.0f}")
    st.caption(f"Likely range: {CURRENCY}{r['low']:,.0f} – {CURRENCY}{r['high']:,.0f}")

if METRICS_PATH.exists():
    m = json.loads(METRICS_PATH.read_text())
    with st.expander("Model performance"):
        st.write(f"Best model: **{m['best_model']}**")
        st.json(m["results"][m["best_model"]])
