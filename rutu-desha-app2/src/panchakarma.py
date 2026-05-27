"""
panchakarma.py
Panchakarma Timing Advisor: maps current Rutu to optimal, beneficial,
use-with-caution, and contraindicated Karma; provides Ritusandhi countdown
with preparatory protocols and contemporary scientific insights.
"""
import datetime

RUTU_START_DATES = {
    "Shishira": (1, 14),
    "Vasanta":  (3, 14),
    "Grishma":  (5, 14),
    "Varsha":   (7, 14),
    "Sharad":   (9, 14),
    "Hemanta":  (11, 14),
}
RUTU_SEQUENCE = ["Shishira", "Vasanta", "Grishma", "Varsha", "Sharad", "Hemanta"]

PANCHAKARMA_RUTU_MAP = {
    "Vasanta": {
        "optimal": [
            {"karma": "Vamana", "full_name": "Vamana (Therapeutic Emesis)",
             "dosha_target": "Kapha Prakopa",
             "classical_basis": "Charaka Samhita — Sutrasthana 16.17: 'Vasante Kapha Prakopah' — Kapha peaks in Vasanta making Vamana the gold-standard Samshodhana.",
             "poorvakarma": "7–10 days internal Snehapana (Panchatikta Ghrita or plain Ghrita) + 3 days Bashpa/Nadi Svedana.",
             "pradhana_karma": "Madanaphala + Yashti + Honey emetic. Target 4–8 Vega. Single morning session.",
             "pashchat_karma": "Samsarjana Krama (7-day graduated diet); strict rest for 3 days post-emesis.",
             "duration_total": "14–17 days",
             "contraindications": "Avoid in Rutu-Vyapad; ensure Agni adequate (5-day Deepana-Pachana mandatory first)."},
            {"karma": "Nasya", "full_name": "Karma Nasya (Nasal Administration)",
             "dosha_target": "Kapha in Urdhvajatrugata",
             "classical_basis": "Ashtanga Hridayam — Sutrasthana 20.1: Nasya specifically indicated for Urdhvajatrugata disorders; Vasanta Kapha aggravates Shiro-Kantha region.",
             "poorvakarma": "3–5 days local Abhyanga (head/neck) + Nadi Svedana.",
             "pradhana_karma": "Vacha taila or Anu taila — 8 drops per nostril; 7-day Karma Nasya.",
             "pashchat_karma": "Avoid cold drinks and cold/wind exposure for 1 week.",
             "duration_total": "10–12 days",
             "contraindications": "Allow 3-day gap after Vamana; avoid during active fever or nasal congestion."},
        ],
        "beneficial": [
            {"karma": "Mridu Virechana", "full_name": "Mridu Virechana (Mild Purgation)",
             "dosha_target": "Residual Pitta from Shishira",
             "classical_basis": "Charaka Samhita — Kalpasthana 1.4: Mild Virechana in Vasanta for residual Pitta when Vamana is not feasible.",
             "poorvakarma": "3–5 days Snehapana",
             "pradhana_karma": "Trivrit leha or Eranda taila — mild dose; 1 session.",
             "duration_total": "8–10 days",
             "contraindications": "Not first choice; use only if Kapha involvement is minimal."},
        ],
        "use_with_caution": [],
        "avoid": [
            {"karma": "Basti", "reason": "Vata is in Prashama in Vasanta — Basti is not the primary therapy; use only for specific Vata co-vitiation under careful evaluation."},
            {"karma": "Raktamokshana", "reason": "Not indicated in Vasanta; blood properties are still in winter-Kapha phase."},
        ],
        "ritusandhi_note": "Vasanta–Grishma Ritusandhi (last 7 days of Vasanta): Complete all Vamana courses BEFORE Ritusandhi begins. Start Pitta-pacifying regimen 5 days before transition. Shift from Udwartana to light oil massage.",
        "agni_guidance": "Agni is characteristically Manda (sluggish) in Vasanta due to Kapha load. MANDATORY: 5–7 days Deepana-Pachana with Trikatu + warm water or Chitrakadi Vati before ANY Samshodhana.",
        "rasayana_window": "Post-Vamana Vasanta is the OPTIMAL window for Chyawanprasha Rasayana — purified Kapha channels maximise assimilation of rejuvenating formulas.",
        "scientific_insight": "Spring histamine surges parallel Kapha Prakopa — mast cell degranulation increases at vernal equinox. Vamana stimulates the vagus nerve (dorsal vagal complex activation), resetting hypothalamic-pituitary-adrenal (HPA) axis overload accumulated through winter. Research shows vagal stimulation reduces systemic inflammatory markers (IL-6, TNF-α). Seasonal allergy peaks in Vasanta align precisely with Kapha Prakopa theory.",
    },
    "Grishma": {
        "optimal": [
            {"karma": "Virechana", "full_name": "Virechana (Therapeutic Purgation)",
             "dosha_target": "Pitta Sanchaya (early accumulation)",
             "classical_basis": "Charaka Samhita — Su 16.18 and AH Su 3.58: Virechana in early Grishma clears nascent Pitta Sanchaya before it reaches Prakopa in Sharad.",
             "poorvakarma": "5–7 days Tikta Ghrita Snehapana + 2–3 days mild Svedana (avoid excess heat exposure).",
             "pradhana_karma": "Trivrit churna or Eranda taila or Icchabhedi Rasa — titrated to constitution. 1–3 Vega.",
             "pashchat_karma": "Samsarjana Krama; cooling diet (Yava, Shali rice, buttermilk); avoid heat for 1 week.",
             "duration_total": "12–15 days",
             "contraindications": "Avoid during peak summer >38°C ambient. Perform in early Grishma only. Ensure full hydration throughout."},
            {"karma": "Raktamokshana", "full_name": "Raktamokshana (Jalauka / Sringa)",
             "dosha_target": "Pitta–Rakta Dushthi",
             "classical_basis": "Sushruta Samhita — Sutrasthana 14.25: Raktamokshana indicated when Pitta vitiates Rakta; Grishma increases blood viscosity and Pitta-Rakta accumulation.",
             "poorvakarma": "3 days Snehana; ensure patient is well hydrated pre-procedure.",
             "pradhana_karma": "Jalauka (leech) for localised conditions; Sringa for regional; Siravedha for systemic Pitta-Rakta.",
             "pashchat_karma": "Haridra + honey paste on site; cooling diet for 3 days.",
             "duration_total": "5–7 days",
             "contraindications": "Contraindicated in dehydration or anaemia (Hb < 10 g/dL); avoid in anticoagulant therapy."},
        ],
        "beneficial": [],
        "use_with_caution": [
            {"karma": "Anuvasana Basti",
             "reason": "Vata Sanchaya begins in Grishma — mild Anuvasana Basti (60–120 ml sesame oil) is permissible for specific Vata conditions; AVOID Niruha Basti during peak heat."},
        ],
        "avoid": [
            {"karma": "Vamana", "reason": "Kapha Prashama in Grishma — body is already depleted from heat; Vamana further reduces Ojas and Bala critically."},
            {"karma": "Vigorous Bashpa Svedana", "reason": "Intense sweating therapy in Grishma causes severe Pitta aggravation, dehydration, and electrolyte depletion; use only mild Nadi Svedana if required."},
        ],
        "ritusandhi_note": "Grishma–Varsha Ritusandhi (last 7 days of Grishma — MOST CRITICAL): Stop all Samshodhana. Begin Laghu Bhojana protocol. Transition to Basti preparation. Immune resilience is at its annual minimum at this junction — protect all patients.",
        "agni_guidance": "Agni is in Vishama (irregular) state due to heat stress and dehydration. Dhanyaka (coriander) + Shatapushpa water is an excellent Agni stabiliser. Never start Samshodhana without 5-day Agni stabilisation.",
        "rasayana_window": "Post-Virechana early Grishma: Amalaki Rasayana — its Pitta-cooling and Vayasthapana properties are maximally needed in the early summer window.",
        "scientific_insight": "Hepatic Phase I (CYP450) and Phase II (conjugation) detoxification are enhanced by longer daylight photoperiods in summer. Virechana aligns with this peak hepatic metabolic capacity window. Circadian clock genes (CLOCK, BMAL1) show maximal expression in early summer, supporting enhanced Samshodhana efficacy classically described for this season.",
    },
    "Varsha": {
        "optimal": [
            {"karma": "Niruha Basti", "full_name": "Niruha Basti (Decoction Enema — Vata Samshodhana)",
             "dosha_target": "Vata Prakopa (peak season)",
             "classical_basis": "Charaka Samhita — Siddhisthana 1.25: 'Bastireva Vishishyate' — Basti is supreme among all Panchakarma; gold standard for Varsha Vata Prakopa.",
             "poorvakarma": "5–7 days Abhyanga (Dhanvantara taila) + mild Nadi Svedana.",
             "pradhana_karma": "Kala Basti (16 sessions: 8 Niruha + 8 Anuvasana) or Karma Basti (30 sessions). Dashamoola Kwatha base for Niruha; Dhanvantara/Sesame taila for Anuvasana.",
             "pashchat_karma": "Manda (thin rice gruel) for 3 days; warm liquids; avoid Vata-aggravating foods for 1 week.",
             "duration_total": "16–35 days depending on Basti type",
             "contraindications": "Avoid during active diarrhoea or fever; mandatory 5-day Deepana-Pachana (Panchakola Phanta) before starting."},
            {"karma": "Anuvasana Basti", "full_name": "Anuvasana Basti (Oil Enema)",
             "dosha_target": "Vata Prakopa — Ruksha-Sheeta quality correction",
             "classical_basis": "Ashtanga Hridayam — Kalpa Sthana 4.3: Anuvasana with Dhanvantara taila counters the Ruksha and Sheeta Guna of Varsha Vata.",
             "poorvakarma": "3–5 days Abhyanga",
             "pradhana_karma": "60–120 ml Dhanvantara taila; administered on alternating days with Niruha in Kala Basti schedule.",
             "duration_total": "Integrated into Kala/Yoga Basti schedule (16–30 days)",
             "contraindications": "Avoid in Ama — check for tongue coat and low appetite before starting."},
        ],
        "beneficial": [
            {"karma": "Brumhana Nasya", "full_name": "Brumhana (Nourishing) Nasya",
             "dosha_target": "Prana and Udana Vata — Bala building",
             "classical_basis": "Charaka Samhita — Siddhisthana 9.89: Brumhana Nasya with Ashwagandha/Bala taila builds Bala during the weakened Varsha season.",
             "poorvakarma": "3 days local Abhyanga to head + Nadi Svedana",
             "pradhana_karma": "Ashwagandha taila or Bala taila — 4–6 drops per nostril; 7 days.",
             "duration_total": "10 days",
             "contraindications": "Avoid during active cold, fever, or heavy rain exposure on treatment day."},
        ],
        "use_with_caution": [
            {"karma": "Virechana",
             "reason": "May be needed for Pitta Sanchaya from Grishma but monsoon weather instability makes Anupana dosing difficult; proceed only if specifically indicated and weather is stable for 3+ days."},
        ],
        "avoid": [
            {"karma": "Vamana", "reason": "STRICTLY CONTRAINDICATED in Varsha — Kapha is in Prashama; Vamana during monsoon severely aggravates Vata and critically depletes Ojas."},
            {"karma": "Raktamokshana (Jalauka)", "reason": "Leeches harbour infection risk during monsoon. Wound healing is severely compromised in Varsha. Avoid unless absolutely necessary; use strictly sterile indoor setup only."},
            {"karma": "Intense Bashpa Svedana", "reason": "Excess sweating during high-humidity monsoon leads to severe electrolyte depletion and Pitta-Vata aggravation."},
        ],
        "ritusandhi_note": "Varsha–Sharad Ritusandhi (last 7 days of Varsha): Complete ALL Basti courses before this transition. Pitta Prakopa is imminent — switch protocol immediately to Pitta-pacifying diet (Tikta Ghrita, bitter vegetables, Madhura-Tikta balance) and begin Virechana preparation.",
        "agni_guidance": "Agni is at its most Manda (weakest) in Varsha. Classical RULE: NEVER begin Samshodhana without minimum 5-day Deepana-Pachana. Use Panchakola Phanta (Shunti, Pippali, Maricha, Chavya, Chitraka) as mandatory Agni kindler. Check tongue for coating — if coated, add 3 more days of Deepana.",
        "rasayana_window": "Post-Basti Varsha: Ashwagandha Avaleha rebuilds Vata-depleted Dhatus; Bala Taila Abhyanga as maintenance. Kushmanda Rasayana for nervous system repair.",
        "scientific_insight": "The enteric nervous system (ENS — the 'second brain') is directly accessible via Basti. Research demonstrates medicated enemas modulate gut microbiome composition (increasing beneficial Lactobacillus and Bifidobacterium), reduce systemic inflammation (CRP, IL-6), and influence the gut-brain axis via vagal afferents. Monsoon-season gut microbiome shifts (reduced Lactobacillus, increased Bacteroides, pathogen surge) precisely parallel the Vata Prakopa of Varsha. Basti resets ENS tone and microbiome during this vulnerable window.",
    },
    "Sharad": {
        "optimal": [
            {"karma": "Virechana", "full_name": "Virechana (Therapeutic Purgation) — Sharad Gold Standard",
             "dosha_target": "Pitta Prakopa (annual peak)",
             "classical_basis": "Charaka Samhita — Sutrasthana 16.19 and AH Su 3.55: Sharad is THE canonical season for Virechana — Pitta Prakopa peaks; purgation is the definitive Samshodhana.",
             "poorvakarma": "5–7 days Tikta Ghrita Snehapana + 2–3 days Bashpa/Nadi Svedana.",
             "pradhana_karma": "Trivrit leha (primary); Eranda taila or Icchabhedi for specific cases. Target 3–5 Vega. Administer at sunrise with warm water.",
             "pashchat_karma": "Samsarjana Krama (7 days graduated diet); avoid heat, spicy foods, alcohol, daytime sleep for 2 weeks.",
             "duration_total": "14–17 days",
             "contraindications": "Screen for Ama; avoid in active fever, pregnancy, severe Daurbalya."},
            {"karma": "Raktamokshana", "full_name": "Raktamokshana (Jalauka Avacharana) — Sharad optimal",
             "dosha_target": "Pitta–Rakta Dushthi (peak incidence)",
             "classical_basis": "Sushruta Samhita — Sutrasthana 14.26 and SS Sharira 8.22: Sharad is optimal for Raktamokshana — Pitta's peak aggravation of Rakta makes bloodletting most clinically effective.",
             "poorvakarma": "3 days Snehapana; adequate hydration",
             "pradhana_karma": "Jalauka (Hirudo medicinalis) applied to affected area; Haridra + honey post-procedure.",
             "pashchat_karma": "Cooling diet; no spicy/sour foods for 5 days; wound care daily.",
             "duration_total": "5–7 days; can repeat after 4 weeks",
             "contraindications": "Haemophilia, anaemia (Hb < 10 g/dL), anticoagulant therapy — absolute contraindications."},
        ],
        "beneficial": [
            {"karma": "Pitta-Nasya", "full_name": "Nasya (Shatapushpa / Chandana Taila)",
             "dosha_target": "Pitta-type Shiroroga",
             "classical_basis": "AH Uttara Sthana 22.18: Chandana/Kshira-based Nasya clears accumulated Pitta from Shiroroga during Sharad.",
             "poorvakarma": "3 days local Abhyanga with coconut oil",
             "pradhana_karma": "Shatapushpa taila or Chandana taila — 4–6 drops; 7 days.",
             "duration_total": "10 days",
             "contraindications": "Avoid in active URTI; 3-day gap after Virechana."},
        ],
        "use_with_caution": [
            {"karma": "Anuvasana Basti",
             "reason": "Vata is in Prashama — can use Anuvasana Basti for chronic Vata disorders; Niruha composition should be Pitta-pacifying (Madhura, Tikta Dravyas)."},
        ],
        "avoid": [
            {"karma": "Vamana", "reason": "Kapha is settled in Sharad; Vamana is not indicated and aggravates Vata-Pitta in the post-monsoon-depleted body."},
            {"karma": "Vigorous Svedana", "reason": "Pitta is in Prakopa — intense heat-based Svedana dangerously aggravates Pitta and Rakta. Use only mild Nadi Svedana if required."},
        ],
        "ritusandhi_note": "Sharad–Hemanta Ritusandhi (last 7 days of Sharad): Reduce Samshodhana intensity. Begin Rasayana and Brumhana (nourishing) protocols. This is the opening of the ideal Rasayana administration window — begin Brahma Rasayana or Chyawanprasha.",
        "agni_guidance": "Agni begins recovering in Sharad after Varsha depletion. Confirm Sama or Tikshna Agni before Virechana. Use Kutaja Ghana Vati + warm water for 3 days to assess Agni state — proceed only when appetite is clear and tongue coat absent.",
        "rasayana_window": "Post-Virechana Sharad: Brahma Rasayana and Amalaki Rasayana — purified Pitta channels ensure maximum efficacy. Triphala churna with ghee + honey at bedtime begins the Rasayana window.",
        "scientific_insight": "Melatonin-cortisol balance shifts significantly post-autumnal equinox, activating pro-inflammatory cytokine cascades (IL-1β, IL-6, TNF-α) — directly paralleling Pitta Prakopa theory. Hepatic Phase I/II detoxification remains highly active in early Sharad. Virechana in this window likely modulates LPS-triggered TLR4 signalling — a key inflammatory pathway in metabolic syndrome, NASH, and autoimmune conditions. Research on purgative herbs (Cassia angustifolia / Senna) confirms bile acid metabolism resetting post-purgation.",
    },
    "Hemanta": {
        "optimal": [
            {"karma": "Brumhana Basti", "full_name": "Brumhana Basti (Nourishing Kshira Basti)",
             "dosha_target": "Dhatu Brumhana; Vata Prashama maintenance",
             "classical_basis": "Charaka Samhita — Siddhisthana 12.14: Hemanta with strong Agni and Vata Prashama is ideal for Brumhana Basti using Kshira and Ashwagandha-based preparations.",
             "poorvakarma": "7–10 days Mahanarayan taila Abhyanga",
             "pradhana_karma": "Kshira Basti (milk + Ashwagandha/Shatavari); Yoga Basti (16 sessions) or Kala Basti (16 sessions).",
             "pashchat_karma": "Balanced warm nourishing diet; continue daily Abhyanga for 2 weeks.",
             "duration_total": "23–37 days",
             "contraindications": "Avoid during fever; not suitable for Ama-dominant presentations."},
            {"karma": "Rasayana Administration", "full_name": "Kaya Kalpa Rasayana Therapy",
             "dosha_target": "Dhatu nourishment; Ojas and Vyadhikshamatva enhancement",
             "classical_basis": "Charaka Samhita — Chikitsa Sthana 1.1.7: Hemanta and Shishira are explicitly THE optimal seasons for Rasayana — strongest Agni ensures maximal assimilation.",
             "poorvakarma": "3–5 days Mridu Virechana to clear Srotas",
             "pradhana_karma": "Brahma Rasayana / Chyawanprasha Avaleha / Ashwagandha Rasayana. 30–90 days continuous administration.",
             "duration_total": "35–95 days",
             "contraindications": "Avoid in Ama Pradhan state; ensure Srotas Shodhana before beginning."},
        ],
        "beneficial": [
            {"karma": "Brumhana Nasya", "full_name": "Brumhana Nasya (Kshira/Ashwagandha Taila)",
             "dosha_target": "Prana-Udana Vata protection; Shiras nourishment",
             "classical_basis": "AH Sutrasthana 20.4: Cold-dry air in Hemanta aggravates Prana and Udana Vata; Brumhana Nasya protects Mastishka (brain) channels.",
             "poorvakarma": "3–5 days local head Abhyanga + Nadi Svedana",
             "pradhana_karma": "Kshira taila or Ashwagandha taila — 4–6 drops per nostril; 7–14 days.",
             "duration_total": "10–17 days",
             "contraindications": "Avoid during acute URTI or sinusitis."},
        ],
        "use_with_caution": [
            {"karma": "Mridu Vamana",
             "reason": "Kapha Sanchaya begins in Hemanta — very mild Vamana is acceptable for specific chronic Kapha conditions, but full Shodhana Vamana is best deferred to Vasanta when Kapha is in Prakopa."},
        ],
        "avoid": [
            {"karma": "Raktamokshana", "reason": "Cold-induced vasoconstriction in Hemanta makes bloodletting risky; wound healing is significantly slower in cold months; strictly avoid unless compelled by specific urgent indication."},
            {"karma": "Vigorous Niruha Basti (Samshodhana)", "reason": "The focus in Hemanta is Brumhana (nourishing), not Samshodhana (eliminating); vigorous eliminating Niruha is counterproductive to the tissue-building goals of the season."},
        ],
        "ritusandhi_note": "Hemanta–Shishira Ritusandhi (last 7 days of Hemanta): Continue Rasayana and Brumhana protocols without interruption — this is one of the more benign Ritusandhi junctions. No major protocol change needed; simply ensure warm environment continuity.",
        "agni_guidance": "Jatharagni is very strong in Hemanta — the body can metabolise and assimilate even heavy, nourishing foods. Classical Hemanta Ritucharya explicitly recommends Mahamamsarasa, Kshira preparations, and Ghrita-rich diet. Avoid over-restriction — adequate caloric intake is important.",
        "rasayana_window": "PEAK Rasayana window begins. Chyawanprasha, Brahma Rasayana, Ashtavarga-based formulations — all are maximally effective due to strong Agni and optimal Dhatu-building anabolic environment.",
        "scientific_insight": "Winter thermogenesis activates brown adipose tissue (BAT) and increases mitochondrial biogenesis — directly corresponding to the classical 'strong Agni' of Hemanta. Anabolic hormones (GH, IGF-1, testosterone) peak in winter months, supporting classical emphasis on tissue-building (Brumhana). Vitamin D levels are low but paradoxically immune-modulating activity is enhanced via VDR nuclear signalling — complementing Rasayana adaptogenic mechanisms.",
    },
    "Shishira": {
        "optimal": [
            {"karma": "Brumhana Basti (continued)", "full_name": "Yoga Basti / Kala Basti (Brumhana focus)",
             "dosha_target": "Kapha Sanchaya prevention + lingering Vata management",
             "classical_basis": "CS Siddhisthana 12.16: Shishira shares the strong-Agni of Hemanta; Brumhana Basti with Ashwagandha-Shatavari preparations highly effective.",
             "poorvakarma": "7 days Kshirabala taila Abhyanga",
             "pradhana_karma": "Yoga Basti (16 sessions) — alternate Anuvasana (Kshira Basti) and mild Niruha.",
             "duration_total": "20–25 days",
             "contraindications": "Avoid in Ama; ensure Agni adequacy before starting."},
            {"karma": "Rasayana Administration (peak)", "full_name": "Kaya Kalpa — peak administration window",
             "dosha_target": "Ojas, Bala, Vyadhikshamatva",
             "classical_basis": "Charaka Samhita — Chikitsa Sthana 1.1.8: 'Shishire Balam Uttamam' — strength is at annual peak in Shishira; Rasayana absorbs best.",
             "poorvakarma": "Mridu Virechana for channel clearance (3–5 days)",
             "pradhana_karma": "Ashwagandha Rasayana / Chyawanprasha. 45–90 days continuous.",
             "duration_total": "50–95 days",
             "contraindications": "Ama-dominant tongue or poor appetite — defer until Deepana-Pachana complete."},
        ],
        "beneficial": [
            {"karma": "Brumhana Nasya", "full_name": "Brumhana Nasya",
             "dosha_target": "Prana Vata; Vata-type Shiroroga",
             "classical_basis": "AH Sutrasthana 20.3: Nasya with Kshira preparations protects against Shishira dryness and Vata in head channels.",
             "poorvakarma": "3 days local Abhyanga + steam",
             "pradhana_karma": "Kshira taila — 4–6 drops; 7 days.",
             "duration_total": "10 days",
             "contraindications": "Avoid during acute URTI."},
        ],
        "use_with_caution": [
            {"karma": "Mridu Virechana",
             "reason": "For specific residual Pitta conditions from Sharad only. Cold ambient makes Samsarjana Krama challenging — ensure warm indoor recovery environment throughout."},
        ],
        "avoid": [
            {"karma": "Vamana (Shodhana)", "reason": "Kapha is only in Sanchaya in Shishira, NOT yet in Prakopa — Vamana is premature; aggravates Vata and depletes Ojas. Save for Vasanta."},
            {"karma": "Raktamokshana", "reason": "Cold vasoconstriction + poorest wound healing of the year; strictly avoid in Shishira and Hemanta."},
            {"karma": "Intense Bashpa Svedana", "reason": "Paradoxically, intense Svedana in dry-cold Shishira depletes body fluids rapidly and aggravates Vata despite surface heat application."},
        ],
        "ritusandhi_note": "Shishira–Vasanta Ritusandhi (last 7 days of Shishira — CLINICALLY CRITICAL PREPARATION): Begin Deepana-Pachana 5–7 days before Vasanta to prepare accumulating Kapha for imminent Vamana. CS Sutrasthana 6.21 explicitly describes this preparatory phase. Patients with Kapha-dominant conditions (Tamaka Shwasa, Sthaulya, Madhumeha) should begin Udwartana and dietary restriction NOW.",
        "agni_guidance": "Tikshna Agni (sharp, intense) in Shishira — avoid EXCESSIVE Snehapana without clear indication; Ama can paradoxically form from oversaturation with heavy oleating agents given to a body not requiring it. Match Brumhana to Agni capacity.",
        "rasayana_window": "PEAK Rasayana window along with Hemanta. 'Shishire Balam Uttamam' (Charaka). Vasanta Kusumakara Rasa, Ashwagandha, Shatavari — all maximally effective now due to strong Agni and peak anabolic state.",
        "scientific_insight": "Cold-induced thermogenesis and insulin sensitivity are paradoxically at their annual peak in Shishira — the metabolic environment is optimal for anabolic processes. Melatonin levels are highest (longest nights), driving circadian alignment and enhancing cellular repair. Immune memory consolidation (IgG class switching, immunological memory formation) is strongest in winter — directly paralleling Vyadhikshamatva enhancement through Rasayana. Research on adaptogenic herbs (Withania somnifera, Asparagus racemosus) confirms maximal absorption and bioavailability in winter months.",
    },
}

