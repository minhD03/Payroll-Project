import pandas as pd
from faker import Faker
import random
from datetime import timedelta, date, datetime

fake = Faker()

def safe_date_conversion(date_value, fallback=None):
    """
    Safely convert a date string to a datetime.date object.
    If the value is invalid or None, return the fallback date.
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

def generate_allowance(employee_details, contract_details):
    allowance = []
    today = date.today()

    #Map allowance amounts.
    ALLOWANCE_RATES = {
        "First Aid Allowance": 19.76,  #Fixed weekly rate.
        "Laundry Allowance": 1.49      #Fixed weekly rate.
    }

    #Process allowances for employees
    for employee in employee_details:
        employee_id = employee["employee_id"]
        termination_date = safe_date_conversion(employee.get("termination_date"), None)

        #Get contract details for the current employee.
        contracts = [c for c in contract_details if c["employee_id"] == employee_id]
        if not contracts:
            continue  #Skip employees without contracts.

        for contract in contracts:
            start_date = safe_date_conversion(contract.get("start_date"), None)
            end_date = safe_date_conversion(contract.get("end_date"), today)
            job_title = contract.get("job_title")

            #Check for termination_date overriding end_date.
            if termination_date:
                end_date = min(end_date, termination_date)

            #Ensure allowance dates do not exceed today.
            end_date = min(end_date, today)

            #Skip invalid contract dates.
            if not start_date or start_date > today:
                continue
            if not end_date or end_date < start_date:
                continue

            #Determine allowance type and amount.
            if job_title == "Nurse":
                allowance_type = "First Aid Allowance"
                allowance_amount = ALLOWANCE_RATES["First Aid Allowance"]
            elif job_title == "Cleaner":
                allowance_type = "Laundry Allowance"
                allowance_amount = ALLOWANCE_RATES["Laundry Allowance"]
            else:
                continue  #Skip employees without relevant allowances.

            #Generate allowances starting 1 week after the contract start date.
            allowance_start_date = start_date + timedelta(days=7)
            current_date = allowance_start_date

            while current_date <= end_date:
                allowance_end_date = current_date + timedelta(days=6)  #Allowance valid for 1 week.

                #Ensure the allowance start and end dates do not exceed today.
                if current_date > today:
                    break
                if allowance_end_date > today:
                    allowance_end_date = today

                #Add allowance record.
                allowance.append({
                    "allowance_id": fake.uuid4(),
                    "employee_id": employee_id,
                    "allowance_type": allowance_type,
                    "allowance_amount": round(allowance_amount, 2),
                    "allowance_start_date": current_date.strftime("%Y-%m-%d"),
                    "allowance_end_date": allowance_end_date.strftime("%Y-%m-%d"),
                })

                #Move to the next weekly period.
                current_date += timedelta(weeks=1)

    return allowance


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

    # Generate allowance data.
    allowance_data = generate_allowance(employee_details, contract_details)

    #Save to CSV.
    pd.DataFrame(allowance_data).to_csv("allowance.csv", index=False)
    print("Allowance data saved to allowance.csv")
