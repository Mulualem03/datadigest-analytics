# DataDigest Analytics - Modern Data Stack Project

A production-ready end-to-end data pipeline demonstrating modern data engineering best practices using open-source tools and cloud infrastructure.

## 📊 Project Overview

DataDigest Analytics is a complete Modern Data Stack implementation for a hypothetical digital media company, transforming raw content data into actionable business intelligence through automated ETL pipelines.

### Business Problem
Digital media companies need to move beyond gut-feeling editorial decisions to data-driven content strategy. This project demonstrates how to:
- Aggregate data from multiple sources (articles, social media, web analytics)
- Transform raw data into unified analytics
- Automate daily pipeline execution
- Generate insights on content performance

### Architecture

```
Data Sources → Airbyte (Ingestion) → BigQuery (Warehouse) → dbt (Transformation) → Airflow (Orchestration)
     ↓              ↓                      ↓                    ↓                      ↓
4 CSV Files    Hourly Syncs         3-Layer Storage      SQL Models           Scheduled DAGs
(1,933 rows)                     (raw/staging/marts)   (clean/aggregate)      (daily at 6AM)
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Cloud Platform** | Google Cloud Platform | Infrastructure & compute |
| **Data Warehouse** | BigQuery | Columnar storage & analytics |
| **Data Ingestion** | Airbyte (Kubernetes) | Automated data collection |
| **Transformation** | dbt Core | SQL-based data modeling |
| **Orchestration** | Apache Airflow 3.0 | Workflow automation |
| **Languages** | Python 3.13, SQL | Data processing & pipelines |
| **Version Control** | Git/GitHub | Code management |

## 📁 Project Structure

```
datadigest-analytics/
├── airflow/
│   └── dags/
│       └── datadigest_pipeline.py    # Orchestration workflow
├── data/                              # Raw CSV files (4 sources)
├── datadigest_transform/              # dbt project
│   ├── models/
│   │   ├── staging/                   # Cleaned data models
│   │   └── marts/                     # Business analytics
│   └── dbt_project.yml
├── scripts/                           # Data collection scripts
└── README.md
```

## 🚀 Key Features

### 1. Automated Data Ingestion
- **4 data sources**: Medium articles, Twitter mentions, Reddit submissions, web analytics
- **1,933 total records** ingested and synchronized
- **Hourly sync schedule** via Airbyte
- **Schema validation** and error handling

### 2. Three-Layer Data Warehouse
- **Raw Layer**: Original data from Airbyte with metadata
- **Staging Layer**: Cleaned, typed, standardized data
- **Marts Layer**: Business-ready analytics tables

### 3. dbt Transformations
- **4 staging models**: Clean and standardize each data source
- **1 marts model**: `content_performance` - unified analytics combining all sources
- **Data quality tests**: Uniqueness and null checks
- **Documentation**: Auto-generated lineage graphs

### 4. Airflow Orchestration
- **Daily automated runs** at 6:00 AM UTC
- **38-second execution time**: dbt run → test → docs
- **Dependency management**: Sequential task execution
- **Manual trigger capability** for on-demand runs

## 📈 Results & Insights

### Pipeline Metrics
- **Total Records Processed**: 1,933
- **Final Analytics Rows**: 60 (unified content performance)
- **Data Quality**: 100% test pass rate
- **Pipeline Duration**: 38 seconds end-to-end

### Top Content Insights
1. **Most Engaging Article**: "Visual Guide to Gradient Boosted Trees" (355 engagement score)
2. **Best Publication**: Towards Data Science (4 of top 10 articles)
3. **Social Correlation**: Twitter engagement correlates with overall performance
4. **Traffic vs. Engagement**: High web sessions don't always equal social engagement

## 🏗️ Implementation Milestones

### Milestone 1-2: Data Collection & Cloud Setup
- Collected data from 4 sources (Medium, Twitter, Reddit, Web Analytics)
- Configured GCP project with BigQuery datasets
- Implemented 3-layer warehouse architecture

### Milestone 3A: Airbyte Ingestion
- Deployed Airbyte on local Kubernetes cluster
- Created 4 source-to-destination connections
- Automated hourly data synchronization
- Resolved schema conflicts and optimized storage

### Milestone 3B: dbt Transformation
- Built 4 staging models for data cleaning
- Created `content_performance` mart with joined analytics
- Implemented data quality tests
- Generated pipeline documentation

### Milestone 4: End-to-End Validation
- Validated complete data flow (raw → staging → marts)
- Generated lineage documentation
- Verified 1,933 raw records → 60 unified rows
- Confirmed all quality tests passing

### Milestone 5: Airflow Orchestration
- Installed Apache Airflow 3.0.6
- Created automated DAG with 3 tasks
- Scheduled daily execution at 6 AM UTC
- Successfully tested pipeline execution (38s runtime)

## 🔧 Setup Instructions

### Prerequisites
- Python 3.13+
- Google Cloud Platform account
- Docker Desktop (for Airbyte)
- Homebrew (macOS)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Mulualem03/datadigest-analytics.git
cd datadigest-analytics
```

