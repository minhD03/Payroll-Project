import pandas as pd
from faker import Faker
import random
from datetime import timedelta, date, datetime
from constants.public_holidays import PUBLIC_HOLIDAYS

fake = Faker()

def generate_employee_leave(employee_details, contract_details):
    employee_leave = []
    today = date.today()

    #Map employment type to leave hours.
    leave_hours_mapping = {"Full-time": 7.6, "Part-time": 3.8, "Casual": 4}
    casual_unpaid_limit = 16  #2 days in hours for casual employees.

    for employee in employee_details:
        employee_id = employee["employee_id"]
        termination_date = (
            datetime.strptime(employee["termination_date"], "%Y-%m-%d").date()
            if pd.notna(employee["termination_date"])
            else None
        )
        employee_contracts = [
            {
                **c,
                "start_date": datetime.strptime(c["start_date"], "%Y-%m-%d").date(),
                "end_date": (
                    datetime.strptime(c["end_date"], "%Y-%m-%d").date()
                    if pd.notna(c["end_date"])
                    else None
                ),
            }
            for c in contract_details
            if c["employee_id"] == employee_id
        ]

        for contract in employee_contracts:
            start_date = contract["start_date"]
            end_date = min(contract["end_date"] or today, termination_date or today)
            employment_type = contract["employment_type"]

            #Skip if the employee is terminated before the contract starts.
            if end_date < start_date:
                continue

            #Calculate pro-rata leave entitlements based on formulas.
            contract_duration_days = (end_date - start_date).days
            weekly_hours = leave_hours_mapping[employment_type]
            annual_leave_entitlement = (weekly_hours / 38) * 152 * (contract_duration_days / 365)
            sick_leave_entitlement = (weekly_hours * 52) / 26 * (contract_duration_days / 365)

            #Convert leave entitlements to days (rounded down).
            max_annual_leaves = int(annual_leave_entitlement / weekly_hours)
            max_sick_leaves = int(sick_leave_entitlement / weekly_hours)

            #Track number of leaves per type per year.
            annual_leaves_taken = 0
            sick_leaves_taken = 0
            unpaid_leaves_taken = 0

            #Annual Leave (Not for Casual Employees).
            if employment_type != "Casual":
                max_annual_leaves = random.randint(0, max_annual_leaves)  #Randomize leaves taken.
                while annual_leaves_taken < max_annual_leaves:
                    leave_start_date = fake.date_between(start_date=start_date, end_date=end_date)
                    leave_end_date = leave_start_date

                    #Avoid public holidays for leave start.
                    while leave_start_date.weekday() >= 5 or leave_start_date in PUBLIC_HOLIDAYS.get(leave_start_date.year, []):
                        leave_start_date += timedelta(days=1)
                        if leave_start_date > today:  #Ensure it does not exceed today.
                            break

                    if leave_start_date > today:
                        break

                    leave_end_date = leave_start_date
                    annual_leaves_taken += 1

                    employee_leave.append({
                        "leave_id": fake.uuid4(),
                        "employee_id": employee_id,
                        "leave_type": "Annual Leave",
                        "leave_start_date": leave_start_date,
                        "leave_end_date": leave_end_date,
                        "leave_hours": weekly_hours,
                    })

            #Sick and Carer's Leave (Not for Casual Employees).
            if employment_type != "Casual":
                max_sick_leaves = random.randint(0, max_sick_leaves)  #Randomize leaves taken.
                while sick_leaves_taken < max_sick_leaves:
                    leave_start_date = fake.date_between(start_date=start_date, end_date=end_date)
                    leave_end_date = leave_start_date

                    #Avoid public holidays for leave start.
                    while leave_start_date.weekday() >= 5 or leave_start_date in PUBLIC_HOLIDAYS.get(leave_start_date.year, []):
                        leave_start_date += timedelta(days=1)
                        if leave_start_date > today:  #Ensure it does not exceed today.
                            break

                    if leave_start_date > today:
                        break

                    leave_end_date = leave_start_date
                    sick_leaves_taken += 1

                    employee_leave.append({
                        "leave_id": fake.uuid4(),
                        "employee_id": employee_id,
                        "leave_type": "Sick and Carer's Leave",
                        "leave_start_date": leave_start_date,
                        "leave_end_date": leave_end_date,
                        "leave_hours": weekly_hours,
                    })

            #Unpaid Leave (Only for Casual Employees or if Randomly Chosen).
            if employment_type == "Casual" or (employment_type != "Casual" and random.random() < 0.1):
                while unpaid_leaves_taken < 2:  #Maximum 2 days for casual.
                    leave_start_date = fake.date_between(start_date=start_date, end_date=end_date)
                    leave_end_date = leave_start_date

                    #Avoid public holidays for leave start.
                    while leave_start_date.weekday() >= 5 or leave_start_date in PUBLIC_HOLIDAYS.get(leave_start_date.year, []):
                        leave_start_date += timedelta(days=1)
                        if leave_start_date > today:  #Ensure it does not exceed today.
                            break

                    if leave_start_date > today:
                        break

                    leave_end_date = leave_start_date
                    unpaid_leaves_taken += 1

                    employee_leave.append({
                        "leave_id": fake.uuid4(),
                        "employee_id": employee_id,
                        "leave_type": "Unpaid Leave",
                        "leave_start_date": leave_start_date,
                        "leave_end_date": leave_end_date,
                        "leave_hours": weekly_hours,
                    })

    return employee_leave


if __name__ == "__main__":
    #Load employee_details and contract_details using relative paths.
    employee_details = pd.read_csv("./employee_details.csv").to_dict(orient="records")
    contract_details = pd.read_csv("./contract_details.csv").to_dict(orient="records")

    #Generate employee leave.
    employee_leave = generate_employee_leave(employee_details, contract_details)

    #Save to CSV.
    df_employee_leave = pd.DataFrame(employee_leave)
    df_employee_leave.to_csv("./employee_leave.csv", index=False)
    print("Employee leave saved to employee_leave.csv")
