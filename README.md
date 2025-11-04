# 🧩 Vendor Performance Analysis (Company Standard Project)

## 📘 Overview
This project analyzes vendor and procurement performance to identify cost inefficiencies, vendor dependency, and profit optimization opportunities.  
It integrates **SQL, Python, and Power BI** for end-to-end data analysis — from ingestion and cleaning to dashboard visualization.

---

## ⚙️ Tech Stack
- **Language:** Python (Pandas, NumPy, Matplotlib, Seaborn)
- **Database:** MySQL (SQLAlchemy, PyMySQL)
- **Visualization:** Power BI
- **Reporting:** ReportLab (PDF generation)
- **Tools:** Jupyter Notebook, VS Code

---

## 📂 Project Workflow
1. **Data Ingestion:** Loaded 6 raw datasets (sales, purchases, inventory, vendor invoices, pricing) into MySQL using Python ETL scripts.  
2. **Data Cleaning:** Handled missing values, duplicates, and schema mismatches across large datasets (>1M records).  
3. **Exploratory Data Analysis (EDA):** Identified trends in vendor performance, pricing, and sales contribution.  
4. **Hypothesis Testing:** Applied t-test and ANOVA to analyze bulk purchase impact on unit cost and profitability.  
5. **Dashboard & KPIs:** Designed a Power BI dashboard to visualize metrics such as:  
   - Top-performing vendors by revenue and profit  
   - Inventory turnover & vendor dependency ratio  
   - Freight cost contribution and purchase-to-sales ratio  
6. **Reporting:** Automated PDF summaries for management insights.

---

## 📊 Key Insights
- Identified **underperforming vendors** needing pricing or promotional adjustments.  
- Found that **bulk purchasing reduced unit costs** significantly (p < 0.05).  
- Improved vendor selection efficiency by **~35%** using KPI-based insights.  
- Highlighted top 5 vendors contributing to 60% of total sales.  

---

## 🧠 Skills Demonstrated
- SQL joins, aggregation, and window functions  
- Python data analysis (EDA, visualization, hypothesis testing)  
- Power BI dashboard design & storytelling with data  
- Data pipeline automation (ETL + reporting)

---

## 🗃️ Repository Structure
📁 Vendor-Performance-Analysis/
│
├── data/ # Raw CSV datasets
├── notebooks/ # Jupyter notebooks for analysis
├── scripts/
│ ├── db_ingest.ipynb # ETL ingestion to MySQL
│ ├── ingest_load_data_infile.py
│ ├── vendor_summary.sql # SQL summary queries
│
├── dashboard/ # Power BI .pbix file
├── reports/ # Auto-generated PDF reports
│
├── output/ # Cleaned / merged CSVs
├── README.md # Project documentation