2. **Set up virtual environment**
```bash
python3 -m venv dbt_venv
source dbt_venv/bin/activate
pip install -r requirements.txt
```

3. **Configure GCP credentials**
```bash
# Place your service account key in the project root
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
```

4. **Initialize dbt**
```bash
cd datadigest_transform
dbt debug  # Verify connection
dbt run     # Run transformations
dbt test    # Validate data quality
```

5. **Start Airflow**
```bash
export AIRFLOW_HOME=~/datadigest-analytics/airflow
airflow standalone  # Starts webserver + scheduler
# Access at http://localhost:8080
```

6. **Launch Airbyte** (optional for new data ingestion)
```bash
abctl local install
# Access at http://localhost:8000
```

## 📊 Data Model

### Content Performance Mart Schema

| Column | Type | Description |
|--------|------|-------------|
| `url` | STRING | Article URL (primary key) |
| `title` | STRING | Article title |
| `author` | STRING | Content author |
| `publication` | STRING | Publishing platform |
| `claps` | INT64 | Medium engagement metric |
| `twitter_likes` | INT64 | Twitter engagement |
| `reddit_upvotes` | INT64 | Reddit engagement |
| `total_sessions` | INT64 | Web traffic sessions |
| `social_engagement_score` | INT64 | Weighted engagement: claps + (twitter×2) + (reddit×3) |

## 🔍 Key Learnings

### Technical Insights
1. **Cloud-first architecture** reduces operational overhead
2. **dbt's ref() function** enables dynamic dependency management
3. **Airflow 3.0 syntax changes** require updated parameter names
4. **Airbyte Destinations V2** uses typed columns vs JSON storage

### Best Practices Implemented
- **Separation of concerns**: Clear raw/staging/marts boundaries
- **Idempotent transformations**: Safe to re-run without side effects
- **Data lineage tracking**: Full visibility from source to insight
- **Automated testing**: Quality gates at every transformation step
- **Version control**: Complete pipeline as code

## 🎯 Future Enhancements

- [ ] Replace synthetic data with real API integrations (Twitter/Reddit APIs)
- [ ] Add visualization layer (Looker, Tableau, or Metabase)
- [ ] Implement incremental models for large-scale data
- [ ] Deploy to production (Cloud Composer, dbt Cloud)
- [ ] Add email alerts for pipeline failures
- [ ] Create additional marts (author performance, publication trends)
- [ ] Implement machine learning models for content recommendation

## 👤 Author

**Mulualem Kahssay**
- GitHub: [@Mulualem03](https://github.com/Mulualem03)
- Email: mulualemkahssay@gmail.com
- Project Duration: September 17-23, 2025

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

Built as a demonstration of Modern Data Stack principles using entirely free and open-source tools. Special thanks to the communities behind Airbyte, dbt, and Apache Airflow for their excellent documentation and tools.

---

**Note**: This project uses synthetic data for demonstration purposes. All engagement metrics and analytics are simulated to showcase pipeline capabilities.
