"""This module contains creates a DAG using Python and explores
basic components of Airflow such as timings and task dependencies."""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago


# Declares the DAG owner
args = {"owner": "jtardelli", "start_date": days_ago(1)}

# DAG declaration. It contains the time to start the DAG, the
# interval and the DAG id.
with DAG(
    dag_id="hello_worrd",
    default_args=args,
    schedule_interval="0 5 * * *",  # minute, hour, day, month, and week day
) as dag:

    # Define BashOperator to print words
    # BashOperator is an AirFlow operator to run Linux commands
    print_hello = BashOperator(task_id="print_hello", bash_command="echo Hello")

    print_world = BashOperator(task_id="print_world", bash_command="echo World")

    # Define the bitwise operator to indicate the task dependency
    print_hello >> print_world

if __name__ == "__main__":
    dag.cli()
