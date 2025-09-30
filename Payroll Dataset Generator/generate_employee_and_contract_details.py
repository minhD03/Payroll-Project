import pandas as pd
from faker import Faker
import random
from datetime import timedelta, date
from utils import generate_employee_ids

fake = Faker()

def generate_contract_details(employee_ids):
    contract_details = []
    terminated_employee_ids = random.sample(employee_ids, int(len(employee_ids) * 0.05))  #5% of employees terminated.

    for employee_id in employee_ids:
        #Assign employment type and contract type.
        employment_type = random.choice(["Full-time", "Part-time", "Casual"])
        if employment_type == "Casual":
            contract_type = "Casual"
        else:
            contract_type = random.choice(["Permanent", "Fixed-Term"])

        #Generate initial contract dates.
        start_date = fake.date_between_dates(date_start=date(2021, 1, 1), date_end=date.today())
        duration_months = random.choice([6, 12, 24]) if contract_type == "Fixed-Term" else None
        end_date = (
            start_date + timedelta(days=30 * duration_months) if duration_months else None
        )

        #Determine contract status.
        if employee_id in terminated_employee_ids:
            contract_status = "Terminated"
            end_date = fake.date_between_dates(date_start=start_date, date_end=date.today())
        elif end_date and end_date < date.today():
            contract_status = "Expired"
        else:
            contract_status = "Active"

        #Assign job title and payment frequency.
        job_title = random.choice([
            "Nurse", "Software Developer", "Administrative Assistant",
            "IT Support Specialist", "Cleaner", "Security Guard"
        ])

        if job_title in ["Nurse", "Cleaner"]:
            payment_frequency = "Weekly"
        else:
            payment_frequency = random.choice(["Weekly", "Fortnightly", "Monthly"])

        #Generate pay rate.
        pay_rate = round(random.uniform(20, 50), 2)

        #Add current contract details.
        contract_details.append({
            "contract_id": fake.uuid4(),
            "employee_id": employee_id,
            "start_date": start_date,
            "end_date": end_date,
            "pay_rate": pay_rate,
            "job_title": job_title,
            "payment_frequency": payment_frequency,
            "contract_type": contract_type,
            "employment_type": employment_type,
            "contract_status": contract_status,
        })

        #Generate one previous contract for 10% of non-casual employees (excluding terminated employees).
        if employee_id not in terminated_employee_ids and employment_type != "Casual" and random.random() < 0.1:
            generate_previous_contract(contract_details, employee_id, start_date, pay_rate, job_title, employment_type)

    return contract_details


def generate_previous_contract(contract_details, employee_id, current_start_date, current_pay_rate, job_title, employment_type):
    #Generate previous contract start and end dates.
    duration_months = random.choice([6, 12])  #Minimum duration 6 months.
    end_date = current_start_date - timedelta(days=1)
    start_date = end_date - timedelta(days=30 * duration_months)

    #Calculate pay rate decrease.
    pay_rate_decrease = random.choice([0.05, 0.10])  #5% or 10% decrease.
    previous_pay_rate = round(current_pay_rate * (1 - pay_rate_decrease), 2)

    #Determine contract type.
    contract_type = random.choice(["Permanent", "Fixed-Term"]) if employment_type != "Casual" else "Casual"

    #Add previous contract.
    contract_details.append({
        "contract_id": fake.uuid4(),
        "employee_id": employee_id,
        "start_date": start_date,
        "end_date": end_date,
        "pay_rate": previous_pay_rate,
        "job_title": job_title,  #Same as the latest contract.
        "payment_frequency": random.choice(["Weekly", "Fortnightly", "Monthly"]),
        "contract_type": contract_type,
        "employment_type": employment_type,  #Same as the latest contract.
        "contract_status": "Expired",  #All previous contracts must be expired.
    })


def generate_employee_details(employee_ids, contract_details):
    employee_details = []

    #Randomly select 30% of employee_ids to have a middle name.
    employees_with_middle_name = set(random.sample(employee_ids, int(len(employee_ids) * 0.3)))

    for employee_id in employee_ids:
        #Extract contract details for the current employee.
        contracts = [c for c in contract_details if c['employee_id'] == employee_id]
        latest_contract = max(contracts, key=lambda x: x['start_date']) if contracts else None

        #Determine hire_date and termination_date.
        hire_date = latest_contract['start_date'] if latest_contract else None
        termination_date = (
            latest_contract['end_date'] if latest_contract and latest_contract['contract_status'] == "Terminated" else None
        )

        #Set employee status based on latest contract status.
        if latest_contract:
            if latest_contract['contract_status'] == "Active":
                employee_status = "Active"
            else:  # Expired or Terminated
                employee_status = "Inactive"
        else:
            employee_status = "Inactive"  #Default if no contract exists.
        
        #Conditionally generate middle name.
        middle_name = fake.first_name() if employee_id in employees_with_middle_name else None

        #Add employee details.
        employee_details.append({
            "employee_id": employee_id,
            "employee_first_name": fake.first_name(),
            "employee_middle_name": middle_name,
            "employee_last_name": fake.last_name(),
            "employee_gender": random.choice(["Male", "Female"]),
            "employee_location": fake.city(),
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=60),
            "hire_date": hire_date,
            "termination_date": termination_date,
            "employee_status": employee_status,
        })

    return employee_details


if __name__ == "__main__":
    #Generate employee IDs.
    total_employees = 100
    employee_ids = generate_employee_ids(total_employees)

    #Generate contract details.
    contract_details = generate_contract_details(employee_ids)

    #Generate employee details.
    employee_details = generate_employee_details(employee_ids, contract_details)

    #Save to CSV.
    df_contract_details = pd.DataFrame(contract_details)
    df_contract_details.to_csv("contract_details.csv", index=False)
    print("Contract details saved to contract_details.csv")

    df_employee_details = pd.DataFrame(employee_details)
    df_employee_details.to_csv("employee_details.csv", index=False)
    print("Employee details saved to employee_details.csv")
