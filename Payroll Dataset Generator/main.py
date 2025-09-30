import subprocess

def run_generators():
    #Combined script for employees and contracts.
    scripts = [
        "generate_employee_and_contract_details.py",  
        "generate_bonus.py",
        "generate_allowance.py",
        "generate_employee_leave.py",
        "generate_dim_pay_period.py",
        "generate_timesheet_and_roster.py",
        "generate_time_off_in_lieu.py"
    ]
    for script in scripts:
        print(f"Running {script}...")
        subprocess.run(["python", script])

if __name__ == "__main__":
    run_generators()
    print("All datasets generated and saved as CSV files.")
