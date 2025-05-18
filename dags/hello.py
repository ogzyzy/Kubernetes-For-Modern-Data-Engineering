from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'dominikzygarski.com',
    'start_date': datetime(2025, 5, 18),
    'catchup': False
}

dag = DAG(
    'hello_world',
    default_args=default_args,
    schedule=timedelta(days=1)
)

t1 = BashOperator(
    task_id='hello_world',
    bash_command='echo "Hello World"',
    dag=dag
)

t2 = BashOperator(
    task_id='hello_dml',
    bash_command='echo "Hello Dominik"',
    dag=dag
)

t1 >> t2 