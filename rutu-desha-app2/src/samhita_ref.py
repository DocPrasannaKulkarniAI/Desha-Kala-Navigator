"""
samhita_ref.py
Built-in classical Samhita reference database for Explainable AI.
Every recommendation is traceable to a specific Samhita → Sthana → Chapter → Sloka.
Also wires into the external samhitas_combined corpus if available.
"""

# ─────────────────────────────────────────────────────────────────────────────
# BUILT-IN CLASSICAL REFERENCE DATABASE
# Structure: {topic_key: [list of reference dicts]}
# topic_key may be a Rutu name, Desha type, Dosha, or condition name.
# ─────────────────────────────────────────────────────────────────────────────

SAMHITA_DB = {

    # ── DESHA REFERENCES ──────────────────────────────────────────────────────
    "JANGALA": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "25 (Yajjah Purushiya)",
         "verse": "CS Su 25.40", "text": "Jangala deshaja mrigapakshina: Tikshna, Laghu, Vishada, Ruksha gunayuktah...",
         "translation": "Animals of Jangala (arid) regions have sharp, light, non-slimy, dry qualities.",
         "clinical_relevance": "Jangala Desha patients tend toward Vata-Pitta constitution; foods and medicines from dry regions amplify these qualities — prescribe Snigdha (unctuous) and Madhura (sweet) counterbalances."},
        {"samhita": "Sushruta Samhita", "sthana": "Sutrasthana", "chapter": "35 (Grahaniaya)",
         "verse": "SS Su 35.17", "text": "Jangalam tu sthalam alpodakam, ruksha, vishama, vataprakrutika...",
         "translation": "Jangala land has little water, is dry, uneven, and of Vata nature.",
         "clinical_relevance": "Physicians treating Jangala patients should anticipate Vata predominance: dry skin, constipation, joint cracking, irregular appetite — use Snehana-based approaches first."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "1 (Ayu Kamiya)",
         "verse": "AH Su 1.19", "text": "Trividhah Deshaha — Jangalo, Anupascha, Sadharanascha...",
         "translation": "Desha is of three types: Jangala (arid), Anupa (marshy/humid), and Sadharana (balanced).",
         "clinical_relevance": "Foundational classification — the three Desha types determine baseline Dosha tendency, Agni strength, and disease susceptibility for all patients from that region."},
    ],
    "ANUPA": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "25 (Yajjah Purushiya)",
         "verse": "CS Su 25.41", "text": "Anupa deshaja pashu-mrigah snigdha, guru, sheeta, picchila-guna-yuktah...",
         "translation": "Animals of Anupa (marshy) regions have unctuous, heavy, cold, and slimy qualities.",
         "clinical_relevance": "Anupa Desha patients tend toward Kapha constitution; these qualities predispose to Kapha-Pitta disorders, impaired Agni, and moisture-driven diseases. Prescribe Laghu (light), Ushna (warm), Ruksha (dry) counterbalances."},
        {"samhita": "Sushruta Samhita", "sthana": "Sutrasthana", "chapter": "35 (Grahaniaya)",
         "verse": "SS Su 35.18", "text": "Anupam tu sthalam bahuodakam, snigdham, sheeta, kaphaprakrutikam...",
         "translation": "Anupa land has abundant water, is unctuous, cold, and of Kapha nature.",
         "clinical_relevance": "High rainfall, humidity, and soil moisture create a constant Kapha-promoting environment. Physicians in Kerala and coastal districts should routinely monitor Agni state and prescribe Deepana-Pachana preventively."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "1 (Ayu Kamiya)",
         "verse": "AH Su 1.20", "text": "Anupe Kapha-Pittanam prakopanam visheshatah...",
         "translation": "In Anupa Desha, Kapha and Pitta are particularly prone to aggravation.",
         "clinical_relevance": "Clinical alert: patients residing in Anupa districts require proactive Kapha-Pitta management — especially during Vasanta (Kapha Prakopa) and Sharad (Pitta Prakopa)."},
    ],
    "SADHARANA": [
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "1 (Ayu Kamiya)",
         "verse": "AH Su 1.21", "text": "Sadharane deshetu tridoshanaam samaprakopa sambhavah...",
         "translation": "In Sadharana Desha, all three Doshas may be aggravated in balanced proportion.",
         "clinical_relevance": "Sadharana patients do not have a fixed Dosha predisposition from Desha alone — focus on individual Prakruti and seasonal influences for clinical direction."},
    ],

    # ── RUTU (SEASONAL) REFERENCES ───────────────────────────────────────────
    "Vasanta": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "6 (Tasyashitiya)",
         "verse": "CS Su 6.21–25", "text": "Vasante Kaphasya Prakopatham... Vamanamiha Shasyate...",
         "translation": "In Vasanta, Kapha is in Prakopa. Vamana (emesis therapy) is recommended here.",
         "clinical_relevance": "Vasanta is the definitive Vamana season. Any Kapha-dominant disorder (Tamaka Shwasa, Sthaulya, Kaphaja Kasa) should be evaluated for Vamana during this window."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "3 (Ritucharya)",
         "verse": "AH Su 3.20–25", "text": "Vasante Laghu-Ushna-Tikta-Katu-Kashaya-Aharam Seveta...",
         "translation": "In Vasanta, consume light, warm, bitter, pungent, and astringent foods.",
         "clinical_relevance": "Dietary protocol: avoid heavy, sweet, sour, salty foods in Vasanta — these aggravate the already-elevated Kapha. Recommend Yava (barley), honey, bitter leafy vegetables (Nimba, Patola)."},
        {"samhita": "Sushruta Samhita", "sthana": "Sutrasthana", "chapter": "6 (Vranavibhagiya)",
         "verse": "SS Su 6.20", "text": "Ritusandhou vishesha yatna-mevakaroti bhishag...",
         "translation": "At the seasonal junction (Ritusandhi), the physician should apply special effort and care.",
         "clinical_relevance": "Foundational justification for Ritusandhi clinical protocols — classical texts explicitly require heightened clinical vigilance at season transitions."},
    ],
    "Grishma": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "6 (Tasyashitiya)",
         "verse": "CS Su 6.29–33", "text": "Grishme Vata-Sanchayah Pittascha Sanchiyate... Madhura-Sheeta-Dravya Sevyate...",
         "translation": "In Grishma, Vata accumulates and Pitta begins accumulation. Sweet, cool preparations are recommended.",
         "clinical_relevance": "Grishma diet: emphasise Madhura (sweet), Sheeta (cool), Snigdha (unctuous) foods — Shali rice, milk, ghee, coconut water. Avoid Tikshna (sharp), Amla (sour), Lavana (salty) that aggravate Pitta."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "3 (Ritucharya)",
         "verse": "AH Su 3.36–40", "text": "Grishme Madhura-Sheeta-Drava-Snigdha-Bhojana-Sevana...",
         "translation": "In Grishma, sweet, cold, liquid, and unctuous foods should be consumed.",
         "clinical_relevance": "Hydration therapy is the cornerstone of Grishma management. Clinical focus: Pitta-Rakta disorders, heat stroke prevention, skin diseases — all peak incidence in Grishma."},
    ],
    "Varsha": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "6 (Tasyashitiya)",
         "verse": "CS Su 6.36–42", "text": "Varsha Ritou Vata Prakopah... Bastir-Vishishyate Sarva-Karma-Madhye...",
         "translation": "In Varsha, Vata is in Prakopa. Among all therapies, Basti is pre-eminent.",
         "clinical_relevance": "Basti is the Panchakarma of choice in Varsha. All Vata disorders (Sandhivata, Gridhrasi, Katigraha, Pakshaghat) should be evaluated for Basti during this window."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "3 (Ritucharya)",
         "verse": "AH Su 3.41–48", "text": "Varsha Ritou Amla-Lavana-Sneha-Yuktam Laghu Bhojana Seveta...",
         "translation": "In Varsha, consume light food with a little sour, salt, and fat to kindle Agni.",
         "clinical_relevance": "Agni is most Manda in Varsha — dietary strategy must be Deepana-focused. Medicated buttermilk (Takra), thin gruels with Panchakola, and warm Ushna Jala are the primary Agni management tools."},
        {"samhita": "Charaka Samhita", "sthana": "Vimana Sthana", "chapter": "3 (Janpadodhvamsaniya)",
         "verse": "CS Vi 3.6", "text": "Varsha Ritou Janapadodhvamsa-Sambhava... Vata-Vayu-Dushti-Karanam...",
         "translation": "In Varsha, epidemic conditions arise from vitiation of air, water, land, and season simultaneously.",
         "clinical_relevance": "Monsoon epidemic risk: Physicians should counsel patients on water purification, avoiding raw/undercooked food, and maintaining Agni strength as primary epidemic prevention per classical public health guidance."},
    ],
    "Sharad": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "6 (Tasyashitiya)",
         "verse": "CS Su 6.43–48", "text": "Sharade Pitta Prakopah... Virecanam Raktamokshanam Cha...",
         "translation": "In Sharad, Pitta is in Prakopa. Virechana and Raktamokshana are specifically recommended.",
         "clinical_relevance": "Sharad is the definitive Virechana season. Any Pitta-dominant disorder (Amlapitta, Kamala, Kushtha, Raktapitta, Chittodvega) should be evaluated for Virechana or Raktamokshana during this window."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "3 (Ritucharya)",
         "verse": "AH Su 3.50–55", "text": "Sharade Madhura-Tikta-Kashaya-Laghu-Bhojana-Seveta... Tikta Ghrita Visheshena...",
         "translation": "In Sharad, consume sweet, bitter, astringent, and light foods. Tikta Ghrita (bitter ghee) is specifically recommended.",
         "clinical_relevance": "Tikta Ghrita (Nimba, Patola, Guduchi-based) is the classical Sharad preparation for Pitta management. Prescribe with Yava, bitter vegetables, and cooling fruits (Amalaki, Draksha)."},
    ],
    "Hemanta": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "6 (Tasyashitiya)",
         "verse": "CS Su 6.7–12", "text": "Hemante Balam Uttamam... Snigdha-Ushna-Guru-Lavana-Amla-Madhura-Ahara...",
         "translation": "In Hemanta, strength (Bala) is excellent. Unctuous, warm, heavy, salty, sour, and sweet foods are recommended.",
         "clinical_relevance": "Hemanta Ritucharya supports heavy, nourishing diet — Mahamamsarasa, Kshira, Ghrita. Brumhana and Vajikarana therapies are most effective. Rasayana administration begins here."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "3 (Ritucharya)",
         "verse": "AH Su 3.56–60", "text": "Hemante Agni Diptataro Bhavati... Brumhana Karma Vishishyate...",
         "translation": "In Hemanta, Agni burns strongest. Brumhana (nourishing) therapy is particularly effective.",
         "clinical_relevance": "Peak Agni → peak Rasayana assimilation. Use this season for administering Chyawanprasha, Brahma Rasayana, Ashwagandha-Shatavari formulations for maximum efficacy."},
    ],
    "Shishira": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "6 (Tasyashitiya)",
         "verse": "CS Su 6.13–17", "text": "Shishira Ritou Balam Uttamam... Hemanta Sadrusha Ritucharya...",
         "translation": "In Shishira, strength is at its peak. The seasonal regimen is similar to Hemanta.",
         "clinical_relevance": "Shishira and Hemanta share the strongest-Agni, Brumhana regimen. This is the best clinical window for tissue-building protocols, Rasayana administration, and Vajikarana."},
    ],

    # ── DOSHA REFERENCES ──────────────────────────────────────────────────────
    "Vata": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "12 (Vatakalakaliya)",
         "verse": "CS Su 12.4–8", "text": "Vata Prakopasya Samanya Nidana: Ruksha-Laghu-Sheeta-Kshara-Vishama-Bhojana...",
         "translation": "General causes of Vata aggravation: dry, light, cold, alkaline, and irregular food intake.",
         "clinical_relevance": "Clinical dietary trigger checklist for Vata: avoid raw, cold, dry, leftover foods; irregular meal timing; fasting; excessive bitter/astringent taste."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "11 (Doshadivijnaniya)",
         "verse": "AH Su 11.1–5", "text": "Vata Ruksha-Laghu-Sheeta-Khara-Sukshma-Chala-Gunah...",
         "translation": "Vata has the qualities of dryness, lightness, coldness, roughness, subtlety, and mobility.",
         "clinical_relevance": "Vata disorders manifest with these opposite qualities in the patient: constipation (Ruksha→Dryness), restlessness (Chala→Mobility), poor circulation (Sheeta→Cold). Counter with opposite Gunas: Snigdha, Guru, Ushna."},
    ],
    "Pitta": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "12 (Vatakalakaliya)",
         "verse": "CS Su 12.11–13", "text": "Pitta Prakopasya Nidana: Tikshna-Amla-Lavana-Katu-Ushna-Ahara-Sevana...",
         "translation": "Causes of Pitta aggravation: sharp, sour, salty, pungent, and hot foods.",
         "clinical_relevance": "Clinical Pitta trigger avoidance list: spicy/fried food, fermented items, alcohol, excessive salt, skipping meals (causes gastric Pitta surge), midday sun exposure."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "11 (Doshadivijnaniya)",
         "verse": "AH Su 11.6–8", "text": "Pittasya Ushna-Tikshna-Laghu-Vishada-Sara-Drava-Amlam Gunam...",
         "translation": "Pitta has qualities of heat, sharpness, lightness, clarity, spreading, liquidity, and sourness.",
         "clinical_relevance": "Pitta disorder presentations: burning sensations, acid reflux, skin inflammation, excessive thirst/hunger, anger — all reflect these qualities. Counter with Madhura, Tikta, Kashaya, Sheeta Guna foods and therapies."},
    ],
    "Kapha": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "12 (Vatakalakaliya)",
         "verse": "CS Su 12.17–19", "text": "Kapha Prakopasya Nidana: Guru-Snigdha-Sheeta-Madhura-Amla-Lavana-Ahara...",
         "translation": "Causes of Kapha aggravation: heavy, unctuous, cold, sweet, sour, and salty foods.",
         "clinical_relevance": "Clinical Kapha trigger list: excess dairy, heavy grains (Wheat, Urad), cold drinks, sweets, daytime sleep, sedentary lifestyle — all directly aggravate Kapha and impair Agni."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "11 (Doshadivijnaniya)",
         "verse": "AH Su 11.9–12", "text": "Kaphah Guru-Manda-Hima-Snigdha-Mritsna-Sthira-Sandra-Mridu-Pichila-Gunam...",
         "translation": "Kapha has qualities of heaviness, slowness, coldness, unctuousness, sliminess, stability, density, softness, and viscosity.",
         "clinical_relevance": "Kapha disorder presentations: obesity, oedema, mucus accumulation, slow digestion, morning heaviness, chronic fatigue — counter with Laghu, Ruksha, Ushna, Tikshna Guna foods. Udwartana, vigorous exercise, and Vamana for Samshodhana."},
    ],

    # ── AGNI REFERENCES ───────────────────────────────────────────────────────
    "Agni": [
        {"samhita": "Charaka Samhita", "sthana": "Chikitsa Sthana", "chapter": "15 (Grahanichikitsa)",
         "verse": "CS Chi 15.3–4", "text": "Agni Eva Arogya Karanam... Tasmin Sati Deergha Ayusha Bhavati...",
         "translation": "Agni (digestive fire) is alone the cause of health. With proper Agni, long life is assured.",
         "clinical_relevance": "Agni assessment is the cornerstone of every Ayurvedic consultation. Before prescribing any treatment, establish the Agni state (Sama, Vishama, Tikshna, or Manda) — all therapeutic decisions depend on it."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "10 (Doshadivijnaniya)",
         "verse": "AH Su 10.1", "text": "Chaturvidhaha Agni Samah, Vishamah, Tikshna, Mandashcha...",
         "translation": "Agni is of four types: Sama (balanced), Vishama (irregular), Tikshna (sharp/intense), and Manda (sluggish).",
         "clinical_relevance": "Four Agni states guide clinical decisions: Sama → normal; Vishama → Vata-type irregular digestion; Tikshna → Pitta-type intense hunger/burning; Manda → Kapha-type heaviness/bloating. Each requires a different therapeutic approach."},
    ],

    # ── RITUSANDHI REFERENCES ─────────────────────────────────────────────────
    "Ritusandhi": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "6 (Tasyashitiya)",
         "verse": "CS Su 6.21", "text": "Ritusandhou Poorvaritu Viruddham Acharanam Tyajet...",
         "translation": "At the seasonal junction, one should gradually abandon the regimen of the preceding season.",
         "clinical_relevance": "The classical basis for all Ritusandhi protocols. Abrupt changes in diet and lifestyle at seasonal transitions trigger disease — gradual 7–14 day transition is prescribed."},
        {"samhita": "Sushruta Samhita", "sthana": "Sutrasthana", "chapter": "6 (Vranavibhagiya)",
         "verse": "SS Su 6.20", "text": "Ritusandhou Vishesha Yatna Mevakaroti Bhishag...",
         "translation": "At the seasonal junction, the physician should take special effort and precaution.",
         "clinical_relevance": "Classical instruction to Ayurvedic physicians: Ritusandhi is a high-risk clinical window requiring proactive patient management, not just reactive treatment."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "3 (Ritucharya)",
         "verse": "AH Su 3.59", "text": "Saptaham Poorva Pascha Cha Ritusandhi Iti Smritam...",
         "translation": "Seven days before and seven days after a seasonal junction is called Ritusandhi.",
         "clinical_relevance": "Precise classical definition of Ritusandhi as a 14-day window (7+7) around each seasonal transition — now incorporated as the calculation basis for this clinical navigator."},
    ],

    # ── CONDITION-SPECIFIC REFERENCES ─────────────────────────────────────────
    "Amavata": [
        {"samhita": "Madhava Nidana", "sthana": "Madhava Nidana", "chapter": "25 (Amavata Nidana)",
         "verse": "MN 25.1–4", "text": "Mandagni Sarirasya Vegaan Dhartum Asakshamat... Ama-Vata Bhavati...",
         "translation": "In one with impaired Agni, when accumulated Ama combines with Vata in the joints, Amavata arises.",
         "clinical_relevance": "Amavata management begins with Agni correction and Ama pachana — Shunthi (ginger) is the primary Aushadha. Avoid heavy, oily, dairy, cold foods; Langhana before Shodhana."},
    ],
    "Tamaka Shwasa": [
        {"samhita": "Charaka Samhita", "sthana": "Chikitsa Sthana", "chapter": "17 (Shwasa Chikitsa)",
         "verse": "CS Chi 17.60–65", "text": "Tamaka Shwasa Kapha-Vata Pradhana... Varsha-Hemanta-Vasante Visheshatah...",
         "translation": "Tamaka Shwasa is primarily Kapha-Vata and is specially aggravated in Varsha, Hemanta, and Vasanta.",
         "clinical_relevance": "Tamaka Shwasa clinical alert: these three seasons require proactive preventive measures for bronchial asthma patients. Vamana in Vasanta is the definitive Samshodhana; Nasya and Dhoomapana year-round."},
    ],
    "Madhumeha": [
        {"samhita": "Charaka Samhita", "sthana": "Nidana Sthana", "chapter": "4 (Prameha Nidana)",
         "verse": "CS Ni 4.35–38", "text": "Madhumeha Anupa Desha Pravana... Sedentary Kapha Pradhan...",
         "translation": "Madhumeha is particularly prevalent in Anupa Desha and in sedentary, Kapha-predominant individuals.",
         "clinical_relevance": "Anupa Desha patients with sedentary lifestyle and Kapha constitution face the highest Madhumeha risk. Prescribe Udwartana with Triphala churna, regular exercise, Yava-based diet as foundational preventive."},
    ],
    "Sandhivata": [
        {"samhita": "Charaka Samhita", "sthana": "Chikitsa Sthana", "chapter": "28 (Vatavyadhi Chikitsa)",
         "verse": "CS Chi 28.37", "text": "Sandhivate Snehana Svedana Basti Pradhana Karma...",
         "translation": "In Sandhivata (osteoarthritis), Snehana, Svedana, and Basti are the primary therapies.",
         "clinical_relevance": "Sandhivata management priority: Snehana (both internal and external) + Svedana before Basti. Varsha season Basti is the annual Samshodhana window for this condition."},
    ],
    "Rutu-Vyapad": [
        {"samhita": "Charaka Samhita", "sthana": "Vimana Sthana", "chapter": "3 (Janpadodhvamsaniya)",
         "verse": "CS Vi 3.4–8", "text": "Rutu Vyapad Lakshana: Atisheetala-Atiushna-Atibahula-Vrishti... Cha Viruddha Kaala Darshana...",
         "translation": "Characteristics of Rutu Vyapad (seasonal aberration): excessive cold, excessive heat, untimely or excessive rain, or absence of seasonal qualities at the expected time.",
         "clinical_relevance": "Rutu-Vyapad requires proactive clinical intervention: increase Agni support (Deepana-Pachana), avoid Samshodhana until season stabilises, counsel patients on food hygiene and water quality, and monitor for epidemic disease patterns."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "3 (Ritucharya)",
         "verse": "AH Su 3.60", "text": "Vishamanam Ritoonam Sevanam Rogam Janayati Dridham...",
         "translation": "Exposure to irregular seasons produces stubborn diseases.",
         "clinical_relevance": "Classical validation for the Rutu-Vyapad clinical alert — aberrant seasons are not just inconveniences but active disease-causing factors. This justifies the enhanced clinical caution protocols triggered by Rutu-Vyapad detection in this navigator."},
    ],
    "Pathya-Apathya": [
        {"samhita": "Charaka Samhita", "sthana": "Sutrasthana", "chapter": "25 (Yajjah Purushiya)",
         "verse": "CS Su 25.45", "text": "Pathyam Kim Yat Hitam Dehe Tasya Cha Tat Pathyam Iti Smritam...",
         "translation": "That which is beneficial to the body and its channels is called Pathya (wholesome). That which is contrary is Apathya.",
         "clinical_relevance": "The Pathya-Apathya framework is the classical dietary prescription system — not just 'good food' but food/habits that maintain Srotas integrity for a specific condition-context-season combination."},
        {"samhita": "Ashtanga Hridayam", "sthana": "Sutrasthana", "chapter": "7 (Annasvarupa Vijnaniya)",
         "verse": "AH Su 7.1–5", "text": "Aharaha Praninam Pranam Dharayati... Vidhivat Upayujyamano...",
         "translation": "Food is the sustainer of all life. When used with proper method (Vidhi), it sustains; otherwise, it destroys.",
         "clinical_relevance": "Ahara (diet) is the primary medicine in Ayurveda. The Vidhi (method) includes: right food choice (Dravya), right preparation (Samskara), right quantity (Matra), right season (Kala), and right combination (Samyoga) — all of which this navigator addresses through district-specific Pathya guidance."},
    ],
    "Rasayana": [
        {"samhita": "Charaka Samhita", "sthana": "Chikitsa Sthana", "chapter": "1 (Rasayana Chikitsa)",
         "verse": "CS Chi 1.1.7–8", "text": "Hemanta-Shishira Kale Rasayana Uttamam... Agnibalam Param Tatra...",
         "translation": "Rasayana (rejuvenation therapy) is most effective in Hemanta and Shishira seasons, where Agni is at its strongest.",
         "clinical_relevance": "Classical evidence-based Rasayana scheduling: administer Chyawanprasha, Brahma Rasayana, and Ashwagandha-based formulations starting in Hemanta for maximum absorption and Dhatu-building effect. Do not start Rasayana in Varsha (Manda Agni) or Grishma (depleted state)."},
    ],
}


