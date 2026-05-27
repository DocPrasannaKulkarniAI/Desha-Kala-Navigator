"""
pathya_apathya.py
District-aware Pathya (wholesome) and Apathya (unwholesome) food guidance.
Loads district-specific food availability from Excel dataset.
Combines: Rutu × Desha × District geography × Clinical condition.
"""
import os
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# RUTU PATHYA – APATHYA  (Seasonal dietary guidance)
# ─────────────────────────────────────────────────────────────────────────────
RUTU_PATHYA_APATHYA = {
    "Vasanta": {
        "dosha_phase": "Kapha Prakopa",
        "ahara_principle": "Laghu (light), Ushna (warm), Tikta-Katu-Kashaya dominant. Counter Kapha unctuousness with dry, rough, astringent foods.",
        "pathya": {
            "cereals": ["Yava (Barley) — primary Kapha-pacifying grain", "Shyamaka (Barnyard millet)", "Old Shali rice (Purana Shali)", "Jowar (Sorghum)"],
            "pulses": ["Moong dal (whole/split) — Laghu, easy to digest", "Kulthi (Horse gram) — Tikta, Ruksha, Agni-kindling", "Masoor dal (Red lentil)"],
            "vegetables": ["Bitter gourd (Karela / Pavakka) — Tikta, Kapha-pacifying", "Drumstick (Moringa / Muringakkai)", "Neem leaves (Nimba patra) — classical Vasanta vegetable", "Pointed gourd (Patola / Parval)", "Agathi leaves (Sesbania)", "Methi (Fenugreek) leaves", "Bottle gourd (Dudhi)"],
            "fruits": ["Amalaki (Indian gooseberry) — Tridoshahara, best Vasanta fruit", "Dry fruits in moderation (Raisins, Dates — small quantity)", "Unripe mango with salt and pepper"],
            "oils": ["Minimal oil use; Mustard oil (Sarshapa taila) preferred if needed — Ruksha, Ushna"],
            "beverages": ["Warm water throughout day (Ushna Jala)", "Ginger-black pepper tea (Shunti-Maricha)", "Honey in warm water (do NOT heat honey — add to warm, not boiling)", "Nagarmotha (Cyperus) water"],
            "dairy": ["Honey (Madhu) — the best Vasanta food pairing", "Buttermilk (Takra) — diluted, spiced with cumin and ginger"],
            "classical_note": "AH Su 3.20: Vasante Laghu-Ushna-Tikta-Katu-Kashaya-Aharam Seveta — in Vasanta, consume light, warm, bitter, pungent, and astringent foods.",
        },
        "apathya": {
            "cereals": ["Freshly harvested rice (Nava Shali — heavy)", "Wheat-based heavy preparations (chapati, bread)", "Maida (refined wheat flour)"],
            "pulses": ["Urad dal (Black gram) — heavy, Kapha-promoting", "Rajma (Kidney beans)", "Chana dal in large quantities"],
            "vegetables": ["Sweet potato (Sheeta, Guru — Kapha aggravating)", "Colocasia/Arbi (Kapha, Pitta promoting)", "Excess salad (raw cold vegetables)"],
            "fruits": ["Banana (heavy, Kapha — limit)", "Jackfruit (very Guru)", "Avocado", "Watermelon (cold, Sheeta)"],
            "beverages": ["Cold water and cold drinks", "Milk in large quantities (Kapha-promoting)", "Alcohol"],
            "others": ["Daytime sleep (Divaswapna) — strongly contraindicated in Vasanta", "Heavy, oily, deep-fried foods", "Curd (Dadhi) — especially at night", "Excess sweet foods (Madhura — aggravates Kapha)"],
            "classical_note": "CS Su 6.25: Avoid Snigdha (unctuous), Guru (heavy), Sheeta (cold), Madhura (sweet) foods in Vasanta — these aggravate the already-elevated Kapha.",
        },
    },
    "Grishma": {
        "dosha_phase": "Pitta Sanchaya + Vata Sanchaya",
        "ahara_principle": "Madhura (sweet), Sheeta (cool), Drava (liquid), Snigdha (unctuous). Focus on hydration and heat management.",
        "pathya": {
            "cereals": ["Shali rice (light, cooling)", "Yava (Barley) — sattu (roasted barley flour with water) is the classical summer drink", "Rice porridge (Kanji / Congee)"],
            "pulses": ["Moong dal — lightest, cooling", "Masoor dal", "Toor dal (moderate)"],
            "vegetables": ["Ash gourd (Kumbalanga / Petha) — cooling, Pitta-pacifying", "Cucumber (Kakdi / Kheera) — high water content", "Ridge gourd (Toori / Peechinga)", "Snake gourd (Padavalanga / Chichinda)", "Tender coconut kernel"],
            "fruits": ["Watermelon (Tarbuz) — primary Grishma fruit", "Musk melon (Kharbuja)", "Ripe mango with milk (in moderation)", "Grapes (Draksha) — Madhura, cooling", "Pomegranate (Anar)", "Coconut water (Nariyal pani) — best Grishma beverage"],
            "oils": ["Coconut oil (Narikela taila) — cooling, Pitta-pacifying", "Ghee (Ghrita) in moderate quantity — Sheeta Virya"],
            "beverages": ["Coconut water throughout day", "Buttermilk (Takra) — diluted, cooling", "Shatavari milk (cold)", "Coriander seed water (Dhanyaka jala)", "Rose water (Gulkand in milk)"],
            "dairy": ["Milk (Kshira) — cooled, with cardamom and sugar", "Ghee", "Gulkand (rose petal preserve)"],
            "classical_note": "CS Su 6.29: Grishme Madhura-Sheeta-Dravya Sevyate — in Grishma, sweet and cool preparations are recommended. AH Su 3.36: Madhura-Sheeta-Drava-Snigdha-Bhojana-Sevana.",
        },
        "apathya": {
            "cereals": ["Heavy bajra rotis in excess", "Deep-fried preparations (Bhatura, Puri)"],
            "pulses": ["Urad dal", "Rajma", "Heavy lentil preparations"],
            "vegetables": ["Garlic (Lasuna) — Tikshna, Ushna — Pitta aggravating in excess", "Onion raw in large qty", "Bitter gourd in excess (Ruksha — dehydrating)"],
            "fruits": ["Sour citrus in excess (lemon, tamarind — Amla, Pitta-aggravating)", "Unripe fruits"],
            "beverages": ["Alcohol", "Hot tea/coffee in excess", "Carbonated drinks"],
            "others": ["Spicy foods (Katu — Tikshna, Ushna)", "Excessive salt", "Midday sun exposure + hot food combination", "Fasting (causes gastric Pitta surge)", "Vigorous exercise in afternoon heat"],
            "classical_note": "AH Su 3.38: Avoid Tikshna (sharp), Amla (sour), Lavana (salty), Katu (pungent) in Grishma — these aggravate Pitta and cause dehydration.",
        },
    },
    "Varsha": {
        "dosha_phase": "Vata Prakopa + Pitta Sanchaya",
        "ahara_principle": "Amla-Lavana-Sneha-Yuktam (slightly sour, salt, with fat) but LAGHU (light) overall. Agni is at weakest — all food must support Agni, never challenge it.",
        "pathya": {
            "cereals": ["Old Shali rice (Purana Shali) — Laghu, easy to digest in Manda Agni state", "Yava (Barley) — Deepana, Agni-kindling", "Moong rice (Kitchari — mung + rice) — THE definitive Varsha staple"],
            "pulses": ["Moong dal ONLY — all other pulses are Guru and contraindicated in Varsha", "Toor dal (in small quantity if Agni confirmed adequate)"],
            "vegetables": ["Patola (Pointed gourd) — specifically recommended in CS for Varsha", "Parval", "Tender drumstick", "Well-cooked bitter gourd", "Avoid all raw/leafy vegetables"],
            "fruits": ["Pomegranate (Anar) — Agni-kindling, Dosha-balancing", "Ripe banana (small Nendran variety — cooked or ripe)", "Dates in moderation"],
            "oils": ["Sesame oil (Tila taila) — Vata-pacifying, warm", "Ghee — moderate, Agni-supporting"],
            "beverages": ["BOILED WATER ONLY (Ushna Jala) — most critical Varsha rule", "Ginger-long pepper tea", "Musta (Nagarmotha) water — Deepana", "Panchakola decoction (Shunti, Pippali, Maricha, Chavya, Chitraka)"],
            "dairy": ["Well-boiled milk only", "Buttermilk (Takra) with ginger and cumin — best Varsha dairy preparation", "Avoid curd/yogurt"],
            "classical_note": "AH Su 3.41: Varsha Ritou Amla-Lavana-Sneha-Yuktam Laghu Bhojana — light food with sour, salt, and fat in Varsha. CS Vi 3.6: Boiled water is essential in Varsha to prevent epidemics.",
        },
        "apathya": {
            "cereals": ["Freshly harvested new grains — all Nava Dhanya are Guru and Ama-forming in Varsha", "Maida", "Heavy wheat preparations"],
            "pulses": ["Urad dal — strictly avoid (very heavy, Ama-forming)", "Rajma", "Chana", "Mixed lentil soups (Panchmel dal)"],
            "vegetables": ["ALL raw leafy vegetables — bacteria and parasite contamination risk in monsoon", "Riverbank vegetables", "Root vegetables unless well-cooked"],
            "fruits": ["Watery fruits in excess (watermelon — adds to Kapha)", "Unripe fruits", "Fruits from flooded/contaminated areas"],
            "beverages": ["Unboiled water — ABSOLUTE contraindication", "Cold water", "River/well water without boiling", "Alcohol", "Cold milk"],
            "others": ["Daytime sleep (Divaswapna) — weakens already-impaired Agni", "Exercise in rain", "Heavy meals", "Stale food", "Curd/yogurt (Dadhi) — Ama-forming in Manda Agni state"],
            "classical_note": "CS Vi 3: Varsha Apathya is primarily about food safety and Agni protection. Any food that challenges the weakened Agni is contraindicated. 'Navam Dhanyam Tyajet' (avoid new/fresh grains).",
        },
    },
    "Sharad": {
        "dosha_phase": "Pitta Prakopa (annual peak)",
        "ahara_principle": "Madhura (sweet), Tikta (bitter), Kashaya (astringent), Laghu (light). Cool, cooling, non-fermented. This is the highest Pitta-risk season.",
        "pathya": {
            "cereals": ["Shali rice (Shashtika — 60-day rice — specifically recommended)", "Yava (Barley)", "Wheat (moderate — Madhura, Sheeta Virya)"],
            "pulses": ["Moong dal", "Masoor dal", "Toor dal (moderate — avoid excess Amla fermented dishes with it)"],
            "vegetables": ["Patola (Pointed gourd) — Tikta, Pitta-pacifying", "Bitter gourd (Karela) — Tikta, classical Sharad vegetable", "Cucumber", "Ash gourd (Kumbalanga)", "Guduchi (Tinospora) — Tikta, Pitta-balancing"],
            "fruits": ["Amalaki (Indian gooseberry) — primary Sharad fruit; Tridoshahara but especially Pitta-cooling", "Pomegranate (Anar)", "Ripe coconut", "Sweet lime (Mosambi)", "Grapes (Draksha)"],
            "oils": ["Ghee (Tikta Ghrita specially — with Neem, Guduchi, Patola)", "Coconut oil"],
            "beverages": ["Coriander-cumin-fennel water (Dhanyaka-Jira-Shatapushpa)", "Rose water / Gulkand milk", "Tender coconut water", "Khas (vetiver) water"],
            "dairy": ["Milk (Kshira) with Shatavari — cooling, Pitta-pacifying", "Ghee", "Avoid large quantities of curd"],
            "classical_note": "CS Su 6.43: Sharad Pitta Prakopa — Tikta (bitter), Madhura (sweet), Kashaya (astringent) dominant diet. AH Su 3.50: Tikta Ghrita Visheshena — Tikta Ghrita is specially recommended in Sharad.",
        },
        "apathya": {
            "cereals": ["Freshly harvested rice (Nava Shali)", "Heavy fried preparations"],
            "pulses": ["Urad dal", "Fermented preparations (Idli/Dosa — Amla, Pitta-aggravating in Sharad)"],
            "vegetables": ["Garlic (Lasuna) in excess", "Onion raw", "Eggplant/Brinjal in excess (Pitta-promoting in Sharad)"],
            "fruits": ["Sour fruits in excess (Tamarind, Raw mango, Lime in excess)", "Fermented fruit products"],
            "beverages": ["Alcohol — strictly avoid in Pitta Prakopa season", "Hot spicy drinks", "Fermented beverages"],
            "others": ["Daytime sleep in direct sun (Atapa Svapanam — specifically mentioned in AH as Sharad Apathya)", "Dew exposure at night", "Eastern wind exposure (Purva Vayu — Pitta-aggravating per classics)", "Excessive physical exertion in midday heat"],
            "classical_note": "AH Su 3.53: Sharad Apathya — Tila (sesame in excess), Mulaka (radish in excess), Dadhi (curd), Alkali, Sarshapa (mustard in excess). CS Su 6.46: Avoid Purva Vayu and early morning dew exposure.",
        },
    },
    "Hemanta": {
        "dosha_phase": "Vata Prashama + Kapha Sanchaya",
        "ahara_principle": "Snigdha (unctuous), Ushna (warm), Guru (heavy), Madhura-Amla-Lavana. Strongest Agni — nourish, build, and strengthen. Brumhana season.",
        "pathya": {
            "cereals": ["Wheat (Godhuma) — Madhura, Snigdha, Brumhana — primary Hemanta grain", "New Shali rice (Nava Shali — now appropriate, unlike Varsha)", "Jowar", "Maize (Makka)"],
            "pulses": ["Urad dal (black gram) — Brumhana, Vata-pacifying — specifically recommended in Hemanta", "Moong dal", "Rajma (kidney beans) in moderate quantities"],
            "vegetables": ["Yam (Surana / Jimikand) — Brumhana, Vata-pacifying", "Colocasia (Arbi / Chembu) — nourishing", "Sweet potato", "Carrots", "Beets", "Methi (Fenugreek) leaves — Deepana, Vata-pacifying", "Garlic (Lasuna) — Vata-pacifying, warmth-generating"],
            "fruits": ["Dates (Kharjura) — Brumhana, Ojas-building — specifically recommended", "Dry figs", "Fresh dates", "Anar (Pomegranate)", "Banana", "Ripe jackfruit"],
            "oils": ["Sesame oil (Tila taila) — Vata-pacifying, warmth-generating — primary Hemanta oil", "Ghee (Ghrita) — generously recommended", "Mustard oil (for cooking in North India)"],
            "beverages": ["Warm milk with Ashwagandha, Shatavari, and Ghee — classical Hemanta tonic", "Jaggery (Guda) warm water", "Kadha (herbal decoction — Trikatu based)", "Warm spiced milk"],
            "dairy": ["Milk (Kshira) — generously recommended in Hemanta; all dairy welcome", "Curd (Dadhi) — now appropriate (unlike Varsha)", "Ghee", "Butter (Navanita)"],
            "classical_note": "CS Su 6.7: Hemante Snigdha-Ushna-Guru-Lavana-Amla-Madhura-Ahara — unctuous, warm, heavy, salty, sour, sweet foods recommended. AH Su 3.56: Hemante Agni Diptataro Bhavati — Agni burns strongest.",
        },
        "apathya": {
            "cereals": ["Very cold, stale preparations", "Raw uncooked grains"],
            "pulses": ["Very light preparations (do not under-eat in Hemanta)"],
            "vegetables": ["Bitter gourd in excess (Tikta — Vata-aggravating in cold season)", "All raw cold salads"],
            "beverages": ["Cold water (Sheeta Jala) — avoid; use warm water", "Iced drinks", "Excess alcohol (short-term warmth, long-term Vata-Pitta aggravation)"],
            "others": ["Fasting or eating too little (Alpabhojana) — weakens the strong Agni paradoxically leading to Sama", "Exposure to cold wind (Vata-Kapha aggravating)", "Excess Tikta-Kashaya-Katu (bitter-astringent-pungent) combinations in cold"],
            "classical_note": "Hemanta Apathya is mainly about under-eating and cold exposure. The strong Agni of Hemanta requires adequate caloric and nutritive input — starvation in Hemanta produces Dhatu Kshaya.",
        },
    },
    "Shishira": {
        "dosha_phase": "Kapha Sanchaya + Vata residual",
        "ahara_principle": "Same as Hemanta — Snigdha, Ushna, Guru, Brumhana diet. Tikshna Agni requires good quality nourishing food. Begin gradually reducing heavy foods in last week (Ritusandhi preparation).",
        "pathya": {
            "cereals": ["Wheat preparations (Godhuma — rotis, upma, khichdi)", "Old Shali rice", "Maize / Corn"],
            "pulses": ["Urad dal preparations (Dal Makhani, Vada)", "Moong dal", "Kulthi (Horse gram) — Ruksha, Deepana — useful to begin in late Shishira for Kapha-preparation"],
            "vegetables": ["Root vegetables — Carrot, Beet, Yam, Sweet potato", "Garlic", "Ginger (Shunti) — generously in cooking", "Fenugreek (Methi)", "Spinach"],
            "fruits": ["Dates", "Figs", "Amla (Amalaki)", "Pomegranate", "Citrus fruits (warmth from Vitamin C is supportive)"],
            "oils": ["Sesame oil", "Ghee", "Mustard oil"],
            "beverages": ["Warm spiced milk", "Tulsi-Ginger-Honey warm water", "Sesame-jaggery (Til-Guda) preparations — classical winter food"],
            "dairy": ["All dairy — generously recommended"],
            "classical_note": "CS Su 6.13: Shishira Ritucharya same as Hemanta — 'Shishira Ritou Balam Uttamam, Hemanta Sadrusha Ritucharya.' Begin Kapha-preparation in last week with slightly lighter foods.",
        },
        "apathya": {
            "beverages": ["Cold water", "Cold drinks"],
            "others": ["Cold wind exposure (Sheeta Vayu)", "Insufficient clothing", "Under-eating", "Beginning heavy Shodhana (Vamana is premature — wait for Vasanta Kapha Prakopa)", "Daytime sleeping in cold"],
            "classical_note": "Shishira Apathya: cold exposure and insufficient nourishment are the primary risks. Begin Udwartana (dry powder massage) in the last 7 days of Shishira to prepare for the transition to Vasanta Vamana protocol.",
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# CONDITION-SPECIFIC PATHYA-APATHYA
# ─────────────────────────────────────────────────────────────────────────────
CONDITION_PATHYA = {
    "Amlapitta": {
        "pathya": "Old Shali rice, Yava (barley), Moong dal, Amalaki, Shatavari, Tikta Ghrita, Patola, bitter gourd, cow's milk (cold), tender coconut water, Draksha (grapes), Khajura (dates).",
        "apathya": "Fermented foods (Idli, Dosa, Vinegar, Alcohol), Amla-dominant fruits (Tamarind, raw mango), spicy/fried food, curd (especially at night), Rajma, Urad dal, tomatoes in excess, citrus in excess.",
        "seasonal_note": "Amlapitta is worst in Sharad (Pitta Prakopa) and Varsha (atmospheric acid). Observe strict Apathya in these two seasons; Tikta Ghrita + Shatavari Churna are the definitive Hemanta-Shishira prevention protocol.",
    },
    "Amavata": {
        "pathya": "Shunti (dry ginger) water throughout day, Kitchari (moong + old rice), Yava, Kulthi (horse gram), Lasuna (garlic — small quantity), Trikatu, Panchakola, Patola, Bitter gourd, well-cooked Moringa.",
        "apathya": "Viruddha Ahara (incompatible food combinations — fish + milk, etc.), Curd/Dadhi (Ama-forming), cold water, heavy pulses (Urad, Rajma, Chana), Junk food, leftover/refrigerated food, fish, Nava Dhanya (fresh grains).",
        "seasonal_note": "Amavata is most aggravated in Varsha and Shishira (cold-damp). Shunti is the single most important dietary addition year-round. Avoid ALL Ama-forming foods especially during Varsha.",
    },
    "Tamaka Shwasa": {
        "pathya": "Ginger (fresh or dry), Pippali (long pepper), Tulsi, Honey, Old rice, Yava, Moong dal, Garlic (small qty), warm spiced water, pomegranate, Hridya preparations (cardamom-cinnamon milk).",
        "apathya": "Bananas (Sheeta, Kapha-promoting), cold water and cold foods, curd (Dadhi), heavy dairy (buffalo milk), fried foods, sesame in excess, Rajma, Urad dal, White rice in excess, Maida.",
        "seasonal_note": "Worst in Vasanta, Varsha, and Hemanta. Vamana in Vasanta is the definitive annual Samshodhana. Avoid ALL cold-damp triggers in Varsha-Hemanta. Dhoomapana with Haridra-Guggulu beneficial in Kapha-season mornings.",
    },
    "Sandhivata": {
        "pathya": "Sesame (Tila — Snehana), Garlic (Lasuna) in ghee, Shallots (Shunti), Ginger, Fenugreek seeds, Dashamoola decoction, Ashwagandha, Bala taila massage, warm sesame oil self-massage.",
        "apathya": "Cold water (especially bathing in cold water), cold/windy environment, excessive bitter/astringent foods, fasting, raw vegetables, nightshade family (tomato, eggplant, potato) in excess.",
        "seasonal_note": "Worst in Varsha (Vata Prakopa) and Shishira (cold-Vata). Basti in Varsha is the annual treatment window. Sesame oil Abhyanga is a non-negotiable daily practice for Sandhivata patients.",
    },
    "Madhumeha": {
        "pathya": "Yava (barley — the primary Pathya grain for Prameha), Kulthi (horse gram), Moong dal, Bitter gourd (Karela), Fenugreek (Methi), Turmeric water, Neem, Amalaki, Jamun (Syzygium), Triphala.",
        "apathya": "White rice in large quantity, Maida, sugar and all sweets, potatoes in excess, Urad dal, Banana, Jackfruit, Mango (ripe, sweet), Grapes (sweet), alcohol, sedentary lifestyle.",
        "seasonal_note": "Worst in Anupa Desha and sedentary patients in Varsha-Hemanta. Udwartana (dry powder massage) with Triphala is specifically indicated for Madhumeha. Kulatha and Yava must replace Shali rice as the primary grain.",
    },
    "Kasa": {
        "pathya": "Honey (Madhu), Ginger (fresh and dry), Pippali, Tulsi, Vasaka (Adhatoda) preparation, warm milk with turmeric, Sitopladi Churna, old rice, warm barley water.",
        "apathya": "Cold water and cold foods, curd/yogurt, banana, cold dairy, fried food, Urad dal, exposure to cold/dust/smoke.",
        "seasonal_note": "Worst in Varsha (cold-damp) and Hemanta-Shishira (cold). Sitopladi Churna with honey is the definitive Kasa formula. Avoid cold at all times.",
    },
    "Kushtha": {
        "pathya": "Bitter vegetables (Karela, Nimba), Tikta Ghrita, Haridra (turmeric), Khadira (Acacia catechu), Nimba (Neem), Triphala, old rice, Yava, Patola.",
        "apathya": "Fish with milk (Viruddha Ahara — classical Kushtha cause), fermented foods, alcohol, excessive salt, sesame in Pitta-dominant Kushtha, hot spicy food, incompatible food combinations.",
        "seasonal_note": "Worst in Sharad (Pitta Prakopa) and Varsha (humidity, fungal aggravation). Virechana in Sharad is the definitive annual Samshodhana. Tikta Ghrita as Snehapana prevents seasonal Kushtha flares.",
    },
    "Hridroga": {
        "pathya": "Arjuna (bark preparation), Punarnava, Garlic in ghee, moong dal, old rice, Ashwagandha (Kapha type), Shatavari (Pitta type), light exercise, warm cow milk.",
        "apathya": "Heavy saturated fats (Ghee in excess — only in specific Vata-type), deep fried foods, Maida, sugar, excess salt, sedentary lifestyle, emotional stress, Urad in excess.",
        "seasonal_note": "Worst in Hemanta-Shishira (cold stress, Kapha-Vata) and Grishma (heat/dehydration cardiovascular stress). Arjuna Kshira Paka is the definitive Hemanta-Shishira preventive formula.",
    },
    "Grahani": {
        "pathya": "Buttermilk (Takra) — the most important Grahani Pathya, Pomegranate (Anar), Bilwa (Bael fruit), Musta (Cyperus), Chitrak, Shunti, old rice-moong Kitchari.",
        "apathya": "Fermented foods, cold water, leafy vegetables in raw form, Maida, Rajma, Urad, spicy food, alcohol, irregular eating times.",
        "seasonal_note": "Worst in Varsha (Manda Agni peak) and seasonal transitions. Takrarishta is the classical Grahani formula — prescribed year-round with dose increase in Varsha.",
    },
    "Pandu": {
        "pathya": "Pomegranate (Anar) — primary Pathya, Draksharishta, fresh green vegetables (Spinach, Moringa), Amla (Amalaki), Sesame, Draksha, dates, copper vessel water (Tamra Jala).",
        "apathya": "Spicy hot food, alcohol, tobacco, black gram (Urad), sesame in excess, sour fermented preparations.",
        "seasonal_note": "Worst in Grishma (heat stress on Rakta) and Sharad (Pitta Prakopa + Rakta Dushthi). Punarnavadi Mandura is the definitive formula; Raktamokshana in Sharad for Pittaja Pandu.",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# DESHA FOOD MODIFIERS (overlay onto Rutu guidance)
# ─────────────────────────────────────────────────────────────────────────────
DESHA_FOOD_MODIFIERS = {
    "ANUPA": {
        "principle": "Counter inherent Kapha-Pitta tendency. Prefer Ruksha (dry), Laghu (light), Ushna (warm) foods even outside their normal Rutu season. Reduce dairy, cold foods, and heavy grains year-round.",
        "always_prefer": ["Yava (barley) over heavy rice", "Kulthi (horse gram)", "Bitter vegetables", "Dry spices (Trikatu)", "Light oils (mustard, small quantity)"],
        "always_reduce": ["Heavy dairy (buffalo milk, paneer in excess)", "Maida", "Cold water and cold foods", "Banana in excess", "Curd at night"],
        "local_specifics": {
            "Kerala": "Coconut oil (moderate use) is appropriate despite Anupa classification — coconut is Madhura, Sheeta Virya but locally metabolised well. Matta/Rosematta rice (hand-pounded) is preferred over white polished rice. Kudampuli (Garcinia cambogia) in cooking naturally counteracts Kapha.",
            "West Bengal": "Mustard oil (Sarshapa taila — Tikshna, Ushna) counteracts Anupa Kapha tendency well. Use generously in cooking. Pointed gourd (Potol) and Bitter gourd are important Anupa-counterbalancing vegetables.",
            "Assam/Northeast": "Bamboo shoots (Tikta, Ruksha) and fermented preparations (traditional) are locally appropriate Kapha-pacifying foods. However, reduce excess fermentation in Varsha-Sharad.",
        },
    },
    "JANGALA": {
        "principle": "Counter inherent Vata-Pitta tendency. Ensure adequate Snigdha (unctuous), Madhura (sweet), Guru (heavy enough) food to counterbalance environmental dryness. Extra emphasis on hydration and oil intake.",
        "always_prefer": ["Ghee (Ghrita) — liberally", "Sesame (Tila) and sesame oil", "Dates (Kharjura) and dry fruits", "Milk preparations", "Root vegetables", "Whole wheat with ghee"],
        "always_reduce": ["Dry, light, Ruksha foods already in excess from environment", "Excessive bitter/astringent in Vata-predominant patients", "Cold/dry foods in winter"],
        "local_specifics": {
            "Rajasthan": "Bajra (pearl millet) roti is the foundation grain — Guru, Ushna, excellent Vata-pacifier for Jangala region. Ker-Sangri (desert beans+berries) are traditional Rajasthani Jangala foods aligned with seasonal availability. Lassi (buttermilk) is the traditional Pitta-pacifier in Grishma.",
            "Punjab/Haryana": "Sarson da saag (mustard greens) + Makki di roti is the classical Hemanta Pathya for this Jangala-Sadharana region — Ushna, nutritive, Vata-pacifying. Ghee on roti is clinically appropriate here — do not restrict in Jangala patients.",
        },
    },
    "SADHARANA": {
        "principle": "No fixed Desha bias — focus on Rutu-specific guidance and individual Prakruti. Maintain balance of all three Gunas. Standard seasonal Pathya-Apathya applies without strong modification.",
        "always_prefer": ["Balanced diet following Rutu guidance strictly", "Local seasonal produce", "Moderate use of all food groups"],
        "always_reduce": ["No specific restriction beyond Rutu guidance"],
        "local_specifics": {
            "Karnataka (Deccan)": "Ragi (Finger millet / Nachni) is the foundation grain — Kashaya, Ruksha, Deepana — excellent for Sadharana-Jangala districts of Karnataka. Ragi mudde with Soppu saaru (greens broth) is a classic seasonal meal.",
            "Maharashtra (Deccan)": "Jowar bhakri is the foundational grain for Maharashtra Sadharana districts — Madhura, Laghu. Ambadi (Gongura/Roselle) is Amla-Tikta and Pitta-pacifying — important seasonal vegetable.",
        },
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# GEO-ZONE BASED LOCALLY AVAILABLE STABLE FOODS
# (Used as the fallback when district not in the Excel)
# ─────────────────────────────────────────────────────────────────────────────
GEO_ZONE_STABLE_FOODS = {
    "South India - Coastal (Kerala, Konkan, Tamil Nadu Coast)": {
        "cereals": "Rice (Matta/Rosematta, Jeerakasala, Navara varieties), Ragi",
        "pulses": "Toor dal, Urad dal (for Idli/Dosa batter), Moong dal, Horse gram (Kulthi/Kollu)",
        "vegetables": "Drumstick (Muringakkai), Ash gourd (Kumbalanga), Bitter gourd (Pavakka), Snake gourd (Padavalanga), Colocasia (Chembu), Yam (Chena), Banana flower, Jackfruit (raw and ripe), Agathi leaves",
        "fruits": "Banana (Nendran, Poovan, Robusta), Coconut (Narikela), Jackfruit, Mango, Pineapple, Guava, Papaya",
        "oils": "Coconut oil (primary), Sesame oil",
        "spices": "Black pepper, Long pepper (Pippali), Cardamom, Ginger, Turmeric, Curry leaves, Asafoetida",
        "dairy": "Cow's milk, Buttermilk (Moru), Ghee",
    },
    "South India - Inland (Karnataka Deccan, Tamil Nadu Plains, Telangana)": {
        "cereals": "Ragi (primary), Rice, Jowar, Bajra, Wheat",
        "pulses": "Toor dal, Horse gram (Kulthi), Moong, Urad, Groundnuts (Chana in Karnataka)",
        "vegetables": "Brinjal, Tomato, Onion, Moringa, Bitter gourd, Gongura/Ambadi (Roselle)",
        "fruits": "Banana, Pomegranate, Guava, Papaya, Mango (seasonal)",
        "oils": "Groundnut oil, Sesame oil, Coconut oil (coastal influence)",
        "spices": "Mustard, Curry leaves, Turmeric, Coriander, Cumin, Red chilli, Asafoetida (Hing)",
        "dairy": "Cow/buffalo milk, Curd (Majjige), Ghee, Buttermilk",
    },
    "West India - Coastal (Maharashtra Coast, Goa, Gujarat Coast)": {
        "cereals": "Rice, Jowar, Bajra, Nachni (Ragi), Wheat",
        "pulses": "Toor dal, Chana, Matki (Moth beans), Vaal (Field beans), Kulith (Horse gram)",
        "vegetables": "Dudhi (Bottle gourd), Karela (Bitter gourd), Vaangi (Brinjal), Tindora/Tendli, Cluster beans, Drumstick",
        "fruits": "Coconut, Cashew, Mango (Alphonso), Banana, Papaya",
        "oils": "Coconut oil, Sesame oil, Groundnut oil",
        "spices": "Kokum (Garcinia), Malvani masala, Turmeric, Ginger, Garlic",
        "dairy": "Buffalo milk, Ghee, Dahi (thick)",
    },
    "West India - Inland (Gujarat, Rajasthan, Maharashtra Deccan)": {
        "cereals": "Bajra (primary), Jowar, Wheat, Rice (limited), Maize",
        "pulses": "Moong, Chana, Toor, Moth beans (Matki), Val, Urad",
        "vegetables": "Ringna (Brinjal), Tindora, Dudhi, Valor papdi, Methi, Batata, Ker-Sangri (Rajasthan)",
        "fruits": "Ber (Ziziphus/Jujube), Pomegranate, Chiku (Sapodilla), Guava, limited mango",
        "oils": "Groundnut oil (primary), Sesame, Mustard",
        "spices": "Cumin, Coriander, Fennel, Fenugreek, Turmeric, Asafoetida",
        "dairy": "Buffalo milk, Lassi, Chaas (Buttermilk), Ghee (generously used)",
    },
    "North India - Plains (Punjab, Haryana, UP, Bihar, Delhi)": {
        "cereals": "Wheat (primary), Bajra, Maize, Rice (UP/Bihar)",
        "pulses": "Arhar/Toor dal, Chana dal, Rajma, Masoor, Urad, Moong",
        "vegetables": "Mustard greens (Sarson — winter), Spinach (Palak), Bathua (Chenopodium), Methi, Makkai (Corn), Potato, Cauliflower, Peas, Turnip",
        "fruits": "Mango (Langra, Dasheri), Guava, Jamun, Ber, Lychee (seasonal), Citrus",
        "oils": "Mustard oil (primary in UP/Bihar/Punjab), Refined oil",
        "spices": "Cumin, Coriander, Turmeric, Garam masala, Ginger, Garlic, Fenugreek",
        "dairy": "Milk, Dahi (Thick curd), Lassi, Ghee (generous), Makhan (White butter)",
    },
    "East India (West Bengal, Odisha, Jharkhand, Chhattisgarh)": {
        "cereals": "Rice (primary — Gobindobhog, Sitabog, Sona Masuri varieties), Small amounts Wheat",
        "pulses": "Moong dal (primary), Masoor dal, Toor, Chana, various lentils",
        "vegetables": "Pointed gourd (Potol/Parval), Pumpkin (Kumro), Shim (Flat beans), Jhinge (Ridge gourd), Neem leaves, Bitter gourd (Karela), Mustard greens",
        "fruits": "Mango (Himsagar, Fazli), Guava, Litchi, Jackfruit, Banana, Coconut (coastal Odisha)",
        "oils": "Mustard oil (primary for Bengal/Odisha cooking)",
        "spices": "Panch Phoron (5-spice blend), Mustard seeds, Turmeric, Ginger, Neem leaves",
        "dairy": "Milk, Dahi (thick), Mishti Doi (sweetened), Ghee",
    },
    "Northeast India (Assam, Manipur, Meghalaya, Tripura, Nagaland)": {
        "cereals": "Rice (multiple varieties including black rice, glutinous varieties), Maize",
        "pulses": "Black-eyed peas, Moong, Masoor, Limited lentil variety",
        "vegetables": "Bamboo shoots (Bash gaj/Khorisa — fermented), Water spinach (Kochu shak), Colocasia, Bitter melon, Wild greens",
        "fruits": "Banana, Pineapple, Papaya, Jackfruit, Citrus (Khasi mandarin), Plum",
        "oils": "Mustard oil, Sesame oil, Limited coconut",
        "spices": "Bhut jolokia (ghost pepper — use cautiously), Ginger, Garlic, Turmeric",
        "dairy": "Limited dairy; fish (local river fish) is the primary protein source",
    },
}


def get_geo_zone(state: str, district: str) -> str:
    """Map state/district to geo-zone for food lookup fallback."""
    state_lower = state.lower()
    district_lower = district.lower()

    kerala_coastal = ["thiruvananthapuram", "kollam", "alappuzha", "ernakulam", "thrissur", "malappuram", "kozhikode", "kannur", "kasaragod"]
    if "kerala" in state_lower:
        return "South India - Coastal (Kerala, Konkan, Tamil Nadu Coast)"

    if any(s in state_lower for s in ["tamil", "andhra", "telangana"]):
        coastal_districts = ["chennai", "tiruvallur", "kanchipuram", "villupuram", "cuddalore", "nagapattinam", "visakhapatnam", "krishna", "guntur"]
        if any(d in district_lower for d in coastal_districts):
            return "South India - Coastal (Kerala, Konkan, Tamil Nadu Coast)"
        return "South India - Inland (Karnataka Deccan, Tamil Nadu Plains, Telangana)"

    if "karnataka" in state_lower:
        coastal = ["dakshina kannada", "udupi", "uttara kannada"]
        if any(d in district_lower for d in coastal):
            return "South India - Coastal (Kerala, Konkan, Tamil Nadu Coast)"
        return "South India - Inland (Karnataka Deccan, Tamil Nadu Plains, Telangana)"

    if any(s in state_lower for s in ["goa", "maharashtra"]):
        coastal_maha = ["mumbai", "thane", "raigad", "ratnagiri", "sindhudurg", "palghar", "north goa", "south goa"]
        if any(d in district_lower for d in coastal_maha) or "goa" in state_lower:
            return "West India - Coastal (Maharashtra Coast, Goa, Gujarat Coast)"
        return "West India - Inland (Gujarat, Rajasthan, Maharashtra Deccan)"

    if "gujarat" in state_lower:
        coastal_guj = ["surat", "bharuch", "anand", "kheda", "navsari", "valsad", "junagadh", "amreli"]
        if any(d in district_lower for d in coastal_guj):
            return "West India - Coastal (Maharashtra Coast, Goa, Gujarat Coast)"
        return "West India - Inland (Gujarat, Rajasthan, Maharashtra Deccan)"

    if "rajasthan" in state_lower:
        return "West India - Inland (Gujarat, Rajasthan, Maharashtra Deccan)"

    if any(s in state_lower for s in ["punjab", "haryana", "uttar pradesh", "bihar", "delhi", "himachal", "uttarakhand", "jammu"]):
        return "North India - Plains (Punjab, Haryana, UP, Bihar, Delhi)"

    if any(s in state_lower for s in ["west bengal", "odisha", "jharkhand", "chhattisgarh"]):
        return "East India (West Bengal, Odisha, Jharkhand, Chhattisgarh)"

    if any(s in state_lower for s in ["assam", "manipur", "meghalaya", "tripura", "nagaland", "mizoram", "arunachal", "sikkim"]):
        return "Northeast India (Assam, Manipur, Meghalaya, Tripura, Nagaland)"

    return "South India - Inland (Karnataka Deccan, Tamil Nadu Plains, Telangana)"


def load_district_food_profile(district_food_excel_path: str, state: str, district: str, desha_class: str) -> dict:
    """Load district-specific food profile from Excel. Falls back to geo-zone defaults."""
    profile = {}

    # Try Excel first
    if os.path.exists(district_food_excel_path):
        try:
            df = pd.read_excel(district_food_excel_path, sheet_name="01_District_Food_Profile")
            df.columns = df.columns.str.strip()
            match = df[(df["State"].str.lower() == state.lower()) &
                       (df["District"].str.lower() == district.lower())]
            if not match.empty:
                row = match.iloc[0]
                profile = {
                    "source": "District-Specific Data",
                    "district": district,
                    "state": state,
                    "desha": desha_class,
                    "cereals": str(row.get("Cereals_Available", "")),
                    "pulses": str(row.get("Pulses_Available", "")),
                    "vegetables": str(row.get("Vegetables_Available", "")),
                    "fruits": str(row.get("Fruits_Available", "")),
                    "oils": str(row.get("Oils_Available", "")),
                    "spices": str(row.get("Spices_Available", "")),
                    "dairy": str(row.get("Dairy_Available", "")),
                    "special_items": str(row.get("Special_Local_Foods", "")),
                    "geo_zone": str(row.get("Geo_Zone", "")),
                    "notes": str(row.get("Notes", "")),
                }
                return profile
        except Exception:
            pass

    # Fallback to geo-zone
    geo_zone = get_geo_zone(state, district)
    zone_foods = GEO_ZONE_STABLE_FOODS.get(geo_zone, {})
    profile = {
        "source": f"Geo-Zone Default ({geo_zone})",
        "district": district,
        "state": state,
        "desha": desha_class,
        "cereals": zone_foods.get("cereals", "Data not available"),
        "pulses": zone_foods.get("pulses", "Data not available"),
        "vegetables": zone_foods.get("vegetables", "Data not available"),
        "fruits": zone_foods.get("fruits", "Data not available"),
        "oils": zone_foods.get("oils", "Data not available"),
        "spices": zone_foods.get("spices", "Data not available"),
        "dairy": zone_foods.get("dairy", "Data not available"),
        "special_items": "",
        "geo_zone": geo_zone,
        "notes": "District-specific data not available; geo-zone average shown.",
    }
    return profile


def get_combined_pathya_apathya(state: str, district: str, desha_class: str,
                                 rutu: str, condition: str,
                                 district_food_excel_path: str = "") -> dict:
    """
    Return comprehensive Pathya-Apathya combining:
    1. District food profile (what is locally available)
    2. Rutu-specific guidance
    3. Condition-specific guidance
    4. Desha modifier
    """
    food_profile = load_district_food_profile(district_food_excel_path, state, district, desha_class)
    rutu_guide = RUTU_PATHYA_APATHYA.get(rutu, {})
    condition_guide = CONDITION_PATHYA.get(condition, {}) if condition and condition != "Not Provided" else {}
    root_desha = desha_class.split("-")[0].upper() if desha_class else "SADHARANA"
    desha_modifier = DESHA_FOOD_MODIFIERS.get(root_desha, DESHA_FOOD_MODIFIERS["SADHARANA"])

    return {
        "food_profile": food_profile,
        "rutu_guidance": rutu_guide,
        "condition_guidance": condition_guide,
        "desha_modifier": desha_modifier,
    }
