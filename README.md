# 📈 Equity Scanner

A Python-based Equity Scanner that automates the complete workflow of collecting, processing, storing, and analyzing NSE equity market data.

The project downloads historical market data, performs data validation and cleaning, stores the processed data in PostgreSQL, and provides multiple stock scanners to identify potential trading opportunities based on price action, volume, delivery percentage, and breakout strategies.

> **Current Version:** v1.0 (Basic Equity Scanner)

---

# Table of Contents

- Overview
- Features
- Tech Stack
- Project Structure
- Workflow
- Scanner Modules
- Installation
- Database Setup
- How to Run
- Future Enhancements
- Author

---

# Overview

The objective of this project is to build a modular and scalable equity screening system capable of processing large volumes of historical NSE data and generating actionable trading opportunities.

The current version focuses on **end-of-day (EOD)** equity scanning using historical market data.

The project has been designed with scalability in mind so that advanced technical indicators, options analysis, dashboards, and real-time market scanning can be added in future versions.

---

# Features

## Data Pipeline

- Download daily NSE Bhavcopy data
- Validate downloaded files
- Merge daily datasets
- Clean and standardize market data
- Generate data quality reports
- Load processed data into PostgreSQL

---

## Database

- PostgreSQL integration
- Optimized schema
- Indexed tables
- Repository layer for database access

---

## Scanner Engine

Current scanners include:

- High Delivery Scanner
- Volume Breakout Scanner
- Price Breakout Scanner
- Gap Scanner
    - Gap Up
    - Gap Down
- 52 Week High Scanner
- Smart Money Scanner

---

## Application

- Modular architecture
- Interactive CLI
- Scanner Manager
- Run individual scanners
- Run all scanners together

---

# Tech Stack

### Programming Language

- Python

### Database

- PostgreSQL

### Libraries

- Pandas
- NumPy
- SQLAlchemy
- psycopg2
- Requests
- BeautifulSoup4
- tqdm

---

# Project Structure

```
Equity Scanner
│
├── data
│   ├── raw
│   └── processed
│
├── database
│   ├── migrations
│   ├── database.py
│   ├── loader.py
│   ├── schema.sql
│   └── indexes.sql
│
├── docs
│
├── scripts
│   ├── downloader
│   ├── processing
│   ├── scanner
│   │   ├── base.py
│   │   ├── repository.py
│   │   └── scanners
│   │       ├── delivery.py
│   │       ├── volume.py
│   │       ├── breakout.py
│   │       ├── gap.py
│   │       ├── high52week.py
│   │       └── smart_money.py
│   │
│   ├── tests
│   ├── config.py
│   ├── download_data.py
│   ├── run.py
│   └── utils.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Workflow

```
Download NSE Data
        │
        ▼
Validate CSV Files
        │
        ▼
Merge Daily Files
        │
        ▼
Clean Data
        │
        ▼
Quality Validation
        │
        ▼
Load into PostgreSQL
        │
        ▼
Repository Layer
        │
        ▼
Scanner Engine
        │
        ▼
Trading Opportunities
```

---

# Scanner Modules

## High Delivery Scanner

Identifies stocks with unusually high delivery percentage, indicating potential accumulation.

---

## Volume Breakout Scanner

Detects stocks trading with significantly higher volume compared to their recent average.

---

## Price Breakout Scanner

Identifies stocks closing above their previous 20-day high.

---

## Gap Scanner

Detects:

- Gap Up
- Gap Down

using configurable percentage-based gap detection.

---

## 52 Week High Scanner

Identifies stocks trading above their previous 52-week high.

---

## Smart Money Scanner

A strategy-based scanner that combines multiple market conditions:

- High Delivery
- Volume Breakout
- Price Breakout
- Liquidity Filter

This scanner generates high-conviction trading candidates by combining multiple screening conditions.

---

# Installation

Clone the repository.

```bash
git clone https://github.com/<your-username>/equity-scanner.git

cd equity-scanner
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Database Setup

Create a PostgreSQL database.

Execute:

- schema.sql
- indexes.sql

Update database credentials inside:

```
database/database.py
```

Load processed data into PostgreSQL using the loader module.

---

# How to Run

Run the main application.

```bash
python -m scripts.run
```

The CLI allows you to:

- Run High Delivery Scanner
- Run Volume Breakout Scanner
- Run Price Breakout Scanner
- Run Gap Scanner
- Run 52 Week High Scanner
- Run Smart Money Scanner
- Run all scanners

---

# Current Status

### Completed

- Downloader
- Data Validation
- Merge Pipeline
- Data Cleaning
- Quality Checks
- PostgreSQL Integration
- Repository Layer
- Scanner Framework
- Smart Money Scanner
- Interactive CLI

---

# Future Enhancements

This project is under active development.

Planned features include:

- RSI Scanner
- MACD Scanner
- EMA & SMA Strategies
- Bollinger Bands
- Candlestick Pattern Recognition
- Options Scanner
- Relative Strength Scanner
- ATR Scanner
- Watchlist Support
- CSV & Excel Export
- Dashboard (Streamlit/Flask)
- REST API
- Live NSE Data
- Scheduled Daily Scans
- Email & Telegram Alerts

---

# License

This project is developed for educational and learning purposes.

---

# Author

**Tanishq Arya**

B.Tech Computer Science Engineering

Aspiring Data Analyst | Python Developer | SQL | PostgreSQL | Data Analytics

---

## Version

Current Release:

**Equity Scanner v1.0**

Future versions will introduce advanced technical indicators, options analysis, live market scanning, dashboards, and AI-assisted stock screening.