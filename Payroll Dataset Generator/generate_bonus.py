import pandas as pd
from faker import Faker
import random
from datetime import timedelta, date, datetime

fake = Faker()

def safe_date_conversion(date_value, fallback=None):
    """
    Safely convert a date string to a datetime.date object.
    """
    try:
        if isinstance(date_value, str):
            return datetime.strptime(date_value, "%Y-%m-%d").date()
        elif isinstance(date_value, (datetime, date)):
            return date_value
        else:
            return fallback
    except Exception:
        return fallback

def generate_bonus(employee_details, contract_details):
    bonus = []
    today = date.today()

    for employee in employee_details:
        employee_id = employee["employee_id"]
        termination_date = safe_date_conversion(employee.get("termination_date"), None)

        #Get contract details for the current employee.
        contracts = [c for c in contract_details if c["employee_id"] == employee_id]
        if not contracts:
            continue

        for contract in contracts:
            start_date = safe_date_conversion(contract.get("start_date"), None)
            end_date = safe_date_conversion(contract.get("end_date"), today)

            #Override end_date with termination_date if it exists.
            if termination_date:
                end_date = min(end_date, termination_date)

            #Skip invalid contracts.
            if not start_date or start_date > today or end_date < start_date:
                continue

            #Generate Christmas Bonus for each year in the contract period.
            current_year = start_date.year
            while current_year <= end_date.year and current_year <= today.year:
                christmas_bonus_date = date(current_year, 12, 25)
                if start_date <= christmas_bonus_date <= end_date and christmas_bonus_date <= today:
                    bonus.append({
                        "bonus_id": fake.uuid4(),
                        "employee_id": employee_id,
                        "bonus_type": "Christmas Bonus",
                        "bonus_amount": round(random.uniform(200, 500), 2),
                        "bonus_date": christmas_bonus_date.strftime("%Y-%m-%d"),
                    })
                current_year += 1

            #Generate Performance Bonus 1-3 times per year within the contract period.
            for year in range(start_date.year, min(end_date.year, today.year) + 1):
                num_bonuses = random.randint(1, 3)  #Random 1 to 3 performance bonuses per year.
                for _ in range(num_bonuses):
                    bonus_date = fake.date_between(
                        start_date=max(start_date, date(year, 1, 1)),
                        end_date=min(end_date, date(year, 12, 31))
                    )
                    if bonus_date <= today:  #Exclude future dates.
                        bonus.append({
                            "bonus_id": fake.uuid4(),
                            "employee_id": employee_id,
                            "bonus_type": "Performance Bonus",
                            "bonus_amount": round(random.uniform(500, 2000), 2),
                            "bonus_date": bonus_date.strftime("%Y-%m-%d"),
                        })

            #Generate Retention Bonus for employees with at least 1 year of employment.
            retention_bonus_date = start_date + timedelta(days=365)
            if retention_bonus_date <= end_date and retention_bonus_date <= today:
                bonus.append({
                    "bonus_id": fake.uuid4(),
                    "employee_id": employee_id,
                    "bonus_type": "Retention Bonus",
                    "bonus_amount": round(random.uniform(1000, 3000), 2),
                    "bonus_date": retention_bonus_date.strftime("%Y-%m-%d"),
                })

            #Generate Sign-On Bonus for employees whose contracts started this year.
            if start_date.year == today.year:
                sign_on_bonus_date = start_date + timedelta(days=30)  #Issued 1 month after start date.
                if sign_on_bonus_date <= today:
                    bonus.append({
                        "bonus_id": fake.uuid4(),
                        "employee_id": employee_id,
                        "bonus_type": "Sign-On Bonus",
                        "bonus_amount": round(random.uniform(500, 1500), 2),
                        "bonus_date": sign_on_bonus_date.strftime("%Y-%m-%d"),
                    })

    return bonus


if __name__ == "__main__":
    #Load employee_details and contract_details from CSV files.
    employee_details = pd.read_csv("employee_details.csv").to_dict("records")
    contract_details = pd.read_csv("contract_details.csv").to_dict("records")

    #Convert termination_date and contract dates to datetime.date.
    for emp in employee_details:
        emp["termination_date"] = safe_date_conversion(emp.get("termination_date"), None)
    for contract in contract_details:
        contract["start_date"] = safe_date_conversion(contract.get("start_date"), None)
        contract["end_date"] = safe_date_conversion(contract.get("end_date"), None)

    #Generate bonus data.
    bonus_data = generate_bonus(employee_details, contract_details)

    #Save to CSV.
    pd.DataFrame(bonus_data).to_csv("bonus.csv", index=False)
    print("Bonus data saved to bonus.csv")
