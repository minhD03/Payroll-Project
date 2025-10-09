# Payroll Project
This project is a system that helps businesses in tracking the Payroll system. The SQL script transforms raw data into datasets with appropriate format and no conflictions when reading. Then, I used Power BI Dashboard to visualize and draw meaningful insights. These findings will determine actions to either embracing it or reduce it.

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











