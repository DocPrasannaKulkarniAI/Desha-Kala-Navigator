"""
utils.py (enhanced)
- Loads KB from app2/data first, then falls back to sibling app1/data folder.
- Wires Samhita corpus (external Excel) + built-in samhita_ref DB into UI-ready functions.
"""
import os
import pandas as pd
import streamlit as st

WORKBOOK_NAME = "Rutu_Desha_AI_KnowledgeBase_v1.0.xlsx"
PATHYA_APATHYA_FILE = "pathya_apathya_district_diet.xlsx"


def _find_knowledge_base_dir():
    """Search for the knowledge base workbook in multiple candidate locations."""
    this_file = os.path.abspath(__file__)
    app2_root = os.path.dirname(os.path.dirname(this_file))

    candidates = [
        os.path.join(app2_root, "data"),
        os.path.join(os.path.dirname(app2_root), "rutu-desha-app", "data"),
        os.path.join(os.path.dirname(app2_root), "data"),
    ]
    for d in candidates:
        if os.path.isfile(os.path.join(d, WORKBOOK_NAME)):
            return d
    return os.path.join(app2_root, "data")


@st.cache_data
def load_ayurvedic_knowledge_base():
    data_dir = _find_knowledge_base_dir()
    workbook_file = os.path.join(data_dir, WORKBOOK_NAME)

    master_file = os.path.join(data_dir, f"{WORKBOOK_NAME} - 02_Master District Data.csv")
    rutu_file = os.path.join(data_dir, f"{WORKBOOK_NAME} - 03_Rutu-District Profile.csv")
    foundations_file = os.path.join(data_dir, f"{WORKBOOK_NAME} - 04_Classical Foundations.csv")

    def _load_csv_or_excel(csv_path, sheet_name, header=1):
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path, header=header)
        if os.path.exists(workbook_file):
            return pd.read_excel(workbook_file, sheet_name=sheet_name, header=header)
        return None

    def _normalize_foundations(raw_df):
        if raw_df is None or raw_df.empty:
            return raw_df
        header_idx = None
        for idx, row in raw_df.iterrows():
            row_values = [str(x).strip() for x in row.values if pd.notna(x)]
            if any(v.lower() == "desha type" for v in row_values):
                header_idx = idx
                break
        if header_idx is not None:
            header_values = [str(x).strip() if pd.notna(x) else "" for x in raw_df.iloc[header_idx].values]
            normalized = raw_df.iloc[header_idx + 1:].copy()
            normalized.columns = header_values
            normalized = normalized.loc[:, normalized.columns != ""]
            normalized.columns = normalized.columns.str.strip()
            return normalized
        raw_df.columns = raw_df.columns.astype(str).str.strip()
        return raw_df

    master_df = _load_csv_or_excel(master_file, "02_Master District Data", header=1)
    if master_df is not None:
        master_df.columns = master_df.columns.str.strip()
        master_df = master_df.dropna(subset=["State / UT", "District"])
        master_df["State / UT"] = master_df["State / UT"].astype(str).str.strip()
        master_df["District"] = master_df["District"].astype(str).str.strip()
    else:
        st.error(f"Knowledge base not found. Expected workbook: {workbook_file}\nCopy 'Rutu_Desha_AI_KnowledgeBase_v1.0.xlsx' into the data/ folder.")
        master_df = None

    rutu_df = _load_csv_or_excel(rutu_file, "03_Rutu-District Profile", header=1)
    if rutu_df is not None:
        rutu_df.columns = rutu_df.columns.str.strip()
        rutu_df = rutu_df.dropna(subset=["State", "District", "Rutu (Season)"])
        rutu_df["State"] = rutu_df["State"].astype(str).str.strip()
        rutu_df["District"] = rutu_df["District"].astype(str).str.strip()
        rutu_df["Rutu (Season)"] = rutu_df["Rutu (Season)"].astype(str).str.strip()
        rename_map = {
            "Temp Mean (°C)": "Temp Mean (deg C)", "Temp Min (°C)": "Temp Min (deg C)",
            "Temp Max (°C)": "Temp Max (deg C)", "Diurnal Temp Range (°C)": "Diurnal Temp Range (deg C)",
        }
        rutu_df = rutu_df.rename(columns=rename_map)

    if os.path.exists(foundations_file) or os.path.exists(workbook_file):
        foundations_df = None
        try:
            for i in range(5):
                if os.path.exists(foundations_file):
                    temp_df = pd.read_csv(foundations_file, skiprows=i)
                else:
                    temp_df = pd.read_excel(workbook_file, sheet_name="04_Classical Foundations", skiprows=i)
                if "Desha Type" in temp_df.columns or any("JANGALA" in str(x) for x in temp_df.iloc[:, 0]):
                    foundations_df = _normalize_foundations(temp_df)
                    break
            if foundations_df is None:
                if os.path.exists(foundations_file):
                    foundations_df = pd.read_csv(foundations_file, header=2)
                else:
                    foundations_df = pd.read_excel(workbook_file, sheet_name="04_Classical Foundations", header=2)
                foundations_df = _normalize_foundations(foundations_df)
        except Exception:
            foundations_df = None
    else:
        foundations_df = None

    return master_df, rutu_df, foundations_df


