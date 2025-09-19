# Fertilizers mapping
fertilizers = {
    "urea": {
        "alternative": "🌿 Vermicompost, Panchagavya, Jeevamrutha",
        "benefits": "Improves soil fertility, provides balanced nutrients, enhances microbial activity.",
        "impact": "❌ Urea harms soil long-term. ✅ Organic compost increases soil carbon, reduces cost, and improves resilience."
    },
    "dap": {
        "alternative": "🌱 Rock Phosphate + Cow Manure",
        "benefits": "Provides slow-release phosphorus and improves soil structure.",
        "impact": "❌ DAP causes nutrient imbalance. ✅ Rock phosphate enriches soil naturally."
    },
    "npk": {
        "alternative": "🌿 Green Manure + Farmyard Manure",
        "benefits": "Adds NPK naturally, improves soil structure.",
        "impact": "❌ NPK salts reduce soil microbes. ✅ Green manure supports healthy soil life."
    },
    "mop": {
        "alternative": "🌱 Wood Ash, Banana Stem Compost, Seaweed Extract",
        "benefits": "Supplies potassium naturally, improves plant immunity.",
        "impact": "❌ MOP leads to soil salinity. ✅ Wood ash & seaweed are eco-friendly."
    },
    "zinc sulphate": {
        "alternative": "🌿 Zinc-rich biofertilizers, Cow Dung, Rock Dust",
        "benefits": "Provides zinc slowly, improves soil microbes.",
        "impact": "❌ Excess ZnSO₄ harms soil. ✅ Natural sources are safer."
    }
}

# Pesticides mapping
pesticides = {
    "pesticide": {
        "alternative": "🦗 Neem Oil Spray, Garlic-Chili Extract, Cow Urine Solution",
        "benefits": "Repels harmful insects without killing pollinators.",
        "impact": "❌ Chemical pesticides kill beneficial insects. ✅ Herbal sprays are eco-safe."
    },
    "insecticide": {
        "alternative": "🐞 Neem Oil, Soap Spray, Intercropping with Marigold",
        "benefits": "Controls pests, supports pollinators, reduces residues.",
        "impact": "❌ Insecticides contaminate food. ✅ Organic methods produce healthier crops."
    },
    "carbofuran": {
        "alternative": "🌿 Neem Seed Powder, Trichogramma Bio-control",
        "benefits": "Effective against soil pests safely.",
        "impact": "❌ Highly toxic. ✅ Neem-based products are safe."
    },
    "monocrotophos": {
        "alternative": "🌱 Herbal Pesticides + Sticky Traps",
        "benefits": "Controls sucking pests safely.",
        "impact": "❌ Deadly. ✅ Herbal solutions protect farmer health."
    },
    "glyphosate": {
        "alternative": "🌿 Mulching, Hand Weeding, Cow-based Herbicides",
        "benefits": "Controls weeds, improves soil moisture.",
        "impact": "❌ Carcinogenic. ✅ Organic methods save water, enrich soil."
    },
    "endosulfan": {
        "alternative": "🐞 Neem Oil, Bacillus thuringiensis (Bt), Bio-control",
        "benefits": "Targets pests safely without harming humans.",
        "impact": "❌ Banned. ✅ Organic methods protect environment & health."
    },
    "mancozeb": {
        "alternative": "🍄 Neem Decoction, Garlic Extract, Whey Spray",
        "benefits": "Effective against leaf spots naturally.",
        "impact": "❌ Leaves residues. ✅ Herbal sprays are safe."
    },
    "captan": {
        "alternative": "🌿 Cow Urine + Asafoetida Mixture",
        "benefits": "Prevents seedling rot naturally.",
        "impact": "❌ Contaminates soil. ✅ Cow-based solutions promote soil life."
    }
}

def suggest_fertilizer(input_text):
    input_text = input_text.lower().strip()
    if input_text in fertilizers:
        return fertilizers[input_text]
    return {
        "alternative": "✅ Use compost, green manure & biofertilizers.",
        "benefits": "Supports soil fertility and sustainable farming.",
        "impact": "Healthy soil, better yields, safe food."
    }

def suggest_pesticide(input_text):
    input_text = input_text.lower().strip()
    if input_text in pesticides:
        return pesticides[input_text]
    return {
        "alternative": "✅ Use Neem, Garlic-Chili sprays, or bio-control methods.",
        "benefits": "Safe, eco-friendly, and cost-effective.",
        "impact": "Protects crops, soil, pollinators, and your health."
    }