RITUSANDHI_INSIGHTS = {
    "Shishira->Vasanta": {
        "description": "Cold-Dry to Cool-Moist transition",
        "classical_ref": "Charaka Samhita — Sutrasthana 6.21: 'Ritusandhou Poorvaritu Viruddham Acharanam Tyajet' — gradually abandon the regimen of the preceding season.",
        "physiological_shift": "Vascular tone shifts from cold-induced constriction to spring vasodilation; Kapha liquefies from accumulated solid state, increasing mucus secretion and lymphatic load.",
        "vulnerable_systems": "Respiratory, lymphatic, nasal sinuses, upper GI (Kapha Srotas)",
        "preparatory_protocol": "1) Shift to lighter meals (reduce ghee, dairy, sweets). 2) Begin Trikatu with warm water post-meals. 3) Dry powder massage (Udwartana) — replace oil massage. 4) Increase morning exercise intensity. 5) Begin Deepana-Pachana with Chitrakadi Vati.",
        "scientific_insight": "Circadian clock gene resetting (CLOCK, BMAL1) occurs at equinoctial transitions. Immune system shifts from Th2 (winter/Kapha) to Th1 activation (spring), creating a transient inflammatory window. Spring allergy incidence peaks — parallel to Kapha Prakopa theory.",
        "duration_warning": "14-day transition protocol recommended.",
    },
    "Vasanta->Grishma": {
        "description": "Cool-Moist to Hot-Dry transition",
        "classical_ref": "AH Sutrasthana 3.27: Progressive reduction of Kapha and activation of Pitta Sanchaya begins at Vasanta-Grishma junction.",
        "physiological_shift": "Thermoregulatory load increases; plasma volume contracts as sweating intensifies; Pitta-Rakta accumulation begins in peripheral circulation.",
        "vulnerable_systems": "Cardiovascular, skin, liver, small intestine (Pitta-Rakta Srotas)",
        "preparatory_protocol": "1) Increase fluid intake (coconut water, coriander water, buttermilk). 2) Introduce cooling foods — Shali rice, Yava, Shatavari. 3) Reduce spicy/fermented/sour intake. 4) Begin Pitta-pacifying Abhyanga (coconut oil instead of sesame).",
        "scientific_insight": "Heat stress activates HSP (Heat Shock Protein) chaperone pathways. Plasma aldosterone rises to conserve sodium, potentially elevating blood pressure — classical Pitta-Rakta correlation. Hepatic CYP450 enzymes peak in early summer.",
        "duration_warning": "14-day transition protocol recommended.",
    },
    "Grishma->Varsha": {
        "description": "Hot-Dry to Warm-Wet transition — MOST VULNERABLE TRANSITION OF THE YEAR",
        "classical_ref": "Charaka Samhita — Vimana Sthana 3.6: Grishma-Varsha junction is explicitly cited as the highest-risk Ritusandhi for Janapadodhvamsa (epidemic diseases).",
        "physiological_shift": "Sudden atmospheric cooling, humidity surge, and reduced sunlight simultaneously destabilise all three Doshas — Vata activates (barometric drop), Pitta disturbed (acid rain, sudden cooling), Kapha surges (humidity). Agni drops sharply within 48 hours of monsoon onset.",
        "vulnerable_systems": "GI tract (Agni), joints, respiratory, skin — ALL systems simultaneously vulnerable",
        "preparatory_protocol": "1) MANDATORY: Stop all vigorous Panchakarma courses. 2) Boiled/filtered water only. 3) Avoid raw vegetables, leafy greens, street food. 4) Take Haritaki + Rock salt daily. 5) Warm Ushna Jala throughout day. 6) Reduce dairy to well-boiled milk only.",
        "scientific_insight": "Monsoon onset disrupts gut microbiome diversity — Bacteroidetes/Firmicutes ratio shifts significantly, increasing GI infection susceptibility. Atmospheric pressure drops trigger baroreceptor-mediated autonomic responses (Vata-type). Water-borne pathogen surge (V. cholerae, E. coli, enteroviruses) aligns with Janapadodhvamsa described in Vimana Sthana 3.",
        "duration_warning": "21-day cautious protocol — the most important Ritusandhi in clinical practice.",
    },
    "Varsha->Sharad": {
        "description": "Warm-Wet to Warm-Dry transition — Pitta Prakopa ignition",
        "classical_ref": "Charaka Samhita — Sutrasthana 6.43: 'Sharad Ritau Pitta Prakopah' — accumulated Pitta of Varsha is released into Prakopa when sunshine returns post-monsoon.",
        "physiological_shift": "Monsoon withdrawal + returning sunshine creates sharp humidity-heat combinations. Pitta releases from Sanchaya into Prakopa within days of clear weather.",
        "vulnerable_systems": "Skin, liver, small intestine, eyes, blood (Rakta Dushthi — Pittaja disorders peak here)",
        "preparatory_protocol": "1) Begin Pitta-pacifying foods — Tikta Ghrita, bitter vegetables (Patola, Nimba). 2) Avoid fermented/sour foods. 3) Reduce Basti; prepare for Virechana by starting Snehapana. 4) Madhura-Tikta diet balance.",
        "scientific_insight": "Post-monsoon solar radiation surge activates cutaneous Vitamin D synthesis but simultaneously increases reactive oxygen species (ROS) production — Pitta-Rakta correlation. Hepatic oxidative stress markers peak in early Sharad. Virechana's antioxidant-stimulating mechanism has measurable impact on hepatic GSH/GSSG ratio.",
        "duration_warning": "14-day transition protocol recommended.",
    },
    "Sharad->Hemanta": {
        "description": "Warm-Dry to Cool-Moist transition — anabolic shift begins",
        "classical_ref": "AH Sutrasthana 3.54: Begin Brumhana and Rasayana as Pitta recedes and Agni strengthens at Sharad-Hemanta junction.",
        "physiological_shift": "Pitta recedes, metabolic rate increases with cooling, Agni strengthens — body shifts from catabolic (Pitta) to anabolic (Kapha-Vata-Agni balance) state.",
        "vulnerable_systems": "Respiratory (Kapha Sanchaya begins), joints (Vata-cold), nervous system (Vata-Shiroroga)",
        "preparatory_protocol": "1) Increase warm, nourishing, oily foods. 2) Begin Abhyanga with sesame oil. 3) Start Rasayana preparations (Chyawanprasha window opens). 4) Reduce cooling/bitter foods gradually.",
        "scientific_insight": "Shortening photoperiod activates melatonin secretion, resetting circadian rhythm and enhancing slow-wave sleep — tissue repair is maximised. Anabolic hormones (GH, IGF-1) begin seasonal rise. Mitochondrial biogenesis upregulation (PGC-1alpha pathway) corresponds to Agni strengthening.",
        "duration_warning": "14-day transition protocol recommended.",
    },
    "Hemanta->Shishira": {
        "description": "Cool-Moist to Cold-Dry transition — mild transition",
        "classical_ref": "Charaka Samhita — Sutrasthana 6.7: Hemanta and Shishira share nearly identical regimen; this Ritusandhi is the mildest of all six junctions.",
        "physiological_shift": "Gradual cold-drying of environment; Kapha Sanchaya deepens; Agni remains strong. Most stable Ritusandhi.",
        "vulnerable_systems": "Joints (Vata-cold), skin (dryness), respiratory (cold dry air)",
        "preparatory_protocol": "1) Increase sesame/ghee in diet. 2) Ensure warm clothing and head covering. 3) Continue Abhyanga and Rasayana without interruption. 4) Protect joints from cold/wind exposure.",
        "scientific_insight": "Cold-induced BAT activation continues deepening; thermogenic state is maintained. Circadian alignment is maximum in this season — insulin sensitivity at annual peak, supporting Brumhana and Rasayana assimilation.",
        "duration_warning": "7-day minimal protocol adjustment — the most benign transition.",
    },
}


