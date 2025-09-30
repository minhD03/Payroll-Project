import pandas as pd
from faker import Faker
from datetime import datetime, timedelta, date
import random
from constants.public_holidays import PUBLIC_HOLIDAYS
from constants.time_frames import TIME_FRAMES
from constants.job_title_services import job_title_services

fake = Faker()


def safe_date_conversion(date_value, fallback):
    """
    Safely convert a date string to a datetime.date object.
    If the value is invalid or None, return the fallback date.
    """
    try:
        if isinstance(date_value, str):
            return datetime.strptime(date_value, "%Y-%m-%d").date()
        elif isinstance(date_value, datetime):
            return date_value.date()
        elif isinstance(date_value, date):
            return date_value
        else:
            return fallback
    except Exception:
        return fallback


def calculate_adjusted_hours(employment_type, base_hours):
    """
    Calculate adjusted hours for overtime or undertime based on employment type.
    """
    adjustment = 0
    is_overtime = random.random() < 0.3  #30% chance of overtime.
    is_undertime = random.random() < 0.1  #10% chance of undertime (except Casual).

    if is_overtime:
        if employment_type == "Full-time":
            adjustment = random.choice([1, 2, 3, 4])  #Exactly 1-4 hours overtime.
        elif employment_type == "Part-time":
            adjustment = random.choice([1, 2])  #Exactly 1-2 hours overtime.
        elif employment_type == "Casual":
            adjustment = random.choice([1, 2, 3, 4])  #Exactly 1-4 hours overtime.

    elif is_undertime and employment_type != "Casual":
        if employment_type == "Full-time":
            adjustment = -random.choice([1, 2])  #Exactly 1-2 hours undertime.
        elif employment_type == "Part-time":
            adjustment = -1  #Exactly 1 hour undertime.

    return base_hours + adjustment


def generate_timesheet_and_roster(employee_details, contract_details, employee_leave, dim_pay_period):
    timesheet = []
    roster = []

    #Convert dim_pay_period to a DataFrame.
    dim_pay_period_df = pd.DataFrame(dim_pay_period)
    dim_pay_period_df["period_start_date"] = pd.to_datetime(dim_pay_period_df["period_start_date"]).dt.date
    dim_pay_period_df["period_end_date"] = pd.to_datetime(dim_pay_period_df["period_end_date"]).dt.date

    today = date.today()

    #Preprocess leave days into a lookup dictionary.
    leave_days = {}
    for leave in employee_leave:
        employee_id = leave["employee_id"]
        leave_date = safe_date_conversion(leave["leave_start_date"], None)
        if leave_date:
            if employee_id not in leave_days:
                leave_days[employee_id] = set()
            leave_days[employee_id].add(leave_date)

    for employee in employee_details:
        #Fetch and sanitize contract data.
        employee_contracts = [
            {
                **c,
                "start_date": safe_date_conversion(c.get("start_date"), today),
                "end_date": safe_date_conversion(c.get("end_date"), None),
            }
            for c in contract_details if c["employee_id"] == employee["employee_id"]
        ]

        if not employee_contracts:
            continue

        latest_contract = max(employee_contracts, key=lambda x: x["start_date"])
        start_date = latest_contract["start_date"]

        #Sanitize termination_date and end_date.
        contract_end_date = safe_date_conversion(latest_contract.get("end_date"), None)
        termination_date = safe_date_conversion(employee.get("termination_date"), today)

        #Calculate final end_date.
        if contract_end_date is None:
            end_date = termination_date
        else:
            end_date = min(contract_end_date, termination_date)

        employment_type = latest_contract["employment_type"]
        current_date = start_date

        while current_date <= end_date:
            #Skip weekends, public holidays, and leave days.
            if (current_date.weekday() >= 5 or
                current_date in PUBLIC_HOLIDAYS.get(current_date.year, []) or
                current_date in leave_days.get(employee["employee_id"], set())):
                current_date += timedelta(days=1)
                continue

            #Base working hours.
            if employment_type == "Casual":
                base_hours = 4  # Fixed for casual
            elif employment_type == "Part-time":
                base_hours = 3.8
            else:  #Full-time.
                base_hours = 7.6

            #Calculate adjusted hours for timesheet.
            adjusted_hours = calculate_adjusted_hours(employment_type, base_hours)

            #Generate start and end times.
            start_hour = random.randint(8, 11)
            start_minute = random.randint(0, 59)
            start_time = datetime.strptime(f"{start_hour:02}:{start_minute:02}:00", "%H:%M:%S").time()
            end_time = (datetime.combine(date.min, start_time) + timedelta(hours=adjusted_hours)).time()

            #Append to timesheet with adjusted hours.
            timesheet.append({
                "timesheet_id": fake.uuid4(),
                "employee_code": employee["employee_id"],
                "timesheet_transaction_date": current_date.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M:%S"),
                "end_time": end_time.strftime("%H:%M:%S"),
                "timesheet_transaction_hours": round(adjusted_hours, 2),
                "pay_period_id": None  #Placeholder for pay period ID.
            })

            #Generate accurate roster hours.
            shift_name = f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}"
            roster.append({
                "roster_id": fake.uuid4(),
                "employee_id": employee["employee_id"],
                "shift": shift_name,
                "hours": round(base_hours, 2),  #Accurate base hours for roster.
                "work_date": current_date.strftime("%Y-%m-%d"),
                "services": random.choice(job_title_services.get(latest_contract["job_title"], ["General Duties"])),
                "location": employee["employee_location"],
                "pay_period_id": None  #Placeholder for pay period ID.
            })

            current_date += timedelta(days=1)

    #Attach pay_period_id for each entry.
    for entry in timesheet + roster:
        transaction_date = datetime.strptime(entry["work_date" if "work_date" in entry else "timesheet_transaction_date"], "%Y-%m-%d").date()
        employee_id = entry["employee_code" if "employee_code" in entry else "employee_id"]

        #Fetch payment frequency of the employee.
        payment_frequency = next(
            (contract["payment_frequency"] for contract in contract_details if contract["employee_id"] == employee_id),
            None
        )

        #Match dim_pay_period based on transaction_date and payment_frequency.
        pay_period_row = dim_pay_period_df[
            (dim_pay_period_df["period_start_date"] <= transaction_date) &
            (dim_pay_period_df["period_end_date"] >= transaction_date) &
            (dim_pay_period_df["frequency"] == payment_frequency)
        ]

        if not pay_period_row.empty:
            entry["pay_period_id"] = pay_period_row["pay_period_id"].values[0]

    return timesheet, roster


if __name__ == "__main__":
    #Load input datasets.
    employee_details = pd.read_csv("employee_details.csv").to_dict("records")
    contract_details = pd.read_csv("contract_details.csv").to_dict("records")
    employee_leave = pd.read_csv("employee_leave.csv").to_dict("records")
    dim_pay_period = pd.read_csv("dim_pay_period.csv").to_dict("records")

    #Generate timesheet and roster.
    timesheet_data, roster_data = generate_timesheet_and_roster(employee_details, contract_details, employee_leave, dim_pay_period)

    #Save to CSV.
    pd.DataFrame(timesheet_data).to_csv("timesheet.csv", index=False)
    print("Timesheet data saved to timesheet.csv")

    pd.DataFrame(roster_data).to_csv("roster.csv", index=False)
    print("Roster data saved to roster.csv")
