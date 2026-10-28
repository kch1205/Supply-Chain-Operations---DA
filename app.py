import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Supply Chain Profitability Dashboard",
    page_icon="📦",
    layout="wide"
)

page = st.sidebar.radio( 
    "Choose a dashboard",
    [
        "Revenue & Profit Overview",
        "Customer Value Dashboard",
        "Product & Category Performance",
        "Discount Impact Analyzer"
    ],
    key="main_page_selector"
)

page_titles = {
    "Revenue & Profit Overview": "📊 Revenue & Profit Overview",
    "Customer Value Dashboard": "👥 Customer Value Dashboard",
    "Product & Category Performance": "📦 Product & Category Performance",
    "Discount Impact Analyzer": "🏷️ Discount Impact Analyzer"
}

st.title(page_titles[page])
st.caption("Customer, Product, and Profitability Performance Analysis")

DATA_PATH = Path(__file__).parent / "data" / "processed" / "apl_logistics_cleaned.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"Dataset not found at: {DATA_PATH}")
    st.info(
        "Please place apl_logistics_cleaned.csv "
        "inside data/processed."
    )
    st.stop()

df.columns = df.columns.str.strip()

sales_col = "Order Item Total"
profit_col = "Order Profit Per Order"
discount_col = "Order Item Discount"

required_columns = [sales_col, profit_col, discount_col]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing required columns: {missing_columns}")
    st.stop()

# Dashboard navigation
st.sidebar.title("📊 Navigation")

filtered_df = df.copy()

if "Customer Segment" in df.columns:
    segments = sorted(df["Customer Segment"].dropna().unique())
    selected_segments = st.sidebar.multiselect(
        "Customer Segment",
        segments,
        default=segments
    )
    filtered_df = filtered_df[
        filtered_df["Customer Segment"].isin(selected_segments)
    ]

if "Market" in df.columns:
    markets = sorted(df["Market"].dropna().unique())
    selected_markets = st.sidebar.multiselect(
        "Market / Region",
        markets,
        default=markets
    )
    filtered_df = filtered_df[
        filtered_df["Market"].isin(selected_markets)
    ]

if "Order Region" in df.columns:
    regions = sorted(df["Order Region"].dropna().unique())

    selected_regions = st.sidebar.multiselect(
        "Order Region",
        regions,
        default=regions,
        key="order_region_filter"
    )

    filtered_df = filtered_df[
        filtered_df["Order Region"].isin(selected_regions)
    ]


