# Carbon Footprint Calculator (Streamlit Application)
A web-based application that calculates an individual's monthly carbon footprint based on lifestyle parameters such as personal habits, travel, waste generation, energy usage, and consumption.
This project uses a custom, formula-based environmental model instead of machine learning.

---

## Features
### Formula-Based Emission Model
The app calculates emissions from:
* Personal factors (BMR, diet, social activity)
* Travel (transport mode, monthly distance, flights)
* Waste (bag size, frequency, recycling)
* Energy usage (power source, cooking systems, screen and internet usage)
* Consumption habits (grocery expenditure, clothing purchases, shower frequency)

### Modern UI
* Interactive Streamlit interface
* Custom CSS theme
* Dynamic pie-chart visualization
* Results page with interpreted CO₂ output and tree-equivalency metric

### Emission Breakdown
Displays contributions from:

* Personal
* Travel
* Waste
* Energy
* Consumption

### Easy Deployment
The application runs seamlessly on:
* Local machine
* Streamlit Cloud
* Codespaces
* Windows, macOS, and Linux

---

## Installation and Setup

### 1. Clone the Repository

```
git clone https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git
cd REPOSITORY_NAME
```

### 2. Create a Virtual Environment
```
python -m venv venv
```
### 3. Activate the Environment
Windows:
```
venv\Scripts\activate
```
macOS/Linux:
```
source venv/bin/activate
```
### 4. Install Required Packages
```
pip install -r requirements.txt
```
### 5. Run the Application
```
streamlit run app.py
```
---
## Model Overview
This application uses a custom rule-based carbon footprint model.
The logic is located in `carbonpath_model.py` and includes:

* Basal Metabolic Rate (BMR) calculations
* Diet-related CO₂ factors
* Standard emission coefficients per km for various transport modes
* Waste volume and recycling multipliers
* Energy usage estimates for heating, cooking, and electronics
* Consumption-based factors such as clothes and groceries
---