def get_pathya_apathya_excel_path() -> str:
    """Return path to the Pathya-Apathya Excel dataset."""
    this_file = os.path.abspath(__file__)
    app2_root = os.path.dirname(os.path.dirname(this_file))
    return os.path.join(app2_root, "data", PATHYA_APATHYA_FILE)


@st.cache_data
def load_samhita_reference_corpus():
    """Load external Samhita Excel corpus if available."""
    candidates = [
        r"C:/Users/Prasanna/Downloads/samhitas_combined _v2.xlsx",
        r"C:/Users/Prasanna/Downloads/samhitas_combined_v2.xlsx",
    ]
    data_dir = _find_knowledge_base_dir()
    candidates.append(os.path.join(data_dir, "samhitas_combined_v2.xlsx"))

    for path in candidates:
        if os.path.exists(path):
            try:
                df = pd.read_excel(path, sheet_name="All Slokas")
                df.columns = [str(c).strip() for c in df.columns]
                keep_cols = [c for c in ["Source File", "Sthana", "Chapter", "Sloka No.", "Sloka Text", "Comments"] if c in df.columns]
                df = df[keep_cols].copy()
                for col in keep_cols:
                    df[col] = df[col].astype(str)
                return df
            except Exception:
                pass
    return None


def find_relevant_samhita_references(corpus_df, root_class: str, rutu: str = "", condition: str = "", top_n: int = 5):
    """Search external corpus with fallback to built-in database."""
    from src.samhita_ref import get_references_for_topic, SAMHITA_DB

    # Try external corpus
    if corpus_df is not None and not corpus_df.empty:
        keyword_map = {
            "JANGALA": ["jangala", "ruksha", "vata", "dry", "arid"],
            "ANUPA": ["anupa", "snigdha", "kapha", "humid", "marsh"],
            "SADHARANA": ["sadharana", "sama", "balanced"],
        }
        tokens = keyword_map.get(str(root_class).upper(), [])
        if rutu:
            tokens.append(rutu.lower())
        if condition and condition != "Not Provided":
            tokens.append(condition.lower())

        text_blob = (
            corpus_df.get("Sthana", "").astype(str) + " " +
            corpus_df.get("Chapter", "").astype(str) + " " +
            corpus_df.get("Sloka Text", "").astype(str) + " " +
            corpus_df.get("Comments", "").astype(str)
        ).str.lower()

        mask = pd.Series(False, index=corpus_df.index)
        for token in [t for t in tokens if t and t != "nan"]:
            mask = mask | text_blob.str.contains(token, regex=False)
        out = corpus_df[mask].head(top_n).copy()
        if not out.empty:
            return out, "external_corpus"

    # Fall back to built-in
    keys = [root_class.upper() if root_class else "SADHARANA"]
    if rutu:
        keys.append(rutu)
    if condition and condition != "Not Provided":
        keys.append(condition)
    built_in = get_references_for_topic(keys, max_per_topic=3)
    return built_in, "built_in"
