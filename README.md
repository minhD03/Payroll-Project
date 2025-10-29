# Payroll Project [Live Report Publish](https://app.powerbi.com/view?r=eyJrIjoiMmViZDYzYWUtZjVmMy00NDc4LWI2MDgtOGFlYmJhODg5NDViIiwidCI6IjZhNjhlMmQxLWQ4OGQtNDEyYi1iOTgyLWQ0YWVkNWY1MTcxNiJ9)
This project is a system that helps businesses in tracking the Payroll system. The SQL script transforms raw data into datasets with appropriate format and no conflictions when reading. Then, I used Power BI Dashboard to visualize and draw meaningful insights. These findings will determine actions to either embracing it or reduce it.
For Dataset Generator: [Link](https://github.com/minhD03/Payroll-Dataset-Generator.git)

---

## About Dataset:

The datasets includes 14 files that are in .csv format:
- **Allowance**: Extra payments made to employees within specific periods. There are
two main types: Laundry Allowance and First Aid Allowance.
- **Bonus**: Extra rewards for employees within specific events such as Retention Bonus,
Christmas Bonus, Performance bonus, etc.
- **Combined holiday**: List of holiday plans that were implemented. For example, if the
Christmas falls on Sunday, there will be extra day-offs for the following days as
additional holidays.
- Contract details: Contains information about the employees such as job type, title,
active status, pay rate, etc.
- **Date**: A **manual created** dataset created to help retrieving the chronological time.
- **Employee details**: List of employees along with their personal information.
- **Employee leaves**: List of leaves recorded.
- **Junior pay rates**: Wages for employees within specific age group.

## Project Overview

### Dashboard Preview Screenshot:
These are my dashboard screenshots. Further Report can be view in here: [Report Link](https://github.com/minhD03/Payroll-Project/blob/9531a8b92243f0e47f6c6749846aaf5dfaa170df/Payroll%20Report-%20Nhat%20Minh%20Dang.pdf)

![alt text](https://github.com/minhD03/Payroll-Project/blob/34def8fb7416c1a571bd876d1d7e0f672d19944f/Images/Dashboard%201.png)

![alt text](https://github.com/minhD03/Payroll-Project/blob/34def8fb7416c1a571bd876d1d7e0f672d19944f/Images/Dashboard%202.png)
---

## Data Transformation Process:

![alt text](https://github.com/minhD03/Payroll-Project/blob/686a75198d95fc25bf522e353ad8ec660bc325d0/Images/Medallion%20Architecture.jpg)

In this project, I will use three data schemas: Landing, Staging and Mart. These schemas represent three steps in Medallion Architecture. Medallion architecture is a powerful data design pattern used in modern Lakehouse systems to progressively refine and organize data across three distinct layers—Bronze, Silver and Gold—each representing a step in data quality and usability. At its foundation, the Bronze layer ingests raw, unprocessed data from diverse sources such as CRM, ERP or LOB systems, preserving its original form for traceability and historical analysis. This raw data then flows into the Silver layer, where it undergoes cleaning, validation and enrichment—removing duplicates, standardizing formats, and integrating disparate datasets to create a more coherent and reliable view. Finally, the Gold layer transforms this refined data into business-ready assets through dimensional modelling, aggregation and domain-specific enhancements, making it ideal for executive dashboards, machine learning models and advanced analytics. This tiered approach not only ensures data integrity and governance but also enables modular development, scalability and efficient collaboration across data engineering, analytics, and decision-making teams. By separating concerns and incrementally improving data quality, medallion architecture empowers organizations to build robust, flexible pipelines that support both operational reporting and strategic insights.

Because the Date table was created individually, it was put into the Mart layer. For other files, they were imported into Landing layer.

After importing datasets into SQL Server, I divided the tables into **Dimension Table** and **Fact Table**. In a data warehouse, **Dimension Table** provide descriptive context—like employee details, contract terms or pay rate categories—that help slice and filter data. They’re typically wide and relatively static. **Fact Table**, on the other hand, store measurable events—such as allowances, bonuses, timesheets or rosters—and link to dimensions using surrogate keys. These tables are optimized for aggregations, reporting and analytical queries.

In the SQL script, I started by transforming raw landing data into clean, structured staging tables, selecting key columns across HR, payroll and roster files. Then, I standardized formats, renamed fields and mapped identifiers like employee_code to employee_id. In addition, in the marts layer, I built dimension tables by hashing keys (e.g., employee_pk, contract_pk), converting percentages to multipliers and aggregating pay periods. For fact tables, I joined staging data with dimensions using surrogate keys and date logic, ensuring each record was contextualized by contract, employee and pay period. This layered approach supports robust analytics and executive reporting.

## Dashboard Relationships:
When creating Power Bi Dashboard, these are the relationships that I connected:
| From Table (Column)                  | Relationship Type | To Table (Column)                     |
|-------------------------------------|-------------------|---------------------------------------|
| `dim_date(date_pk)`  | One to Many   |  `fact_allowances (allowance_start_date_fk)`    |
| `dim_employees(employee_pk)`     | One to Many     |    `fact_allowances(employee_fk)`    | 
| `dim_pay_period(pay_period_pk)`| One to Many      | `fact_allowances(pay_period_fk)`         | 
| `dim_date(date_pk)`| One to Many      | `fact_bonuses(bonus_date_fk)`         | 
| `dim_eployees(employee_pk)`      | One to Many     | `fact_bonuses(employee_fk)`      | 
| `dim_pay_period(pay_period_pk)`| One to Many      | `fact_bonuses(pay_period_fk)`         | 
|`dim_employees(employee_pk)`  | One to Many      |      `fact_employee_leaves(employee_fk)`   | 
|  `dim_pay_period(pay_period_pk)` | One to Many      |   `fact_employee_leaves(pay_period_fk)`     | 
| `dim_employees(employee_pk)`     | One to Many     |    `fact_roster(employee_fk)`    | 
|  `dim_pay_period(pay_period_pk)` | One to Many      |   `fact_roster(pay_period_fk)`     | 
| `dim_date(date_pk)`  | One to Many   |  `fact_roster(work_date_fk)`    |
| `dim_employees(employee_pk)`     | One to Many     |    `fact_timesheet(employee_fk)`    | 
| `dim_pay_period(pay_period_pk)`| One to Many      | `fact_timesheet(pay_period_fk)`         | 
| `dim_contract(contract_pk)`| One to Many      | `fact_timesheet(contract_fk)`         |
| `dim_date(date_pk)`| One to Many      | `fact_timehseet(timesheet)_transition_date_fk)`         | 
| `dim_date(date_pk)`| One to Many      | `fact_employee_leaves(leave_start_date_fk)`          | 

# Insights gained:
## 🧑‍💼 Employee Type & Job Title Distribution

- **Employment type balance**: Part-time, Full-time and Casual employees each represent ~33%.
  - ✅ **Positive Insight**: Risk exposure is evenly distributed across contract types.
  - 💡 **Recommendation**: Maintain this equilibrium to support operational flexibility and workforce resilience.

- **Job title concentration**: IT Support Specialist, Security Guard and Software Developer collectively account for 19% of roles.
  - ⚠️ **Risk Indicator**: These roles are payroll-sensitive due to their high representation.
  - 🛠 **Action**: Prioritize payroll audits and contract reviews for these positions to mitigate systemic mismatches.

---

## 📊 Contract Status & Payroll Risk

- **Active contracts dominate**: 70% active, 24% expired, and 6% terminated.
  - ✅ **Positive Insight**: Reflects strong employee retention and effective HR policies.
  - ⚠️ **Risk Indicator**: Expired and terminated contracts may contribute to payroll discrepancies.
  - 🛠 **Action**: Implement automated alerts for contract expirations and reinforce offboarding protocols.

- **Payroll discrepancy**: $5.39M in overpayments vs $34.8K in underpayments.
  - ❌ **Negative Insight**: Overpayments represent a significant financial exposure.
  - 🛠 **Action**: Enforce stricter payroll validation, conduct periodic audits and deploy anomaly detection mechanisms.

---

## 📈 Payroll Trend Analysis (2021–Apr 2025)

- **Post-COVID recovery**: Paid amounts surged post-June 2024, while Mandatory amounts rose modestly.
  - ⚠️ **Risk Indicator**: Disproportionate growth suggests inefficiencies or inflated compensation.
  - 🛠 **Action**: Align paid amounts with mandatory benchmarks and consider performance-based compensation adjustments.

- **2022–2024 fluctuations**: Paid amounts ranged from 0.06M–0.08M; Mandatory amounts from 0.04M–0.05M.
  - 📉 **Cause**: COVID-related disruptions impacted workforce stability and budgeting.
  - 💡 **Recommendation**: Use this period as a baseline for resilience modeling and payroll elasticity planning.

---

## 📃 Contract Type Breakdown

- **Casual contracts dominate**: 50k vs 20k for full-time roles.
  - ⚠️ **Risk Indicator**: Heavy reliance on casual staff may lead to performance volatility.
  - 🛠 **Action**: Diversify workforce strategy and invest in full-time talent pipelines to stabilize operations.

- **Full-time demand post-2025**: Paid amounts for full-time roles increased significantly.
  - ✅ **Positive Insight**: Indicates strategic hiring aligned with peak operational periods.
  - 💡 **Recommendation**: Continue leveraging full-time roles for core functions and scale with part-time/casual staff as needed.

---

## 🧑‍💻 Role-Specific Insights

- **IT Support Specialist**:
  - Predominantly filled by part-time and casual contracts.
  - Demand growth observed only from 2025 onward.
  - ⚠️ **Risk Indicator**: Suggests short-term demand; not a strategic long-term role.
  - 🛠 **Action**: Consider outsourcing or flexible staffing models to manage this function efficiently.

- **Software Developer**:
  - Casual contracts represent nearly half of the workforce in this role.
  - Paid and mandatory amounts are significantly higher than IT Support.
  - ✅ **Positive Insight**: High value contribution despite short-term contracts.
  - 💡 **Recommendation**: Adopt hybrid staffing models — retain core developers full-time and supplement with contractors during high-demand cycles.

---

## 🧑‍💼 Administrative Assistant Role

- **Full-time dominance** with minimal fluctuation in payroll metrics.
  - ✅ **Positive Insight**: Indicates operational stability and high dependency.
  - 💡 **Recommendation**: Treat Administrative Assistants as strategic assets. Invest in retention programs, career development and performance-based incentives.
  - 🛠 **Action**: Prioritize this role in workforce planning to ensure continuity and reduce operational risk.

---

## 👥 Employee-Level Analysis

- **Company-wide hours**: ~30k overtime vs 2.26k undertime over 5 years.
  - ✅ **Positive Insight**: High demand met with generous rewards — nearly 1M bonus cards and 26.5k allowance cards.
  - 💡 **Recommendation**: Maintain balance between workload and incentives to support employee well-being.

- **2025 peak**: Overtime demand spiked to 390 hours in the first four months.
  - ⚠️ **Risk Indicator**: Potential burnout or staffing gaps during peak periods.
  - 🛠 **Action**: Forecast peak seasons and proactively scale staffing or implement flexible scheduling.

---

## 🧑‍💼 Individual Employee Insights Examples

- **Aaron Morales**:
  - Overtime: 20–40 hours; Undertime: 1–3 hours; Regular leave every 2–3 months.
  - ✅ **Positive Insight**: Balanced workload and personal life; consistent contributor.
  - 💡 **Recommendation**: Use Aaron’s profile as a benchmark for sustainable employee engagement.

- **Rober**:
  - Overtime: 84 hours; Undertime: 22 hours; Larger gap between overtime and undertime.
  - ⚠️ **Risk Indicator**: May reflect underutilization or role misalignment.
  - 🛠 **Action**: Reassess role expectations and redistribute tasks to optimize productivity.

- **Eric (minor position)**:
  - Overtime: ~740 hours; Undertime: 0; Only 2 leave events in 5 years.
  - ❌ **Negative Insight**: High workload with minimal rest — risk of burnout or disengagement.
  - 🛠 **Action**: Recognize and reward high-effort employees. Introduce wellness checks, mandatory leave cycles and mental health support.
















