import streamlit as st
import base64
from streamlit.components.v1 import html

# import your model
from carbonpath_model import (
    personal_emissions,
    travel_emissions,
    waste_emissions,
    energy_emissions,
    consumption_emissions
)

# import utils
from functions import click_element, chart, compute_breakdown


st.set_page_config(layout="wide", page_title="Carbon Footprint Calculator", page_icon="./media/favicon.ico")


# ---------------------- IMAGE LOADING ----------------------
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()

background = get_base64("./media/background_min.jpg")
icon2 = get_base64("./media/icon2.png")
icon3 = get_base64("./media/icon3.png")

with open("./style/style.css", "r") as style:
    css = f"<style>{style.read().format(background=background, icon2=icon2, icon3=icon3)}</style>"
    st.markdown(css, unsafe_allow_html=True)


def script():
    with open("./style/scripts.js", "r", encoding="utf-8") as scripts:
        html(f"<script>{scripts.read()}</script>", width=0, height=0)


# ---------------------- LAYOUT ----------------------
left, middle, right = st.columns([2, 3.5, 2])
main, comps, result = middle.tabs([" ", " ", " "])

with open("./style/main.md", "r", encoding="utf-8") as main_page:
    main.markdown(main_page.read())

_, but, _ = main.columns([1, 2, 1])
if but.button("Calculate Your Carbon Footprint!", type="primary"):
    click_element("tab-1")


tab1, tab2, tab3, tab4, tab5 = comps.tabs(
    ["👴 Personal", "🚗 Travel", "🗑️ Waste", "⚡ Energy", "💸 Consumption"]
)

tab_result, _ = result.tabs([" ", " "])


# ---------------------- FORM INPUTS ----------------------
def component():
    # PERSONAL
    p1, p2 = tab1.columns(2)
    height = p1.number_input("Height (cm)", 0, 251, value=160)
    weight = p2.number_input("Weight (kg)", 0, 250, value=75)

    sex = tab1.selectbox("Gender", ["female", "male"])
    diet = tab1.selectbox("Diet", ['omnivore', 'pescatarian', 'vegetarian', 'vegan'])
    social = tab1.selectbox("Social Activity", ['never', 'often', 'sometimes'])

    # TRAVEL
    transport = tab2.selectbox("Transportation", ['public', 'private', 'walk/bicycle'])
    if transport == "private":
        vehicle_type = tab2.selectbox("Vehicle Type", ['petrol', 'diesel', 'hybrid', 'lpg', 'electric'])
    else:
        vehicle_type = "None"

    vehicle_km = 0 if transport == "walk/bicycle" else tab2.slider("Monthly Vehicle Distance (km)", 0, 5000, 100)

    air_travel = tab2.selectbox("Flights Last Month", ['never', 'rarely', 'frequently', 'very frequently'])
    flight_map = {"never": 0, "rarely": 1, "frequently": 2, "very frequently": 3}

    # WASTE
    waste_bag = tab3.selectbox("Waste Bag Size", ['small', 'medium', 'large', 'extra large'])
    waste_count = tab3.slider("Waste Bags per Week", 0, 10, 2)
    recycle = tab3.multiselect("Recycled Materials", ['Plastic', 'Paper', 'Metal', 'Glass'])

    # ENERGY
    heating_energy = tab4.selectbox("Heating Energy Source", ['natural gas', 'electricity', 'wood', 'coal'])
    for_cooking = tab4.multiselect("Cooking Systems", ['microwave', 'oven', 'grill', 'airfryer', 'stove'])
    energy_eff = tab4.selectbox("Energy Efficiency", ['No', 'Yes', 'Sometimes'])
    tv_hours = tab4.slider("Daily TV/PC Hours", 0, 24, 5)
    internet_hours = tab4.slider("Daily Internet Hours", 0, 24, 6)

    cooking_system = for_cooking[0] if for_cooking else "stove"

    # CONSUMPTION
    shower = tab5.selectbox("Shower Frequency", ['daily', 'twice a day', 'more frequently', 'less frequently'])
    grocery = tab5.slider("Grocery Bill ($)", 0, 500, 200)
    clothes = tab5.slider("Clothes Bought Monthly", 0, 30, 5)

    return {
        "height": height,
        "weight": weight,
        "sex": sex,
        "diet": diet,
        "social": social,
        "transport": transport,
        "vehicle_km": vehicle_km,
        "vehicle_type": vehicle_type,
        "flights": flight_map[air_travel],
        "waste_bag": waste_bag,
        "waste_count": waste_count,
        "recycles": recycle,
        "heating_energy": heating_energy,
        "cooking_system": cooking_system,
        "efficiency": energy_eff,
        "tv_hours": tv_hours,
        "internet_hours": internet_hours,
        "shower": shower,
        "grocery": grocery,
        "clothes": clothes
    }


ui = component()


# ---------------------- SESSION DEFAULTS ----------------------
if "prediction" not in st.session_state:
    st.session_state.prediction = 0
if "breakdown" not in st.session_state:
    st.session_state.breakdown = {}


# ---------------------- RESULT BUTTON ----------------------
_, resultbutton, _ = tab5.columns([1, 1, 1])

if resultbutton.button("View Result", type="secondary"):

    # compute fresh values
    personal = personal_emissions(ui["height"], ui["weight"], ui["sex"], ui["diet"], ui["social"])
    travel = travel_emissions(ui["transport"], ui["vehicle_km"], ui["flights"])
    waste = waste_emissions(ui["waste_bag"], ui["waste_count"], len(ui["recycles"]) > 0)
    energy = energy_emissions(ui["heating_energy"], ui["cooking_system"], ui["efficiency"],
                              ui["tv_hours"], ui["internet_hours"])
    consumption = consumption_emissions(ui["shower"], ui["grocery"], ui["clothes"])

    breakdown = compute_breakdown(personal, travel, waste, energy, consumption)
    prediction = round(sum(breakdown.values()))

    # store in session
    st.session_state.prediction = prediction
    st.session_state.breakdown = breakdown

    tab_result.image(chart(breakdown, prediction), use_container_width=True)
    click_element("tab-2")


# ---------------------- RESULT PAGE ----------------------
prediction = st.session_state.prediction
breakdown = st.session_state.breakdown

tree_count = round(prediction / 411.4)

tab_result.markdown(
    f"You owe nature <b>{tree_count}</b> tree{'s' if tree_count != 1 else ''} monthly.",
    unsafe_allow_html=True
)

if tab_result.button("🏡 Go to Home", type="secondary"):
    click_element("tab-0")


# ---------------------- FOOTER ----------------------
with open("./style/footer.html", "r", encoding="utf-8") as footer:
    st.markdown(footer.read(), unsafe_allow_html=True)

script()
