import pandas as pd
from faker import Faker
import random
from utils import fake

def generate_time_off_in_lieu(employee_details):
    time_off_in_lieu = []
    for employee in employee_details:
        employee_id = employee["employee_id"]
        overtime_date = fake.date_this_year()
        time_off_in_lieu.append({
            "toil_id": fake.uuid4(),
            "employee_id": employee_id,
            "overtime_date": overtime_date,
            "toil_hours_accrued": random.randint(1, 8),
            "toil_usage_date": fake.date_between(start_date=overtime_date, end_date="+30d"),
        })
    return time_off_in_lieu

if __name__ == "__main__":
    employee_details = pd.read_csv("employee_details.csv").to_dict("records")
    time_off_in_lieu = generate_time_off_in_lieu(employee_details)
    pd.DataFrame(time_off_in_lieu).to_csv("time_off_in_lieu.csv", index=False)