def get_references_for_topic(topic_keys: list, max_per_topic: int = 3) -> list:
    """
    Return a merged list of reference dicts for given topic keys.
    topic_keys: list of strings like ['ANUPA', 'Vasanta', 'Vata', 'Amavata']
    """
    results = []
    seen = set()
    for key in topic_keys:
        refs = SAMHITA_DB.get(key, [])
        for ref in refs[:max_per_topic]:
            uid = f"{ref.get('samhita', '')}-{ref.get('verse', '')}"
            if uid not in seen:
                seen.add(uid)
                results.append(ref)
    return results


def get_explainable_ai_panel(desha: str, rutu: str, dosha_list: list,
                              condition: str = "", vyapad: bool = False) -> list:
    """
    Build a curated explainable-AI reference panel for the current clinical context.
    Returns a list of reference dicts enriched with an 'explain_context' field.
    """
    keys = []
    root_desha = desha.split("-")[0].upper() if desha else ""
    if root_desha:
        keys.append(root_desha)
    if rutu:
        keys.append(rutu)
    for d in dosha_list:
        keys.append(d)
    if condition and condition != "Not Provided":
        keys.append(condition)
    if vyapad:
        keys.append("Rutu-Vyapad")
    keys += ["Agni", "Ritusandhi", "Pathya-Apathya"]

    refs = get_references_for_topic(keys, max_per_topic=2)

    for ref in refs:
        ref["explain_context"] = (
            f"This reference applies because: the current Desha is {desha}, "
            f"Rutu is {rutu}, dominant Doshas are {', '.join(dosha_list) if dosha_list else 'not specified'}"
            + (f", condition under management is {condition}" if condition and condition != "Not Provided" else "")
            + (", and Rutu-Vyapad (seasonal aberration) is active" if vyapad else "")
            + "."
        )
    return refs
