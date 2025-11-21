# -*- coding: utf-8 -*-
"""
Cleaned carbonpath_model.py
Contains only function definitions for CO₂ estimation modules.
"""

# -----------------------------
# PERSONAL MODULE
# -----------------------------

def calc_bmr(height_cm, weight_kg, age=25, gender='female'):
    """
    Calculate Basal Metabolic Rate (Mifflin-St Jeor formula).
    """
    s = 5 if gender.lower() in ('male', 'm') else -161
    return 10 * weight_kg + 6.25 * height_cm - 5 * age + s


def personal_emissions(height_cm, weight_kg, gender, diet, social_activity, age=25):
    """
    Estimate personal-related monthly CO₂ emissions (kg/month) using rough factors.
    Returns a dict with components and the total monthly kg CO₂.
    """
    # Diet emission factors (tonnes CO2 per year)
    DIET_TPY = {"vegan": 1.5, "vegetarian": 1.7, "omnivore": 2.5, "high-meat": 3.5}

    # Convert diet to kg CO2 per month
    diet_tpy = DIET_TPY.get(diet.lower(), DIET_TPY['omnivore'])
    diet_kg_month = (diet_tpy * 1000) / 12  # tonnes → kg, year → month

    # Metabolic emissions from BMR (very rough conversion)
    KCAL_TO_CO2_KG = 0.001  # rough conversion: 1 kcal ≈ 0.001 kg CO₂
    bmr = calc_bmr(height_cm, weight_kg, age, gender)
    metabolic_kg_month = (bmr * KCAL_TO_CO2_KG * 365) / 12  # kcal/day → per month

    # Apply social activity multiplier
    social_map = {"never": 1.0, "sometimes": 1.1, "frequent": 1.2}
    social_mult = social_map.get(social_activity.lower(), 1.0)

    # Final monthly CO₂
    total_personal_kg_month = (diet_kg_month * social_mult) + metabolic_kg_month

    return {
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "gender": gender,
        "diet": diet,
        "social_activity": social_activity,
        "bmr": round(bmr, 2),
        "diet_kg_month": round(diet_kg_month, 2),
        "metabolic_kg_month": round(metabolic_kg_month, 2),
        "social_multiplier": social_mult,
        "total_personal_kg_month": round(total_personal_kg_month, 2)
    }


# -----------------------------
# TRAVEL MODULE
# -----------------------------

def travel_emissions(transport_mode, monthly_km, flights_per_month):
    """
    Estimate travel-related monthly CO₂ emissions (kg/month).
    transport_mode: 'car','motorcycle','bus','train','bike','none'
    monthly_km: monthly road distance
    flights_per_month: integer count of flights per month
    """
    TRANSPORT_KG_PER_KM = {
        "car": 0.20,
        "motorcycle": 0.12,
        "bus": 0.08,
        "train": 0.05,
        "bike": 0.0,
        "none": 0.0
    }
    FLIGHT_KG_PER_FLIGHT = 250  # rough average per short/medium flight

    mode = (transport_mode or "none").lower()
    km_factor = TRANSPORT_KG_PER_KM.get(mode, TRANSPORT_KG_PER_KM['none'])

    road_kg_month = monthly_km * km_factor
    flights_kg_month = flights_per_month * FLIGHT_KG_PER_FLIGHT

    total_travel_kg_month = road_kg_month + flights_kg_month

    return {
        "transport_mode": transport_mode,
        "monthly_km": monthly_km,
        "flights_per_month": flights_per_month,
        "road_kg_month": round(road_kg_month, 2),
        "flights_kg_month": round(flights_kg_month, 2),
        "total_travel_kg_month": round(total_travel_kg_month, 2)
    }


# -----------------------------
# WASTE MODULE
# -----------------------------

