@echo off
echo ============================================================
echo  Desha-Kala Clinical Navigator v2
echo  Starting Ayurvedic Clinical Decision Support App...
echo ============================================================
cd /d "%~dp0"
streamlit run app.py --server.port 8502 --server.headless false
pause
