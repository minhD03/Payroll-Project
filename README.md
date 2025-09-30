# Payroll-Project

This project generates mock payroll-related datasets for a multi-industry Australian business. The data includes employee details, bonuses, allowances, time off in lieu and history records, while maintaining data integrity and realistic relationships. From these generated data, I will transform the data using SSMS and run a SQL script to transform the data and finally display as Power BI Dashboard.

---

## Project Overview

### Dashboard Preview Screenshot:

![alt text](https://github.com/minhD03/Payroll-Project/blob/34def8fb7416c1a571bd876d1d7e0f672d19944f/Images/Dashboard%201.png)

![alt text](https://github.com/minhD03/Payroll-Project/blob/34def8fb7416c1a571bd876d1d7e0f672d19944f/Images/Dashboard%202.png)

### Files contained:

1. **`utils.py`**
   - Contains shared utilities and constants (e.g., minimum wage data, employee ID generation).
   - Must be imported by all other scripts.

2. **`generate_employee_details.py`**
   - Generates the foundational `employee_details.csv` file.
   - Other datasets reference `employee_id` from this file.
   - Must be run first to ensure data integrity.

3. **`generate_bonus.py`**
   - Generates `bonus.csv`, referencing `employee_id` from `employee_details.csv`.

4. **`generate_allowance.py`**
   - Generates `allowance.csv`, referencing `employee_id` from `employee_details.csv`.

5. **`generate_time_off_in_lieu.py`**
   - Generates `time_off_in_lieu.csv`, referencing `employee_id` from `employee_details.csv`.

6. **`generate_history_table.py`**
   - Generates `history_table.csv`, referencing `employee_id` from `employee_details.csv`.

7. **`main.py`**
   - Automates the execution of all scripts in the correct order.
   - Ensures `utils.py` and `generate_employee_details.py` are executed first.

---

## Prerequisites

1. **Python Version:** Ensure you have Python 3.8 or higher installed.
2. **Dependencies:** Install required libraries by running:
   ```bash
   pip install faker pandas
   ```

---

## Instructions to Run the Project

Follow these steps to run the project and generate all datasets:

### 1. Run `utils.py` to Prepare Constants
This step ensures that all shared utilities and constants (e.g., minimum wage data) are correctly initialized.
   ```bash
   python utils.py
   ```

### 2. Run `main.py` to Generate All Datasets
The `main.py` script will automatically execute all data generation scripts in the correct order:
   ```bash
   python main.py
   ```

### 3. Output Files
After running the scripts, the following CSV files will be generated in the project directory:
   - `employee_details.csv`
   - `bonus.csv`
   - `allowance.csv`
   - `time_off_in_lieu.csv`
   - `history_table.csv`
   - `roster.csv`
   - `timesheet.csv`

### 4. Validation
Verify the generated files to ensure all datasets adhere to the predefined rules and relationships.

---

## Troubleshooting

- **Issue:** Missing `employee_id` in other datasets.
  - **Solution:** Ensure `generate_employee_details.py` is executed before any other script.

- **Issue:** Missing dependencies.
  - **Solution:** Run `pip install faker pandas` to install the required libraries.

---
#