def waste_emissions(waste_size, bags_per_week, recycle):
    """
    Estimate waste-related monthly CO₂ emissions (kg/month).
    recycle: boolean (True if recycling reduces waste emissions)
    """
    WASTE_KGCO2_PER_BAG = {
        "small": 5,
        "medium": 8,
        "large": 12,
        "extralarge": 15
    }

    size = (waste_size or "medium").lower().replace(" ", "")
    per_bag_kg = WASTE_KGCO2_PER_BAG.get(size, WASTE_KGCO2_PER_BAG["medium"])

    monthly_bags = bags_per_week * 4
    recycle_multiplier = 0.8 if recycle else 1.0

    total_waste_kg_month = monthly_bags * per_bag_kg * recycle_multiplier

    return {
        "waste_size": waste_size,
        "bags_per_week": bags_per_week,
        "monthly_bags": monthly_bags,
        "recycle": bool(recycle),
        "per_bag_kg_co2": per_bag_kg,
        "recycle_multiplier": recycle_multiplier,
        "total_waste_kg_month": round(total_waste_kg_month, 2)
    }


# -----------------------------
# ENERGY MODULE
# -----------------------------

def energy_emissions(power_source, cooking_system, efficient_devices,
                     pc_hours_per_day, internet_hours_per_day):
    """
    Estimate energy-related monthly CO₂ emissions (kg/month).
    efficient_devices: expected values 'yes','sometimes','no' (case-insensitive)
    cooking_system: string (one of microwave/oven/grill/airfryer/stove)
    """
    ENERGY_BASE_MONTHLY = {
        "natural gas": 120,
        "electricity": 180,
        "wood": 90,
        "coal": 300
    }
    COOKING_SYSTEM_KG = {
        "microwave": 15,
        "oven": 30,
        "grill": 40,
        "airfryer": 20,
        "stove": 25
    }
    EFFICIENCY_MULT = {
        "yes": 0.9,
        "sometimes": 1.0,
        "no": 1.1
    }

    base = ENERGY_BASE_MONTHLY.get((power_source or "electricity").lower(), ENERGY_BASE_MONTHLY["electricity"])
    cooking = COOKING_SYSTEM_KG.get((cooking_system or "stove").lower(), 25)
    eff_mult = EFFICIENCY_MULT.get((efficient_devices or "sometimes").lower(), 1.0)

    pc_monthly_kg = pc_hours_per_day * 30 * 0.05
    internet_monthly_kg = internet_hours_per_day * 30 * 0.03

    total_energy_kg_month = (base + cooking) * eff_mult + pc_monthly_kg + internet_monthly_kg

    return {
        "power_source": power_source,
        "cooking_system": cooking_system,
        "efficient_devices": efficient_devices,
        "pc_hours_per_day": pc_hours_per_day,
        "internet_hours_per_day": internet_hours_per_day,
        "base_kg_month": base,
        "cooking_kg_month": cooking,
        "efficiency_multiplier": eff_mult,
        "pc_kg_month": round(pc_monthly_kg, 2),
        "internet_kg_month": round(internet_monthly_kg, 2),
        "total_energy_kg_month": round(total_energy_kg_month, 2)
    }


# -----------------------------
# CONSUMPTION MODULE
# -----------------------------

def consumption_emissions(shower_freq, grocery_spend_rs, clothes_per_month):
    """
    Estimate consumption-related monthly CO₂ emissions (kg/month).
    grocery_spend_rs: monthly grocery spending (assumed currency, used as number)
    clothes_per_month: integer
    """
    SHOWER_KG_PER_MONTH = {
        "less frequently": 30,
        "daily": 90,
        "twice a day": 120,
        "more frequently": 150
    }

    shower = SHOWER_KG_PER_MONTH.get((shower_freq or "daily").lower(), 90)

    groceries_kg = grocery_spend_rs * 0.1
    clothes_kg = clothes_per_month * 10

    total_consumption_kg_month = shower + groceries_kg + clothes_kg

    return {
        "shower_freq": shower_freq,
        "grocery_spend_rs": grocery_spend_rs,
        "clothes_per_month": clothes_per_month,
        "shower_kg_month": shower,
        "groceries_kg_month": round(groceries_kg, 2),
        "clothes_kg_month": clothes_kg,
        "total_consumption_kg_month": round(total_consumption_kg_month, 2)
    }

# End of file - no top-level execution or tests.
