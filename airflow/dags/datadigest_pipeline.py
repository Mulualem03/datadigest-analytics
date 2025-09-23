from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

default_args = {
    'owner': 'datadigest',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'datadigest_pipeline',
    default_args=default_args,
    description='DataDigest: Airbyte -> dbt -> Tests',
    schedule='0 6 * * *',  # Changed from schedule_interval to schedule
    catchup=False,
) as dag:

    # Task 1: Run dbt transformations
    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd ~/datadigest-analytics/datadigest_transform && source ~/datadigest-analytics/dbt_venv/bin/activate && dbt run',
    )

    # Task 2: Run dbt tests
    test_dbt = BashOperator(
        task_id='run_dbt_tests',
        bash_command='cd ~/datadigest-analytics/datadigest_transform && source ~/datadigest-analytics/dbt_venv/bin/activate && dbt test',
    )

    # Task 3: Generate docs
    docs_dbt = BashOperator(
        task_id='generate_docs',
        bash_command='cd ~/datadigest-analytics/datadigest_transform && source ~/datadigest-analytics/dbt_venv/bin/activate && dbt docs generate',
    )

    # Dependencies: run -> test -> docs
    run_dbt >> test_dbt >> docs_dbt
