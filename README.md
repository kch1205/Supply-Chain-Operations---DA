# Customer, Product, and Profitability Performance Analysis in Supply Chain Operations

## 1. Project Overview

This project analyzes customer, product, and profitability performance in supply chain operations using Python, Pandas, Streamlit, and Power BI.

The objective is to move beyond revenue-focused reporting and understand how profitability varies across customers, products, categories, markets, and regions. The project combines exploratory data analysis, financial KPI calculations, and interactive dashboards to support data-driven business decisions.

## 2. Problem Statement

Supply chain businesses may generate high sales without achieving proportionate profit. Discounts, customer-level differences, product margins, and regional performance can influence overall profitability.

This project addresses the need for better visibility into:

- Customer-level sales and profitability.
- Product and category profit margins.
- Discount patterns and profitability.
- Market and regional performance.
- Transaction-level losses and profit concentration.

## 3. Project Objectives

- Analyze gross sales, net sales, discounts, total profit, and profit margins.
- Identify high-value and low-profit customers.
- Evaluate product and category profitability.
- Investigate discount-rate patterns and their association with profitability.
- Compare performance across markets, countries, and regions.
- Examine shipping modes and delivery performance.
- Build interactive dashboards using Streamlit and Power BI.

## 4. Dataset Overview

The project uses a supply chain transactional dataset containing **180,519 records and 42 columns**.

Important fields include:

- Sales and Order Item Total
- Order Item Discount and Order Item Discount Rate
- Order Profit Per Order
- Customer Id and Customer Segment
- Product Name and Category Name
- Market, Order Region, and Order Country
- Shipping Mode and delivery performance fields

The cleaned dataset is used for analysis across the project's notebooks and dashboard.

## 5. Technologies Used

- **Python** — data analysis and processing
- **Pandas and NumPy** — data manipulation and calculations
- **Matplotlib and Plotly** — data visualization
- **Jupyter Notebook** — exploratory data analysis
- **Streamlit** — interactive web dashboard
- **Power BI** — business intelligence reporting
- **GitHub** — project version control and documentation

## 6. Project Structure

```text
supply-chain-profitability-analysis/
├── data/
│   └── processed/
│       └── apl_logistics_cleaned.csv
├── notebooks/
│   ├── 1_Data_understanding.ipynb
│   ├── 2_Data_Cleaning.ipynb
│   ├── 3_Revenue_Profit_Analysis.ipynb
│   ├── 4_Customer_Analysis.ipynb
│   ├── 5_Product_Category_Analysis.ipynb
│   ├── 6_Discount_Impact_Analysis.ipynb
│   └── 7_Regional_Shipping_Analysis.ipynb
├── powerbi/
│   └── PowerBI_Report.pbix
├── reports/
│   ├── Research_Paper.pdf
│   └── Executive_Summary.md
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

*Adjust filenames and folder paths to match your actual repository.*

## 7. Analytical Methodology

### Data Cleaning and Financial Validation
Reviewed dataset structure, data types, missing values, and financial fields, then prepared a cleaned dataset for subsequent analysis.

### Revenue and Profit Analysis
Calculated gross sales, net sales, total discounts, total profit, and profit margin. Compared financial performance across markets and regions.

### Customer Analysis
Aggregated sales and profit by customer, compared customer segments, and developed a project-defined Customer Value Index.

### Product and Category Analysis
Compared product and category sales, profit, and profit margins. Identified high-sales, low-margin products and examined loss-making categories.

### Discount Impact Analysis
Compared profitability across discount-rate bands and developed a simplified what-if discount scenario. Results are observational and do not establish causation.

### Regional and Shipping Analysis
Examined market, country, and regional profitability, along with shipping modes and delivery performance.

### Profit Concentration Analysis
Compared the profit contributions of the ten highest-profit customers and products.

## 8. Key Financial Results

| Metric | Result |
|---|---:|
| Total records | 180,519 |
| Gross sales | $36,784,734.31 |
| Net sales after discounts | $33,054,402.04 |
| Total discounts | $3,730,378.40 |
| Total profit | $3,966,902.97 |
| Profit margin on net sales | 12.00% |
| Negative-profit records | 33,784 |

These figures are based on the processed dataset and the financial calculations performed in the project.

## 9. Streamlit Dashboard

The Streamlit application contains four analytical modules:

1. **Revenue & Profit Overview** — financial KPIs and market comparisons.
2. **Customer Value Dashboard** — customer profitability, rankings, and segment analysis.
3. **Product & Category Performance** — product margins, category profitability, and visual comparisons.
4. **Discount Impact Analyzer** — discount-rate comparisons and a what-if scenario calculator.

### Dashboard Screenshots

Add screenshots of your actual dashboard pages below. Upload the images to your repository first and adjust the paths if necessary.

#### Revenue & Profit Overview

![Revenue and Profit Overview](screenshots/executive_summary.png)

#### Customer Value Dashboard

![Customer Value Dashboard](screenshots/customer_value.png)

#### Product & Category Performance

![Product and Category Performance](screenshots/product_category.png)

#### Discount Impact Analyzer

![Discount Impact Analyzer](screenshots/discount_impact.png)

## 10. How to Run the Application

### Prerequisites

- Python installed on your computer.
- Git, if cloning the repository.
- The cleaned dataset located at `data/processed/apl_logistics_cleaned.csv`.

### Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd supply-chain-profitability-analysis
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

The application should open in your browser. If it does not, follow the local URL displayed in the terminal.

## 11. Project Deliverables

- Seven Jupyter notebooks covering data understanding, cleaning, and analysis.
- Cleaned supply chain dataset.
- Interactive Streamlit dashboard.
- Power BI report.
- Research paper describing the methodology, findings, limitations, and recommendations.
- Executive summary of the project.

## 12. Limitations

- A usable date field was unavailable for the intended time-based trend analysis.
- Discount-band comparisons are observational and do not prove that discounts cause profit changes.
- The Customer Value Index is a project-defined measure.
- The what-if discount calculator uses simplified assumptions and is not a predictive model.
- Findings are limited to the supplied dataset and its available fields.

## 13. Future Improvements

- Add reliable historical data for monthly and seasonal analysis.
- Incorporate more detailed cost information.
- Validate customer value scoring against additional business outcomes.
- Explore statistical methods for evaluating discount policies.
- Introduce automated data refresh and scheduled KPI reporting.

## 14. Author and Project Information

**Project:** Customer, Product, and Profitability Performance Analysis in Supply Chain Operations  
**Program:** Unified Mentor Data Analytics Internship  
**Tools:** Python, Pandas, Streamlit, Power BI, Jupyter Notebook

---
