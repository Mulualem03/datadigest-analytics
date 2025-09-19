from google.cloud import bigquery
import json

def main():
    client = bigquery.Client(project='datadigest-analytics-2025')
    
    # Load updated schema
    with open('config/schemas/raw_web_analytics.json', 'r') as f:
        schema_config = json.load(f)
    
    schema = []
    for field in schema_config:
        field_type = getattr(bigquery.enums.SqlTypeNames, field['type'])
        mode = field['mode']
        schema.append(bigquery.SchemaField(field['name'], field_type, mode=mode))
    
    # Create table with correct schema
    table_ref = client.dataset('datadigest_raw').table('web_analytics')
    table = bigquery.Table(table_ref, schema=schema)
    
    try:
        table = client.create_table(table)
        print(f"Created table with {len(schema)} columns")
        
        # Load data
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=False,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
        )
        
        import glob
        files = glob.glob('data/raw/web_analytics_*.csv')
        latest_file = max(files)
        
        with open(latest_file, 'rb') as source_file:
            job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
        
        job.result()
        
        table = client.get_table(table_ref)
        print(f"Successfully loaded {table.num_rows} rows to web_analytics table")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
