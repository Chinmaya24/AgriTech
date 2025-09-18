from typing import Dict


_CROP_SYSTEM_PREF: Dict[str, str] = {
    "lettuce": "NFT",
    "basil": "NFT",
    "spinach": "NFT",
    "kale": "NFT",
    "tomato": "DWC",
    "pepper": "DWC",
    "cucumber": "DWC",
    "strawberry": "Kratky",
    "herb": "Kratky",
}


def _normalize(text: str) -> str:
    return (text or "").strip().lower()


def recommend_system(crop: str, space: str, budget: str, lighting: str) -> Dict[str, any]:
    crop_n = _normalize(crop)
    space_n = _normalize(space)
    budget_n = _normalize(budget)
    lighting_n = _normalize(lighting)

    # Enhanced crop to system mapping
    crop_system_map = {
        "lettuce": "NFT",
        "basil": "NFT", 
        "spinach": "NFT",
        "kale": "NFT",
        "arugula": "NFT",
        "mint": "NFT",
        "coriander": "NFT",
        "tomato": "DWC",
        "pepper": "DWC",
        "cucumber": "DWC",
        "eggplant": "DWC",
        "chilli": "DWC",
        "strawberry": "Kratky",
        "herb": "Kratky",
        "radish": "Kratky",
        "mustard": "Kratky",
        "rosemary": "Aeroponics",
        "peas": "Aeroponics",
        "beans": "Aeroponics"
    }
    
    base_system = crop_system_map.get(crop_n, "DWC")

    # Space adjustments
    if any(k in space_n for k in ["small", "tiny", "balcony", "rack", "shelf", "<1", "1-2"]):
        system = "Kratky" if base_system in ["Kratky", "NFT"] else "DWC"
    elif any(k in space_n for k in ["medium", "closet", "2-4", "cabinet"]):
        system = base_system
    else:  # large / room / greenhouse
        system = "NFT" if base_system == "NFT" else base_system

    # Component-wise base costs (per sq ft)
    component_costs = {
        "NFT": {
            "pvc_channels": 1200, "water_pump": 1500, "reservoir": 800, "net_pots": 300, "nutrients": 500, "timer": 400, "base_total": 4700
        },
        "DWC": {
            "tank": 1500, "air_pump": 800, "air_stones": 200, "net_pots": 400, "nutrients": 600, "ph_meter": 500, "base_total": 4000
        },
        "Kratky": {
            "container": 600, "net_pots": 200, "nutrients": 300, "ph_meter": 500, "base_total": 1600
        },
        "Aeroponics": {
            "mist_nozzles": 2000, "high_pressure_pump": 3000, "reservoir": 1000, "net_pots": 500, "nutrients": 800, "sensors": 1500, "led_lights": 2000, "base_total": 10800
        }
    }

    # Budget multipliers
    budget_multipliers = {
        "low": 0.6,
        "medium": 1.0, 
        "high": 1.5
    }
    
    multiplier = budget_multipliers.get(budget_n, 1.0)
    base_cost = component_costs[system]["base_total"]
    total_cost = int(base_cost * multiplier)
    
    # Cost breakdown
    cost_breakdown = {}
    for component, cost in component_costs[system].items():
        if component != "base_total":
            cost_breakdown[component.replace("_", " ").title()] = f"₹{int(cost * multiplier):,}"

    # Enhanced system characteristics matrix
    system_matrix = {
        "NFT": {
            "yield_kg_month": 8,
            "yield_quality": "Best",
            "water_efficiency": "High (90% less than soil)",
            "nutrient_efficiency": "High (precise delivery)", 
            "growth_speed": "Fast",
            "pest_resistance": "High",
            "maintenance": "Moderate",
            "setup_difficulty": "Intermediate",
            "recommended_crops": "Lettuce, Spinach, Kale, Basil, Arugula, Herbs, Mint, Coriander",
            "component_lifespan": "3-5 years",
            "first_harvest": "4-6 weeks",
            "yield_tips": "Maintain consistent flow, prevent root clogs, monitor pH daily, clean channels weekly"
        },
        "DWC": {
            "yield_kg_month": 6,
            "yield_quality": "Better",
            "water_efficiency": "Medium (70% less than soil)",
            "nutrient_efficiency": "High (constant access)",
            "growth_speed": "Fast", 
            "pest_resistance": "Medium",
            "maintenance": "Easy",
            "setup_difficulty": "Beginner",
            "recommended_crops": "Tomatoes, Peppers, Cucumbers, Lettuce, Spinach, Chilli, Eggplant",
            "component_lifespan": "4-6 years",
            "first_harvest": "6-8 weeks",
            "yield_tips": "Keep water oxygenated, change solution weekly, maintain proper spacing, check roots regularly"
        },
        "Kratky": {
            "yield_kg_month": 4,
            "yield_quality": "Good",
            "water_efficiency": "High (85% less than soil)",
            "nutrient_efficiency": "Medium (passive uptake)",
            "growth_speed": "Moderate",
            "pest_resistance": "High", 
            "maintenance": "Easy",
            "setup_difficulty": "Beginner",
            "recommended_crops": "Lettuce, Spinach, Herbs, Small leafy greens, Radish, Mustard",
            "component_lifespan": "2-3 years",
            "first_harvest": "5-7 weeks",
            "yield_tips": "Don't refill reservoir, use proper container size, avoid over-crowding, monitor water level"
        },
        "Aeroponics": {
            "yield_kg_month": 10,
            "yield_quality": "Best",
            "water_efficiency": "High (90% less than soil)",
            "nutrient_efficiency": "High (precise misting)",
            "growth_speed": "Fast",
            "pest_resistance": "High",
            "maintenance": "Hard",
            "setup_difficulty": "Advanced",
            "recommended_crops": "Herbs, Lettuce, High-value vegetables, Commercial crops, Rosemary, Peas, Beans",
            "component_lifespan": "5-7 years",
            "first_harvest": "3-5 weeks",
            "yield_tips": "Monitor mist cycles closely, maintain sterile environment, use quality sensors, backup power essential"
        }
    }

    # Lighting advice
    if lighting_n in ("low", "shade", "weak"):
        light = "Full-spectrum LED, 35-40W per sq ft"
    elif lighting_n in ("medium", "partial", "indirect"):
        light = "Full-spectrum LED, 25-30W per sq ft"
    elif lighting_n in ("high", "sunny", "outdoor", "natural"):
        light = "Leverage natural light; supplement LED as needed"
    else:
        light = "LED grow light (full-spectrum), 30W per sq ft"

    # Get system characteristics
    characteristics = system_matrix[system]
    
    # Detailed system descriptions
    detailed_descriptions = {
        "NFT": "Plants grow in sloped channels where a thin flow of nutrient solution passes over the roots. Ideal for leafy greens like lettuce, spinach, and herbs. Uses very little water (up to 90% less than soil). Components: PVC channels, net pots, small pump, reservoir. Cost: Moderate. Maintenance: Moderate, requires checking flow and preventing clogs. First harvest: 4–6 weeks. Best for small to medium setups with good sunlight or LED lighting.",
        
        "DWC": "Plants float on a raft with roots submerged in oxygenated nutrient solution. Suitable for medium to large leafy greens, tomatoes, peppers, and cucumbers. Growth is fast due to constant nutrient access. Components: Tank, air pump, net pots, nutrient solution. Cost: Moderate to high. Maintenance: Moderate (oxygenation, nutrient monitoring). First harvest: 6–8 weeks. Water-efficient and stable for beginners with slightly larger space.",
        
        "Kratky": "Simple passive hydroponics. Plants sit in a container with nutrient solution and roots partially submerged. No pump required. Very low cost. Best for small leafy crops like lettuce or spinach. Components: Container, net pots, nutrient solution. Maintenance: Easy, but growth is slower. First harvest: 5–7 weeks. Great for beginners or low-budget setups.",
        
        "Aeroponics": "Roots hang in the air and are periodically misted with nutrient solution. Extremely fast growth and highest yield. Suitable for high-value crops like herbs, lettuce, or commercial vegetables. Components: Mist nozzles, reservoir, pump, sensors, LED lighting. Cost: High. Maintenance: Advanced, requires careful control of mist, nutrients, and environment. First harvest: 3–5 weeks. Water-efficient (80–90% less than soil), precise nutrient delivery."
    }
    
    return {
        "system": system,
        "cost": f"₹{total_cost:,}",
        "light": light,
        "yield": f"{characteristics['yield_kg_month']} kg/month",
        "yield_quality": characteristics["yield_quality"],
        "water_efficiency": characteristics["water_efficiency"],
        "nutrient_efficiency": characteristics["nutrient_efficiency"],
        "growth_speed": characteristics["growth_speed"],
        "pest_resistance": characteristics["pest_resistance"],
        "maintenance": characteristics["maintenance"],
        "setup_difficulty": characteristics["setup_difficulty"],
        "recommended_crops": characteristics["recommended_crops"],
        "component_lifespan": characteristics["component_lifespan"],
        "first_harvest": characteristics["first_harvest"],
        "yield_tips": characteristics["yield_tips"],
        "cost_breakdown": cost_breakdown,
        "system_description": detailed_descriptions[system]
    }


def nutrient_recipe(crop: str) -> Dict[str, str]:
    crop_n = _normalize(crop)
    recipes: Dict[str, Dict[str, str]] = {
        "tomato": {
            "npk": "10-5-18",
            "ph": "5.8–6.3",
            "ec": "2.0–3.5 mS/cm",
            "daily_water": "1.5–2.5 L/plant",
        },
        "pepper": {
            "npk": "12-6-18",
            "ph": "5.8–6.2",
            "ec": "2.0–3.0 mS/cm",
            "daily_water": "1.0–2.0 L/plant",
        },
        "cucumber": {
            "npk": "8-4-14",
            "ph": "5.8–6.0",
            "ec": "1.8–2.7 mS/cm",
            "daily_water": "2.0–3.0 L/plant",
        },
        "lettuce": {
            "npk": "8-10-12",
            "ph": "5.8–6.2",
            "ec": "1.0–1.6 mS/cm",
            "daily_water": "0.3–0.6 L/plant",
        },
    }

    if crop_n not in recipes:
        return {
            "npk": "10-5-15",
            "ph": "5.8–6.2",
            "ec": "1.2–2.0 mS/cm",
            "daily_water": "0.5–2.0 L/plant",
        }

    return recipes[crop_n]


