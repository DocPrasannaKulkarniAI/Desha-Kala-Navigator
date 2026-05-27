"""
engine.py (enhanced)
- map_date_to_rutu: solar-calendar Rutu mapping
- fetch_weather_7day: Open-Meteo 5-days history + 7-days forecast
- analyze_rutu_vyapad: seasonal aberration detection
"""
import datetime
import requests
import pandas as pd


def map_date_to_rutu(target_date):
    day = target_date.day
    month = target_date.month
    if (month == 1 and day >= 14) or (month == 2) or (month == 3 and day <= 13):
        return "Shishira"
    if (month == 3 and day >= 14) or (month == 4) or (month == 5 and day <= 13):
        return "Vasanta"
    if (month == 5 and day >= 14) or (month == 6) or (month == 7 and day <= 13):
        return "Grishma"
    if (month == 7 and day >= 14) or (month == 8) or (month == 9 and day <= 13):
        return "Varsha"
    if (month == 9 and day >= 14) or (month == 10) or (month == 11 and day <= 13):
        return "Sharad"
    return "Hemanta"


def _aggregate_hourly(hourly):
    df = pd.DataFrame({
        "time": hourly.get("time", []),
        "temp": hourly.get("temperature_2m", []),
        "rh": hourly.get("relative_humidity_2m", []),
        "precip": hourly.get("precipitation", []),
    })
    if df.empty:
        return pd.DataFrame()
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["time"]).copy()
    df["date"] = df["time"].dt.date
    daily = (
        df.groupby("date", as_index=False)
        .agg({"temp": "mean", "rh": "mean", "precip": "sum"})
        .sort_values("date")
    )
    return daily


def fetch_weather_7day(lat, lon):
    """Fetch 5 days history + 7 days forecast. Returns (history_df, forecast_df, compare_df)."""
    forecast_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,relative_humidity_2m,precipitation"
        "&past_days=5&forecast_days=7&timezone=auto"
    )
    try:
        response = requests.get(forecast_url, timeout=10)
        if response.status_code != 200:
            return None, None, None

        data = response.json()
        all_daily = _aggregate_hourly(data.get("hourly", {}))
        if all_daily.empty:
            return None, None, None

        today = datetime.date.today()
        history_daily = all_daily[all_daily["date"] < today].tail(5).copy()
        forecast_daily = all_daily[all_daily["date"] >= today].head(7).copy()

        # History view
        history_view = history_daily.copy()
        history_view["Date"] = pd.to_datetime(history_view["date"]).dt.strftime("%d %b %Y")
        history_view["Mean Temperature (deg C)"] = history_view["temp"].round(1)
        history_view["Mean Relative Humidity (%)"] = history_view["rh"].round(1)
        history_view["Total Rainfall (mm)"] = history_view["precip"].round(1)
        history_view = history_view[["Date", "Mean Temperature (deg C)", "Mean Relative Humidity (%)", "Total Rainfall (mm)"]]

        # 7-day forecast view with clinical interpretation
        forecast_view = forecast_daily.copy()
        forecast_view["Date"] = pd.to_datetime(forecast_view["date"]).dt.strftime("%d %b %Y")
        forecast_view["Forecast Temp (deg C)"] = forecast_view["temp"].round(1)
        forecast_view["Forecast RH (%)"] = forecast_view["rh"].round(1)
        forecast_view["Forecast Rain (mm)"] = forecast_view["precip"].round(1)

        def clinical_flag(row):
            flags = []
            if row["precip"] >= 20:
                flags.append("Heavy rain — avoid oily meals, protect Agni")
            elif row["precip"] >= 10:
                flags.append("Rain — lighter meals advised")
            if row["temp"] >= 36:
                flags.append("High heat — hydrate, avoid Pitta triggers")
            elif row["temp"] >= 33:
                flags.append("Warm — maintain cooling routine")
            if row["rh"] >= 80:
                flags.append("Very humid — Deepana-Pachana priority")
            elif row["rh"] >= 70:
                flags.append("Humid — light diet")
            if not flags:
                flags.append("Routine preventive care")
            return "; ".join(flags)

        forecast_view["Clinical Advisory"] = forecast_daily.apply(clinical_flag, axis=1)
        forecast_view = forecast_view[["Date", "Forecast Temp (deg C)", "Forecast RH (%)", "Forecast Rain (mm)", "Clinical Advisory"]]

        # Year-over-year comparison
        window_daily = pd.concat([history_daily, forecast_daily], ignore_index=True)
        comparison_view = None
        if not window_daily.empty:
            start_date = min(window_daily["date"])
            end_date = max(window_daily["date"])
            ly_start = start_date.replace(year=start_date.year - 1)
            ly_end = end_date.replace(year=end_date.year - 1)
            archive_url = (
                "https://archive-api.open-meteo.com/v1/archive"
                f"?latitude={lat}&longitude={lon}"
                f"&start_date={ly_start.isoformat()}&end_date={ly_end.isoformat()}"
                "&hourly=temperature_2m,relative_humidity_2m,precipitation"
                "&timezone=auto"
            )
            archive_resp = requests.get(archive_url, timeout=10)
            if archive_resp.status_code == 200:
                archive_daily = _aggregate_hourly(archive_resp.json().get("hourly", {}))
                if not archive_daily.empty:
                    row_map = {row["date"].strftime("%m-%d"): row for _, row in archive_daily.iterrows()}
                    rows = []
                    for _, row in window_daily.iterrows():
                        key = row["date"].strftime("%m-%d")
                        ly = row_map.get(key)
                        if ly is not None:
                            rows.append({
                                "Date": row["date"].strftime("%d %b %Y"),
                                "Temp deg C (Current [Last Year])": f"{row['temp']:.1f} ({ly['temp']:.1f})",
                                "Humidity % (Current [Last Year])": f"{row['rh']:.1f} ({ly['rh']:.1f})",
                                "Rain mm (Current [Last Year])": f"{row['precip']:.1f} ({ly['precip']:.1f})",
                            })
                    if rows:
                        comparison_view = pd.DataFrame(rows)

        return history_view, forecast_view, comparison_view
    except Exception:
        return None, None, None


