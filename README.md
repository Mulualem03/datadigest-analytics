# DataDigest Analytics - Modern Data Stack Project

## Project Overview
A comprehensive data engineering project implementing Modern Data Stack architecture for digital media analytics. This project simulates a real-world business scenario where a digital media company needs unified analytics across multiple data sources.

## Business Problem
**Company**: DataDigest (hypothetical digital media company)
**Challenge**: Editorial team operates on intuition without unified view of content performance
**Goal**: Build centralized analytics platform to enable data-driven content decisions

## Architecture
- **Ingestion**: Airbyte (Open Source)
- **Orchestration**: Apache Airflow
- **Storage & Compute**: Google BigQuery
- **Transformation**: dbt Core
- **Visualization**: Metabase/Looker Studio

## Data Sources
1. **Medium Articles**: RSS feeds from popular publications
2. **Social Media**: Twitter mentions and Reddit discussions
3. **Web Analytics**: Synthetic traffic data mimicking GA4

## Technology Stack
- **Python 3.13** - Data processing and scripting
- **Docker** - Containerization
- **Google Cloud Platform** - Cloud infrastructure
- **SQL** - Data transformation
- **Git** - Version control

## Project Structure
datadigest-analytics/
├── data/                   # Data storage layers
│   ├── raw/               # Raw ingested data
│   ├── processed/         # Cleaned data
│   └── external/          # Reference data
├── scripts/               # Data processing scripts
│   ├── data_exploration/  # Data collection scripts
│   ├── ingestion/         # ETL scripts
│   └── processing/        # Data processing utilities
├── sql/                   # SQL transformations
│   ├── raw/               # Raw data models
│   ├── staging/           # Staging models
│   └── marts/             # Business logic models
├── airflow/               # Workflow orchestration
├── config/                # Configuration files
└── docs/                  # Documentation

## Current Status
- [x] Foundation setup and environment configuration
- [x] Project structure and Git repository
- [ ] Data collection framework
- [ ] Automated ingestion pipeline (Airbyte)
- [ ] Data transformation models (dbt)
- [ ] Orchestration workflows (Airflow)
- [ ] Visualization dashboards

## Getting Started

### Prerequisites
- Python 3.11+
- Docker Desktop
- Google Cloud SDK
- Git

### Setup
1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure GCP credentials
6. Run data collection: `python scripts/data_exploration/enhanced_medium_scraper.py`

## Author
**Mulualem Kahssay**
- Email: mulualemkahssay@gmail.com
- GitHub: [@Mulualem03](https://github.com/Mulualem03)

## License
MIT License
