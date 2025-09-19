# Fertilizers mapping
fertilizers = {
    "urea": {
        "alternative": "🌿 Vermicompost, Panchagavya, Jeevamrutha",
        "benefits": "Improves soil fertility, provides balanced nutrients, enhances microbial activity.",
        "impact": "❌ Urea harms soil long-term. ✅ Organic compost increases soil carbon, reduces cost, and improves resilience.",
        "procedure": """Vermicompost:
1. Prepare shaded pit/container, add waste + dung + worms.
2. Cover, sprinkle water, compost ready in 45–60 days.
Panchagavya:
1. Ferment cow dung, urine, milk, curd, ghee, bananas, jaggery, coconut water.
2. Stir daily for 20 days, dilute before use.
Jeevamrutha:
1. Mix cow dung, urine, jaggery, pulse flour, soil in water.
2. Ferment 5–7 days, apply in irrigation water.""",
        "dosage": "Vermicompost: 2–5 tons/acre; Panchagavya: 3% foliar spray every 15 days; Jeevamrutha: 200 liters/acre every 15 days."
    },
    "dap": {
        "alternative": "🌱 Rock Phosphate + Cow Manure",
        "benefits": "Provides slow-release phosphorus and improves soil structure.",
        "impact": "❌ DAP causes nutrient imbalance. ✅ Rock phosphate enriches soil naturally.",
        "procedure": """Mix rock phosphate powder with cow dung, compost for 30–40 days before application.""",
        "dosage": "Apply 100–150 kg rock phosphate + 1 ton cow manure per acre before sowing."
    },
    "npk": {
        "alternative": "🌿 Green Manure + Farmyard Manure",
        "benefits": "Adds NPK naturally, improves soil structure.",
        "impact": "❌ NPK salts reduce soil microbes. ✅ Green manure supports healthy soil life.",
        "procedure": """Green Manure: Grow sunhemp/dhaincha for 30–40 days, plough in soil.
Farmyard Manure: Collect dung, urine, straw, compost 2–3 months, then apply.""",
        "dosage": "Green manure: 8–10 kg seed/acre; FYM: 5–10 tons/acre before sowing."
    },
    "mop": {
        "alternative": "🌱 Wood Ash, Banana Stem Compost, Seaweed Extract",
        "benefits": "Supplies potassium naturally, improves plant immunity.",
        "impact": "❌ MOP leads to soil salinity. ✅ Wood ash & seaweed are eco-friendly.",
        "procedure": """Wood Ash: Collect and apply near root zone.
Banana Stem Compost: Chop, mix with dung, compost 40 days.
Seaweed Extract: Dilute before spraying.""",
        "dosage": "Wood ash: 100–200 kg/acre; Banana compost: 1–2 tons/acre; Seaweed extract: 50 ml/10 liters water, foliar spray every 20 days."
    },
    "zinc sulphate": {
        "alternative": "🌿 Zinc-rich biofertilizers, Cow Dung, Rock Dust",
        "benefits": "Provides zinc slowly, improves soil microbes.",
        "impact": "❌ Excess ZnSO₄ harms soil. ✅ Natural sources are safer.",
        "procedure": """Apply rock dust or slurry of cow dung with biofertilizers during land prep.""",
        "dosage": "Rock dust: 250–500 kg/acre; Zinc biofertilizer: 1–2 kg/acre mixed with compost."
    }
}