def get_panchakarma_advice(current_rutu: str, vyapad_status: str = "", prakruti: str = "", condition: str = "") -> dict:
    advice = PANCHAKARMA_RUTU_MAP.get(current_rutu, {})
    if not advice:
        return {}
    advice = dict(advice)
    extra_cautions = []
    if vyapad_status and "Vyapad" in vyapad_status:
        extra_cautions.append(
            "RUTU-VYAPAD ACTIVE: Seasonal aberration detected. Avoid initiating new Samshodhana Panchakarma. "
            "Perform Deepana-Pachana and wait for weather stabilisation before proceeding."
        )
    advice["extra_cautions"] = extra_cautions
    return advice


def calculate_ritusandhi_status(target_date: datetime.date) -> dict:
    year = target_date.year
    transitions = []
    for rutu, (month, day) in RUTU_START_DATES.items():
        for y in [year - 1, year, year + 1]:
            try:
                transitions.append((datetime.date(y, month, day), rutu))
            except ValueError:
                pass
    transitions.sort(key=lambda x: x[0])

    current_rutu = "Hemanta"
    next_transition_date = None
    next_rutu = None

    for i, (d, rutu) in enumerate(transitions):
        if d <= target_date:
            current_rutu = rutu
            if i + 1 < len(transitions):
                next_transition_date = transitions[i + 1][0]
                next_rutu = transitions[i + 1][1]

    if next_transition_date is None:
        return {"is_in_ritusandhi": False, "days_to_next_transition": 99,
                "current_rutu": current_rutu, "next_rutu": "Unknown", "urgency": "none"}

    days_to_next = (next_transition_date - target_date).days
    transition_key = f"{current_rutu}->{next_rutu}"
    insight = RITUSANDHI_INSIGHTS.get(transition_key, {})

    if days_to_next <= 7:
        urgency = "critical"
    elif days_to_next <= 14:
        urgency = "imminent"
    elif days_to_next <= 21:
        urgency = "approaching"
    else:
        urgency = "none"

    return {
        "is_in_ritusandhi": days_to_next <= 7,
        "days_to_next_transition": days_to_next,
        "next_transition_date": next_transition_date,
        "current_rutu": current_rutu,
        "next_rutu": next_rutu,
        "transition_key": transition_key,
        "insight": insight,
        "urgency": urgency,
    }
