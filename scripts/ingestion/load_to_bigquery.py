from google.cloud import bigquery
import pandas as pd
import json
import glob
import os
from datetime import datetime

class BigQueryLoader:
    def __init__(self, project_id):
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id
    
    def create_table_from_schema(self, dataset_id, table_id, schema_file):
        """Create BigQuery table from schema file."""
        with open(schema_file, 'r') as f:
            schema_config = json.load(f)
        
        schema = []
        for field in schema_config:
            field_type = getattr(bigquery.enums.SqlTypeNames, field['type'])
            mode = field['mode']
            schema.append(bigquery.SchemaField(field['name'], field_type, mode=mode))
        
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = bigquery.Table(table_ref, schema=schema)
        
        try:
            table = self.client.create_table(table)
            print(f"Created table {dataset_id}.{table_id}")
            return True
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"Table {dataset_id}.{table_id} already exists")
                return True
            else:
                print(f"Error creating table {dataset_id}.{table_id}: {e}")
                return False
    
    def load_csv_to_table(self, dataset_id, table_id, csv_file):
        """Load CSV data to BigQuery table."""
        try:
            df = pd.read_csv(csv_file)
            print(f"Loading {len(df)} rows from {csv_file}")
            
            table_ref = self.client.dataset(dataset_id).table(table_id)
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                skip_leading_rows=1,
                autodetect=False,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
            )
            
            with open(csv_file, 'rb') as source_file:
                job = self.client.load_table_from_file(
                    source_file, table_ref, job_config=job_config
                )
            
            job.result()
            
            table = self.client.get_table(table_ref)
            print(f"Loaded {table.num_rows} rows to {dataset_id}.{table_id}")
            return True
            
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
            return False

def main():
    loader = BigQueryLoader('datadigest-analytics-2025')
    
    # Define table configurations
    table_configs = [
        {
            'dataset': 'datadigest_raw',
            'table': 'medium_articles',
            'schema': 'config/schemas/raw_medium_articles.json',
            'data_pattern': 'data/raw/medium_articles_enhanced_*.csv'
        },
        {
            'dataset': 'datadigest_raw',
            'table': 'twitter_mentions',
            'schema': 'config/schemas/raw_twitter_mentions.json',
            'data_pattern': 'data/raw/twitter_synthetic_*.csv'
        },
        {
            'dataset': 'datadigest_raw',
            'table': 'reddit_submissions',
            'schema': 'config/schemas/raw_reddit_submissions.json',
            'data_pattern': 'data/raw/reddit_synthetic_*.csv'
        },
        {
            'dataset': 'datadigest_raw',
            'table': 'web_analytics',
            'schema': 'config/schemas/raw_web_analytics.json',
            'data_pattern': 'data/raw/web_analytics_*.csv'
        }
    ]
    
    successful_loads = 0
    
    for config in table_configs:
        print(f"\n{'='*50}")
        print(f"Processing {config['table']}")
        print('='*50)
        
        if loader.create_table_from_schema(config['dataset'], config['table'], config['schema']):
            files = glob.glob(config['data_pattern'])
            if files:
                latest_file = max(files)
                print(f"Using data file: {latest_file}")
                
                if loader.load_csv_to_table(config['dataset'], config['table'], latest_file):
                    successful_loads += 1
            else:
                print(f"No data files found for pattern: {config['data_pattern']}")
    
    print(f"\n{'='*50}")
    print(f"LOAD SUMMARY: {successful_loads}/{len(table_configs)} tables loaded successfully")
    print('='*50)

if __name__ == "__main__":
    main()
