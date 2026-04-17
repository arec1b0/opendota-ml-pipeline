import pendulum
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'mlops',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'opendota_retrain_pipeline',
    default_args=default_args,
    description='A simple CT pipeline for OpenDota ML pipeline',
    schedule_interval=timedelta(days=1),
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=['mlops', 'ct'],
) as dag:

    # In a real environment, we'd use operators specific to our infrastructure
    # (e.g. KubernetesPodOperator to run a DVC pipeline).
    # Since we are using DVC, we can recreate the pipeline using bash operator.
    
    run_dvc_repro = BashOperator(
        task_id='dvc_reproduce_pipeline',
        bash_command='dvc repro',
    )

    evaluate_model = BashOperator(
        task_id='evaluate_model_performance',
        bash_command='echo "Evaluating... if good, we push model to registry via MLflow scripts"',
    )

    push_to_registry = BashOperator(
        task_id='push_model_to_registry',
        bash_command='echo "Pushing model to MLFlow Model Registry..."',
    )

    run_dvc_repro >> evaluate_model >> push_to_registry