# Pesticides mapping
pesticides = {
    "pesticide": {
        "alternative": "🦗 Neem Oil Spray, Garlic-Chili Extract, Cow Urine Solution",
        "benefits": "Repels harmful insects without killing pollinators.",
        "impact": "❌ Chemical pesticides kill beneficial insects. ✅ Herbal sprays are eco-safe.",
        "procedure": """Neem Oil: Mix neem oil + soap + water, spray evening.
Garlic-Chili Extract: Grind, boil, filter, dilute before spraying.
Cow Urine: Dilute, ferment 3–5 days, spray.""",
        "dosage": "Neem oil: 30 ml/liter water; Garlic-Chili: 100 ml extract/10 liters water; Cow urine: 5 liters urine + 20 liters water per acre spray."
    },
    "insecticide": {
        "alternative": "🐞 Neem Oil, Soap Spray, Intercropping with Marigold",
        "benefits": "Controls pests, supports pollinators, reduces residues.",
        "impact": "❌ Insecticides contaminate food. ✅ Organic methods produce healthier crops.",
        "procedure": """Neem spray & soap spray as repellents; Marigold intercrop to repel pests.""",
        "dosage": "Neem oil: 30 ml/liter water weekly; Soap spray: 20 g/liter water; Marigold: 4000–5000 plants/acre between main crops."
    },
    "carbofuran": {
        "alternative": "🌿 Neem Seed Powder, Trichogramma Bio-control",
        "benefits": "Effective against soil pests safely.",
        "impact": "❌ Highly toxic. ✅ Neem-based products are safe.",
        "procedure": """Neem seeds dried & powdered; sprinkle in soil.
Trichogramma egg cards released in field.""",
        "dosage": "Neem powder: 250 g/10 m² soil; Trichogramma: 10–12 cards/acre every 15 days."
    },
    "monocrotophos": {
        "alternative": "🌱 Herbal Pesticides + Sticky Traps",
        "benefits": "Controls sucking pests safely.",
        "impact": "❌ Deadly. ✅ Herbal solutions protect farmer health.",
        "procedure": """Sticky traps coated with oil/grease; Herbal sprays (neem, garlic).""",
        "dosage": "Sticky traps: 8–10 per acre; Herbal spray: 100 ml decoction/10 liters water every 7–10 days."
    },
    "glyphosate": {
        "alternative": "🌿 Mulching, Hand Weeding, Cow-based Herbicides",
        "benefits": "Controls weeds, improves soil moisture.",
        "impact": "❌ Carcinogenic. ✅ Organic methods save water, enrich soil.",
        "procedure": """Mulch soil with straw/leaves; Hand weed at intervals; Spray fermented cow dung + urine mix.""",
        "dosage": "Mulch: 2–3 tons dry biomass/acre; Hand weeding: every 20–25 days; Cow-based herbicide: 2–3 liters fermented solution in 20 liters water, spray per acre."
    },
    "endosulfan": {
        "alternative": "🐞 Neem Oil, Bacillus thuringiensis (Bt), Bio-control",
        "benefits": "Targets pests safely without harming humans.",
        "impact": "❌ Banned. ✅ Organic methods protect environment & health.",
        "procedure": """Neem spray for sucking pests; Bt spray for caterpillars; Release ladybird beetles.""",
        "dosage": "Neem oil: 30 ml/liter water; Bt powder: 2 g/liter water; Bio-control insects: 2000–3000/acre release."
    },
    "mancozeb": {
        "alternative": "🍄 Neem Decoction, Garlic Extract, Whey Spray",
        "benefits": "Effective against leaf spots naturally.",
        "impact": "❌ Leaves residues. ✅ Herbal sprays are safe.",
        "procedure": """Boil neem leaves; make garlic paste decoction; dilute whey for spraying.""",
        "dosage": "Neem decoction: 500 ml/10 liters water; Garlic extract: 50 ml/10 liters water; Whey: 1 liter whey in 9 liters water, foliar spray every 10 days."
    },
    "captan": {
        "alternative": "🌿 Cow Urine + Asafoetida Mixture",
        "benefits": "Prevents seedling rot naturally.",
        "impact": "❌ Contaminates soil. ✅ Cow-based solutions promote soil life.",
        "procedure": """Mix cow urine + asafoetida in water, apply to seedlings.""",
        "dosage": "Cow urine mix: 1 liter urine + 10 g asafoetida + 10 liters water, applied at seedling stage."
    }
}

def suggest_fertilizer(input_text):
    input_text = input_text.lower().strip()
    if input_text in fertilizers:
        return fertilizers[input_text]
    return {
        "alternative": "✅ Use compost, green manure & biofertilizers.",
        "benefits": "Supports soil fertility and sustainable farming.",
        "impact": "Healthy soil, better yields, safe food.",
        "procedure": "General composting/vermicompost methods can be used.",
        "dosage": "Compost: 2–5 tons/acre applied before sowing."
    }

def suggest_pesticide(input_text):
    input_text = input_text.lower().strip()
    if input_text in pesticides:
        return pesticides[input_text]
    return {
        "alternative": "✅ Use Neem, Garlic-Chili sprays, or bio-control methods.",
        "benefits": "Safe, eco-friendly, and cost-effective.",
        "impact": "Protects crops, soil, pollinators, and your health.",
        "procedure": "Neem spray or garlic extract applied weekly in evening.",
        "dosage": "Neem oil: 30 ml/liter water; Garlic extract: 100 ml/10 liters water."
    }
