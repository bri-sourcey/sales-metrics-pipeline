# Sales Metrics Pipeline

Automated data extraction and reporting pipeline for sales/call center metrics. Built to reduce manual reporting overhead by automating hourly data pulls from CRM and dialer systems.

## Features

- **Automated Web Scraping**: Selenium-based extraction from legacy CRM/dialer platforms
- **Scheduled Execution**: Runs hourly via Windows Task Scheduler
- **Organized Data Storage**: Auto-sorts raw data by date
- **Environment-Based Config**: Credentials stored securely in `.env`

## Tech Stack

- Python 3.x
- Selenium + WebDriver Manager
- Pandas (for data processing)
- python-dotenv

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and add your credentials

## Project Structure
```
sales-metrics-pipeline/
├── src/
│   └── scrapers/        # Web scraping modules
├── data/
│   ├── raw/             # Downloaded CSVs by date
│   └── processed/       # Cleaned/transformed data
├── outputs/             # Final reports
└── .env.example         # Credential template
```

## Use Case

Originally built to automate hourly sales and compliance reporting, reducing manual data entry from ~30 min/day to zero.