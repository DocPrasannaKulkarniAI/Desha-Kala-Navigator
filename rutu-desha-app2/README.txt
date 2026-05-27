================================================================
 DESHA-KALA CLINICAL NAVIGATOR v2
 Enhanced Ayurvedic Clinical Decision Support for Physicians
================================================================

WHAT'S NEW IN v2
-----------------
1. Panchakarma Timing Advisor    - Rutu-specific Karma guidance with
                                   Poorvakarma, Pradhana, Pashchat Karma
                                   details + scientific insights
2. Pathya-Apathya Quick Lookup   - District-specific wholesome/unwholesome
                                   food guidance with local food dataset
3. 7-Day Extended Forecast       - Open-Meteo 7-day forecast with daily
                                   Ayurvedic clinical advisories
4. Ritusandhi Early Warning      - Countdown to seasonal transition with
                                   preparation protocol + science
5. Dual-District Comparison      - Compare two patients side-by-side
6. Samhita Reference Auto-Linker - Every recommendation traced to
                                   Samhita → Sthana → Chapter → Sloka

SETUP INSTRUCTIONS
-------------------
STEP 1: Install Python 3.10+ if not already installed.
        https://www.python.org/downloads/

STEP 2: Install required packages.
        Open Command Prompt in this folder and run:
          pip install -r requirements.txt

STEP 3: Copy the knowledge base data file.
        Copy  "Rutu_Desha_AI_KnowledgeBase_v1.0.xlsx"
        into  rutu-desha-app2\data\
        (from your existing rutu-desha-app\data\ folder)

        The pathya_apathya_district_diet.xlsx is already included
        in the data\ folder — no action needed.

STEP 4: (Optional) Add Samhita corpus for extended references.
        Copy  "samhitas_combined _v2.xlsx"
        into  rutu-desha-app2\data\
        The app will auto-detect and use it.

STEP 5: Run the app.
        Double-click  run_app.bat
        OR run in Command Prompt:
          streamlit run app.py --server.port 8502

        The app opens at:  http://localhost:8502

FOLDER STRUCTURE
-----------------
rutu-desha-app2/
├── app.py                          ← Main Streamlit application
├── requirements.txt
├── run_app.bat
├── README.txt
├── .streamlit/
│   └── config.toml                 ← Green Ayurvedic theme
├── src/
│   ├── __init__.py
│   ├── engine.py                   ← Weather engine (7-day)
│   ├── utils.py                    ← Data loading + Samhita wiring
│   ├── panchakarma.py              ← Panchakarma Timing Advisor
│   ├── pathya_apathya.py           ← Pathya-Apathya module
│   └── samhita_ref.py              ← Classical reference database
└── data/
    ├── pathya_apathya_district_diet.xlsx  ← NEW: District food dataset
    └── Rutu_Desha_AI_KnowledgeBase_v1.0.xlsx  ← COPY FROM app v1

NOTES FOR PHYSICIANS
---------------------
* This app requires internet access for live weather data.
* All Panchakarma recommendations are advisory — clinical assessment
  of individual patient is always required before procedures.
* Pathya-Apathya guidance is based on classical texts and regional
  food availability data — adjust for individual patient allergies
  and preferences.
* Samhita references are from Charaka Samhita, Sushruta Samhita,
  Ashtanga Hridayam, and Madhava Nidana.

For support contact: prasanna4ai@gmail.com
================================================================
