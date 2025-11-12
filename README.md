# **Vendor Performance Analysis | Retail Inventory & Sales**

---

## **Executive Summary**
Analyzed vendor efficiency and profitability to guide strategic purchasing, pricing, and inventory decisions.  
Built a complete analytics pipeline using **SQL**, **Python**, and **Power BI** to identify underperforming brands, optimize inventory turnover, and evaluate vendor profitability through data-driven insights.

---

## **Business Problem & Research Questions**
Retail companies often face challenges such as inefficient vendor relationships, slow-moving inventory, and inconsistent profit margins.  
This project aimed to:

- Assess vendor performance and contribution to total sales  
- Detect inefficiencies in bulk purchasing and inventory turnover  
- Validate profitability differences across vendors using statistical testing  

---

## **Methodology**
1. **Data Collection & Cleaning:**  
   - Integrated multiple CSV datasets (sales, inventory, vendors)  
   - Removed invalid records (zero sales, profit, or margin)  
   - Created vendor-level summary tables using SQL  

2. **Exploratory Data Analysis (EDA):**  
   - Analyzed profit margins, freight costs, and turnover ratios  
   - Identified loss-making sales and slow-moving stock  

3. **Statistical Analysis:**  
   - Performed hypothesis testing (t-tests) to compare vendor profitability  

4. **Visualization & Reporting:**  
   - Developed an interactive **Power BI dashboard** showcasing key vendor KPIs  

---

## **Dashboard Preview**
Power BI dashboard visualizes vendor-wise sales, margins, inventory turnover, and cost savings.

![Vendor Performance Dashboard](images/dashboard.png)

---

## **Skills**
**Technical:** SQL, Python, Power BI  
**Libraries:** Pandas, NumPy, Matplotlib, Seaborn, SciPy  
**Core Competencies:** Data Cleaning, KPI Analysis, Hypothesis Testing, Dashboarding, Inventory Optimization  

---

## **Results and Business Recommendations**
- **Top Vendors:** 10 vendors accounted for **65.69%** of total purchases — risk of over-reliance  
- **Bulk Purchases:** Achieved **72% cost savings** per unit in large orders  
- **Profitability Variation:** Statistically significant difference between vendor strategies  
- **Inventory Insights:** Detected **$2.71M** in unsold inventory and 198 brands suitable for promotions  

**Recommendations:**
- Diversify vendor base to reduce dependency risk  
- Reprice or promote slow-moving, high-margin brands  
- Optimize bulk order quantities to maximize savings  
- Strengthen marketing for underperforming vendors  

---

## **Next Steps**
- Automate ETL and vendor performance reporting pipeline  
- Integrate real-time vendor scorecards in Power BI  
- Extend analysis to include seasonal demand and vendor reliability metrics  

---

##  Project Structure
```
vendor-performance-analysis/
│
├── README.md
├── .gitignore
├── requirements.txt
├── Vendor Performance Report.pdf
│
├── notebooks/
│ ├── Exploratory data anlaysis.ipynb
│ └── Vendor Performance Analysis.ipynb
│
├── scripts/
│ ├── ingest_db.py
│ └── vendor_sales_summary.py
│
└── dashboard/
└── vendor_performance_dashboard.pbix
```

## **Author & Contact**
**Author:** Mohd Moinuddin  
**Email:** moinuddinn012@gmail.com