# Keep backward-compatible alias
def fetch_weather_history_and_forecast(lat, lon):
    return fetch_weather_7day(lat, lon)


def analyze_rutu_vyapad(canonical_rutu, local_profile, real_time_df):
    if real_time_df is None or real_time_df.empty or local_profile is None or local_profile.empty:
        return {"status": "Prakritistha (Canonical Stable)", "reasons": [], "metrics": {"temp": 0, "rh": 0, "rain": 0}}

    try:
        baseline_temp = float(local_profile["Temp Mean (deg C)"].values[0])
        baseline_rh = float(local_profile["Humidity Mean (%)"].values[0])
    except Exception:
        return {"status": "Prakritistha (Canonical Stable)", "reasons": [], "metrics": {"temp": 0, "rh": 0, "rain": 0}}

    current_temp = real_time_df["Mean Temperature (deg C)"].mean()
    current_rh = real_time_df["Mean Relative Humidity (%)"].mean()
    current_rain = real_time_df["Total Rainfall (mm)"].sum()

    reasons = []
    is_aberrant = False

    if canonical_rutu == "Grishma" and current_rain > 15.0:
        is_aberrant = True
        reasons.append(f"Unseasonal rainfall ({current_rain:.1f} mm) during typically dry Grishma.")
    if abs(current_temp - baseline_temp) > 6.0:
        is_aberrant = True
        reasons.append(f"Marked temperature shift ({current_temp - baseline_temp:+.1f} deg C) versus local seasonal baseline.")
    if abs(current_rh - baseline_rh) > 25.0:
        is_aberrant = True
        reasons.append(f"Marked humidity shift ({current_rh - baseline_rh:+.1f}%) versus local seasonal baseline.")

    if is_aberrant:
        return {"status": "Rutu-Vyapad (Seasonal Aberration)", "reasons": reasons, "metrics": {"temp": current_temp, "rh": current_rh, "rain": current_rain}}
    return {"status": "Prakritistha (Canonical Stable)", "reasons": ["Recent weather is near long-term district-season baseline."], "metrics": {"temp": current_temp, "rh": current_rh, "rain": current_rain}}