if page == "Revenue & Profit Overview":
    net_sales = filtered_df[sales_col].sum()
    total_profit = filtered_df[profit_col].sum()
    total_discounts = filtered_df[discount_col].sum()
    profit_margin = (
        total_profit / net_sales * 100 if net_sales else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Net Sales", f"${net_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Total Discounts", f"${total_discounts:,.2f}")
    col4.metric("Profit Margin", f"{profit_margin:.2f}%")

if page == "Revenue & Profit Overview":
    st.divider()

    st.subheader("Revenue & Profit Overview")

    if "Market" in filtered_df.columns:
        market_summary = (
            filtered_df.groupby("Market", as_index=False)
            .agg(
                Net_Sales=(sales_col, "sum"),
                Total_Profit=(profit_col, "sum")
            )
        )

        chart_data = market_summary.melt(
            id_vars="Market",
            value_vars=["Net_Sales", "Total_Profit"],
            var_name="Metric",
            value_name="Amount"
        )

        fig = px.bar(
            chart_data,
            x="Market",
            y="Amount",
            color="Metric",
            barmode="group",
            title="Net Sales and Profit by Market"
        )

        st.plotly_chart(fig, use_container_width=True)


if page == "Customer Value Dashboard":

    # Customer Profitability Details
    if "Customer Id" in filtered_df.columns:
        customer_details = (
            filtered_df.groupby("Customer Id", as_index=False)
            .agg(
                Net_Sales=(sales_col, "sum"),
                Total_Profit=(profit_col, "sum"),
                Total_Discounts=(discount_col, "sum")
            )
        )

        customer_details["Profit_Margin_%"] = (
            customer_details["Total_Profit"]
            .div(customer_details["Net_Sales"].replace(0, float("nan")))
            .mul(100)
        )

        customer_details = customer_details.sort_values(
            "Total_Profit", ascending=False
        )

        st.subheader("Customer Profitability Details")
        st.dataframe(
            customer_details.rename(columns={
                "Customer Id": "Customer ID",
                "Net_Sales": "Net Sales",
                "Total_Profit": "Total Profit",
                "Total_Discounts": "Total Discounts",
                "Profit_Margin_%": "Profit Margin (%)"
            }).style.format({
                "Net Sales": "${:,.2f}",
                "Total Profit": "${:,.2f}",
                "Total Discounts": "${:,.2f}",
                "Profit Margin (%)": "{:.2f}%"
            }),
            use_container_width=True,
            hide_index=True
        )


        # Customer Value Tiers
        customer_details["Customer Value Tier"] = pd.qcut(
            customer_details["Total_Profit"].rank(method="first"),
            q=3,
            labels=["Low Value", "Medium Value", "High Value"]
        )

        st.subheader("Customer Value Tiers")

        tier_summary = (
            customer_details.groupby(
                "Customer Value Tier", observed=False
            )
            .agg(
                Customers=("Customer Id", "count"),
                Total_Profit=("Total_Profit", "sum")
            )
            .reset_index()
        )

        fig_tiers = px.bar(
            tier_summary,
            x="Customer Value Tier",
            y="Total_Profit",
            color="Customer Value Tier",
            title="Profit Contribution by Customer Value Tier",
            labels={
                "Customer Value Tier": "Customer Tier",
                "Total_Profit": "Total Profit"
            }
        )

        st.plotly_chart(fig_tiers, use_container_width=True)

        st.dataframe(
            tier_summary,
            use_container_width=True,
            hide_index=True
        )

        # Customer Value Tiers
        customer_details["Customer Value Tier"] = pd.qcut(
            customer_details["Total_Profit"].rank(method="first"),
            q=3,
            labels=["Low Value", "Medium Value", "High Value"]
        )

        st.subheader("Customer Value Tiers")

        tier_summary = (
            customer_details.groupby(
                "Customer Value Tier", observed=False
            )
            .agg(
                Customers=("Customer Id", "count"),
                Total_Profit=("Total_Profit", "sum")
            )
            .reset_index()
        )

        fig_tiers = px.bar(
            tier_summary,
            x="Customer Value Tier",
            y="Total_Profit",
            color="Customer Value Tier",
            title="Profit Contribution by Customer Value Tier",
            labels={
                "Customer Value Tier": "Customer Tier",
                "Total_Profit": "Total Profit"
            }
        )

        
        st.plotly_chart(
            fig_tiers,
            use_container_width=True,
            key="customer_value_tiers_chart"
        )


        st.dataframe(
            tier_summary,
            use_container_width=True,
            hide_index=True
        )

    # Net Sales by Customer Segment
    if "Customer Segment" in filtered_df.columns:
        segment_sales = (
            filtered_df.groupby("Customer Segment", as_index=False)
            .agg(Net_Sales=(sales_col, "sum"))
            .sort_values("Net_Sales", ascending=False)
        )

        fig_segment_sales = px.bar(
            segment_sales,
            x="Customer Segment",
            y="Net_Sales",
            title="Net Sales by Customer Segment",
            labels={
                "Customer Segment": "Customer Segment",
                "Net_Sales": "Net Sales"
            },
            color="Customer Segment"
        )

        st.plotly_chart(
            fig_segment_sales,
            use_container_width=True
        )

if page == "Customer Value Dashboard":
    st.subheader("Top 10 Customers by Net Sales")

    if "Customer Id" in filtered_df.columns:
        customer_sales = (
            filtered_df.groupby("Customer Id", as_index=False)
            .agg(Net_Sales=(sales_col, "sum"))
            .sort_values("Net_Sales", ascending=False)
            .head(10)
        )

        fig_customer = px.bar(
            customer_sales,
            x="Net_Sales",
            y="Customer Id",
            orientation="h",
            title="Top 10 Customers by Net Sales",
            labels={
                "Net_Sales": "Net Sales",
                "Customer Id": "Customer ID"
            }
        )

        fig_customer.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_customer, use_container_width=True)
        
    # Customer Sales vs Profit scatter chart
    if "Customer Id" in filtered_df.columns:
        customer_profit = (
            filtered_df.groupby("Customer Id", as_index=False)
            .agg(
                Net_Sales=(sales_col, "sum"),
                Total_Profit=(profit_col, "sum")
            )
        )

        fig_scatter = px.scatter(
            customer_profit,
            x="Net_Sales",
            y="Total_Profit",
            title="Customer Sales vs Profit",
            labels={
                "Net_Sales": "Net Sales",
                "Total_Profit": "Total Profit",
                "Customer Id": "Customer ID"
            },
            hover_data=["Customer Id"]
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

    
    # Bottom 10 Customers by Profit
    if "Customer Id" in filtered_df.columns:
        bottom_customers = (
            filtered_df.groupby("Customer Id", as_index=False)
            .agg(Total_Profit=(profit_col, "sum"))
            .sort_values("Total_Profit", ascending=True)
            .head(10)
        )

        st.subheader("Bottom 10 Customers by Profit")

        fig_bottom = px.bar(
            bottom_customers,
            x="Total_Profit",
            y="Customer Id",
            orientation="h",
            title="Bottom 10 Customers by Profit",
            labels={
                "Total_Profit": "Total Profit",
                "Customer Id": "Customer ID"
            }
        )

        fig_bottom.update_layout(
            yaxis={"categoryorder": "total descending"}
        )

        st.plotly_chart(fig_bottom, use_container_width=True)

    # Total Profit by Customer Segment
    if "Customer Segment" in filtered_df.columns:
        segment_profit = (
            filtered_df.groupby("Customer Segment", as_index=False)
            .agg(Total_Profit=(profit_col, "sum"))
            .sort_values("Total_Profit", ascending=False)
        )

        fig_segment_profit = px.bar(
            segment_profit,
            x="Customer Segment",
            y="Total_Profit",
            title="Total Profit by Customer Segment",
            labels={
                "Customer Segment": "Customer Segment",
                "Total_Profit": "Total Profit"
            },
            color="Customer Segment"
        )

        st.plotly_chart(
            fig_segment_profit,
            use_container_width=True
        )

    else:
        st.warning("Customer Id column was not found in the dataset.")


with st.expander("Preview cleaned dataset"):
    st.dataframe(filtered_df.head(100), use_container_width=True)

# Product & Category Performance
if page == "Product & Category Performance":
    st.divider()
    st.subheader("Product & Category Performance")


    # Product and Category Filters
    selected_category = None
    selected_product = None

    if "Category Name" in filtered_df.columns:
        category_options = sorted(
            filtered_df["Category Name"].dropna().unique()
        )
        selected_category = st.selectbox(
            "Select Product Category",
            ["All Categories"] + category_options,
            key="product_category_selector"
        )

    if "Product Name" in filtered_df.columns:
        product_options = sorted(
            filtered_df["Product Name"].dropna().unique()
        )
        selected_product = st.selectbox(
            "Select Product",
            ["All Products"] + product_options,
            key="product_selector"
        )

    
    product_filtered_df = filtered_df.copy()

    if selected_category and selected_category != "All Categories":
        product_filtered_df = product_filtered_df[
           product_filtered_df["Category Name"] == selected_category
    ]

    if selected_product and selected_product != "All Products":
        product_filtered_df = product_filtered_df[
           product_filtered_df["Product Name"] == selected_product
    ]

    if "Product Name" in product_filtered_df.columns:
        product_summary = (
           product_filtered_df.groupby("Product Name", as_index=False)
            .agg(
                Net_Sales=(sales_col, "sum"),
                Total_Profit=(profit_col, "sum")
            )
            .sort_values("Total_Profit", ascending=False)
        )

   

        product_filtered_df = filtered_df.copy()

        if selected_category and selected_category != "All Categories":
            product_filtered_df = product_filtered_df[
                product_filtered_df["Category Name"] == selected_category
            ]

        if selected_product and selected_product != "All Products":
            product_filtered_df = product_filtered_df[
                product_filtered_df["Product Name"] == selected_product
            ]

        st.subheader("Top 10 Products by Profit")



        fig_products = px.bar(
            product_summary.head(10),
            x="Total_Profit",
            y="Product Name",
            orientation="h",
            title="Top 10 Products by Profit",
            labels={
                "Total_Profit": "Total Profit",
                "Product Name": "Product"
            }
        )

        fig_products.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(fig_products, use_container_width=True)

    else:
        st.warning("Product Name column was not found in the dataset.")

    if "Category Name" in filtered_df.columns:
        category_summary = (
            filtered_df.groupby("Category Name", as_index=False)
            .agg(
                Net_Sales=(sales_col, "sum"),
                Total_Profit=(profit_col, "sum")
            )
            .sort_values("Total_Profit", ascending=False)
        )

        st.subheader("Profit by Product Category")

        fig_categories = px.bar(
            category_summary,
            x="Category Name",
            y="Total_Profit",
            title="Profit by Product Category",
            labels={
                "Category Name": "Category",
                "Total_Profit": "Total Profit"
            }
        )

        st.plotly_chart(fig_categories, use_container_width=True)

    else:
        st.warning("Category Name column was not found in the dataset.")


    # Product-level Profit Margin Analysis
    if "Product Name" in filtered_df.columns:
        product_margin = (
            product_filtered_df.groupby("Product Name", as_index=False)
            .agg(
                Net_Sales=(sales_col, "sum"),
                Total_Profit=(profit_col, "sum")
            )
        )

        product_margin["Profit Margin (%)"] = (
            product_margin["Total_Profit"]
            / product_margin["Net_Sales"].replace(0, float("nan"))
            * 100
        )

        product_margin = product_margin.sort_values(
            "Profit Margin (%)", ascending=True
        )

        st.subheader("Product-Level Profit Margin Analysis")

        st.dataframe(
            product_margin.rename(columns={
                "Product Name": "Product",
                "Net_Sales": "Net Sales",
                "Total_Profit": "Total Profit"
            }).style.format({
                "Net Sales": "${:,.2f}",
                "Total Profit": "${:,.2f}",
                "Profit Margin (%)": "{:.2f}%"
            }),
            use_container_width=True,
            hide_index=True
        )


# Category Profitability Heatmap
if page == "Product & Category Performance":
    if "Category Name" in filtered_df.columns:
        category_heatmap = (
            filtered_df.groupby("Category Name", as_index=False)
            .agg(
                Net_Sales=(sales_col, "sum"),
                Total_Profit=(profit_col, "sum")
            )
        )

        category_heatmap["Profit Margin (%)"] = (
            category_heatmap["Total_Profit"]
            / category_heatmap["Net_Sales"].replace(0, float("nan"))
            * 100
        )

        st.subheader("Category Profitability Heatmap")

        fig_heatmap = px.treemap(
            category_heatmap,
            path=["Category Name"],
            values="Net_Sales",
            color="Profit Margin (%)",
            color_continuous_scale="RdYlGn",
            hover_data=["Total_Profit", "Profit Margin (%)"],
            title="Category Sales and Profit Margin"
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True,
            key="category_profitability_heatmap"
        )

# Discount Impact Analyzer

if page == "Discount Impact Analyzer":
    st.subheader("What-If Discount Scenario")

    discount_rate_col = "Order Item Discount Rate"

    if discount_rate_col in filtered_df.columns:
        current_discount_rate = float(
            filtered_df[discount_rate_col].mean()
        )

        selected_discount_rate = st.slider(
            "Choose a discount rate (%)",
            min_value=0.0,
            max_value=50.0,
            value=min(max(current_discount_rate * 100, 0.0), 50.0),
            step=1.0,
            key="what_if_discount_slider"
        )

        st.caption(
            f"Selected discount rate: {selected_discount_rate:.1f}%"
        )

    
        # What-if profit estimate
        current_profit = filtered_df[profit_col].sum()
        gross_sales = (
            filtered_df["Sales"].sum()
            if "Sales" in filtered_df.columns
            else filtered_df[sales_col].sum()
        )

        current_discount_fraction = current_discount_rate
        selected_discount_fraction = selected_discount_rate / 100

        estimated_profit = current_profit - (
            selected_discount_fraction - current_discount_fraction
        ) * gross_sales

        profit_change = estimated_profit - current_profit

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Current Profit",
            f"${current_profit:,.2f}"
        )

        col2.metric(
            "Estimated Profit",
            f"${estimated_profit:,.2f}",
            delta=f"${profit_change:,.2f}"
        )

        col3.metric(
            "Assumed Discount Rate",
            f"{selected_discount_rate:.1f}%"
        )

        st.caption(
            "Scenario estimate assumes profit changes with the discount-rate difference "
            "applied to gross sales. Actual profit may differ."
        )
    

if page == "Discount Impact Analyzer":
    st.divider()
    st.subheader("Discount Impact Analyzer")

    discount_rate_col = "Order Item Discount Rate"

    if discount_rate_col in filtered_df.columns:
        discount_df = filtered_df.copy()

        discount_df["Discount Band"] = pd.cut(
            discount_df[discount_rate_col],
            bins=[-0.001, 0.05, 0.10, 0.20, float("inf")],
            labels=["0–5%", "5–10%", "10–20%", "20%+"]
        )

        discount_summary = (
            discount_df.groupby("Discount Band", observed=False)
            .agg(
                Records=(profit_col, "count"),
                Net_Sales=(sales_col, "sum"),
                Total_Profit=(profit_col, "sum"),
                Total_Discounts=(discount_col, "sum")
            )
            .reset_index()
        )

        discount_summary["Profit Margin (%)"] = (
            discount_summary["Total_Profit"]
            / discount_summary["Net_Sales"].replace(0, float("nan"))
            * 100
        )

        st.subheader("Performance by Discount Band")

        fig_discount = px.bar(
            discount_summary,
            x="Discount Band",
            y="Total_Profit",
            color="Discount Band",
            title="Total Profit by Discount Band",
            labels={
                "Discount Band": "Discount Range",
                "Total_Profit": "Total Profit"
            }
        )

        st.plotly_chart(fig_discount, use_container_width=True)

        st.subheader("Discount Performance Details")

        st.dataframe(
            discount_summary.style.format({
                "Records": "{:,.0f}",
                "Net_Sales": "${:,.2f}",
                "Total_Profit": "${:,.2f}",
                "Total_Discounts": "${:,.2f}",
                "Profit Margin (%)": "{:.2f}%"
            }),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("Order Item Discount Rate column was not found.")

st.caption(f"Showing {len(filtered_df):,} of {len(df):,} records after filtering.")