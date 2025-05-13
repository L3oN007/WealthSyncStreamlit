import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.services.data_manager import DataManager
from src.services.data_providers import NotionData, GoogleSheetsData
from configs.config import Config
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger("financial_data")

def update_financial_data():
    """Fetch and update financial data from sources"""
    with st.spinner("Fetching data from sources..."):
        try:
            # Get configuration
            config = Config()
            
            # Initialize data providers
            notion = NotionData(config.notion_token, config.notion_database_id)
            google_sheets = GoogleSheetsData(config.credentials_file, config.scope)
            
            # Fetch data
            notion_data = notion.fetch_data()
            finance_data = google_sheets.fetch_finance_data(config.finance_spreadsheet_id)
            
            # Check if data was fetched successfully
            if notion_data.empty and finance_data.empty:
                st.error("No data fetched from any source. Please check your configuration.")
                return False
                
            # Initialize data manager
            data_manager = DataManager(config.raw_data_dir)
            
            # Combine and save data
            combined_finance = data_manager.combine_finance_data(notion_data, finance_data)
            
            if not combined_finance.empty:
                st.success(f"Successfully updated financial data with {len(combined_finance)} records!")
                return True
            else:
                st.warning("No data was combined or saved.")
                return False
                
        except Exception as e:
            logger.error(f"Error updating financial data: {e}")
            st.error(f"Error updating data: {str(e)}")
            return False

def render_financial_data():
    """Render the financial data analysis page"""
    st.title("Financial Data Analysis")
    
    # Create a header section with update button
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔄 Update Data"):
                success = update_financial_data()
                if success:
                    st.rerun()  # Refresh the page to show updated data
       
    
    # Load configuration and data
    config = Config()
    data_manager = DataManager(config.raw_data_dir)
    
    # Load finance data
    finance_data = data_manager.load_finance_data()
    
    if finance_data.empty:
        st.warning("No financial data available. Please click the 'Update Data' button to fetch data.")
        return
    
    # Date range filter
    with st.container():
        st.subheader("Date Range Filter")
        
        # Get min and max dates
        min_date = finance_data['Date'].min().date()
        max_date = finance_data['Date'].max().date()
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", min_date)
        with col2:
            end_date = st.date_input("End Date", max_date)
    
    # Filter data by date
    mask = (finance_data['Date'].dt.date >= start_date) & (finance_data['Date'].dt.date <= end_date)
    filtered_data = finance_data.loc[mask]
    
    if filtered_data.empty:
        st.warning("No data available for the selected date range.")
        return
    
    # Summary statistics
    with st.container():
        st.subheader("Summary Statistics")
        
        # Calculate metrics
        total_amount = filtered_data['Amount'].sum()
        avg_amount = filtered_data['Amount'].mean()
        transaction_count = len(filtered_data)
        
        # Display metrics in columns
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Amount", f"${total_amount:,.2f}")
        col2.metric("Average Transaction", f"${avg_amount:,.2f}")
        col3.metric("Transaction Count", transaction_count)
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Data Tables", "Charts and Visualizations"])
    
    # Tab 1: Data Tables
    with tab1:
        # Category Summary Table
        st.subheader("Category Summary")
        
        # Group by category
        category_data = filtered_data.groupby('Category')['Amount'].agg(['sum', 'mean', 'count'])
        category_data = category_data.reset_index()
        category_data.columns = ['Category', 'Total Amount', 'Average Amount', 'Transaction Count']
        category_data = category_data.sort_values('Total Amount', ascending=False)
        
        # Format currency columns
        category_data['Total Amount'] = category_data['Total Amount'].map('${:,.2f}'.format)
        category_data['Average Amount'] = category_data['Average Amount'].map('${:,.2f}'.format)
        
        # Display category data
        st.dataframe(category_data, use_container_width=True)
        
        # Monthly Summary Table
        st.subheader("Monthly Summary")
        
        # Add month and year columns
        filtered_data['Month'] = filtered_data['Date'].dt.to_period('M')
        
        # Group by month
        monthly_table = filtered_data.groupby('Month')['Amount'].agg(['sum', 'mean', 'count'])
        monthly_table = monthly_table.reset_index()
        monthly_table.columns = ['Month', 'Total Amount', 'Average Amount', 'Transaction Count']
        monthly_table['Month'] = monthly_table['Month'].astype(str)
        monthly_table = monthly_table.sort_values('Month', ascending=False)
        
        # Format currency columns
        monthly_table['Total Amount'] = monthly_table['Total Amount'].map('${:,.2f}'.format)
        monthly_table['Average Amount'] = monthly_table['Average Amount'].map('${:,.2f}'.format)
        
        # Display monthly data
        st.dataframe(monthly_table, use_container_width=True)
        
        # Transaction Details Table
        st.subheader("Transaction Details")
        
        # Add a download button for CSV export
        csv = filtered_data[['Date', 'Category', 'Description', 'Amount']].to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="financial_data.csv",
            mime="text/csv",
        )
        
        # Sort by date (newest first)
        sorted_data = filtered_data.sort_values('Date', ascending=False)
        
        # Format the date and amount columns
        display_data = sorted_data.copy()
        display_data['Date'] = display_data['Date'].dt.strftime('%Y-%m-%d')
        display_data['Amount'] = display_data['Amount'].map('${:,.2f}'.format)
        
        # Display the transaction table
        st.dataframe(display_data[['Date', 'Category', 'Description', 'Amount']], use_container_width=True)
    
    # Tab 2: Charts and Visualizations
    with tab2:
        # Create a multi-column layout for charts
        col1, col2 = st.columns(2)
        
        # Spending by Category Pie Chart
        with col1:
            st.subheader("Spending by Category")
            
            # Prepare data for pie chart
            pie_data = filtered_data.groupby('Category')['Amount'].sum().reset_index()
            pie_data = pie_data.sort_values('Amount', ascending=False)
            
            # Create pie chart
            fig_pie = px.pie(
                pie_data, 
                values='Amount', 
                names='Category',
                title='Spending Distribution',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Top Categories Bar Chart
        with col2:
            st.subheader("Top Spending Categories")
            
            # Get top categories
            top_categories = filtered_data.groupby('Category')['Amount'].sum().sort_values(ascending=False).head(5)
            top_categories = top_categories.reset_index()
            
            # Create bar chart
            fig_bar = px.bar(
                top_categories,
                x='Category',
                y='Amount',
                title='Top 5 Spending Categories',
                color='Amount',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Monthly Trend Analysis
        st.subheader("Monthly Spending Trend")
        
        # Group by month for visualization
        monthly_data = filtered_data.groupby(filtered_data['Date'].dt.to_period('M'))['Amount'].sum()
        monthly_data = monthly_data.reset_index()
        monthly_data['Month'] = monthly_data['Date'].astype(str)
        
        # Create line chart with area fill
        fig_line = px.line(
            monthly_data, 
            x='Month', 
            y='Amount',
            markers=True,
            title='Monthly Spending Trend',
            labels={'Amount': 'Total Amount ($)', 'Month': 'Month'},
            line_shape='spline'
        )
        
        # Add area under the line
        fig_line.add_trace(
            go.Scatter(
                x=monthly_data['Month'],
                y=monthly_data['Amount'],
                mode='lines',
                fill='tozeroy',
                fillcolor='rgba(73, 176, 222, 0.2)',
                line=dict(width=0.5),
                showlegend=False
            )
        )
        
        # Customize layout
        fig_line.update_layout(
            xaxis_title="Month",
            yaxis_title="Total Amount ($)",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Category Comparison by Month
        st.subheader("Category Comparison by Month")
        
        # Get top categories
        top_cats = filtered_data.groupby('Category')['Amount'].sum().nlargest(3).index.tolist()
        
        # Filter data for top categories
        top_cat_data = filtered_data[filtered_data['Category'].isin(top_cats)]
        
        # Group by month and category
        cat_month_data = top_cat_data.groupby([top_cat_data['Date'].dt.to_period('M'), 'Category'])['Amount'].sum().reset_index()
        cat_month_data['Month'] = cat_month_data['Date'].astype(str)
        
        # Create grouped bar chart
        fig_cat_month = px.bar(
            cat_month_data,
            x='Month',
            y='Amount',
            color='Category',
            title='Top 3 Categories by Month',
            barmode='group'
        )
        
        st.plotly_chart(fig_cat_month, use_container_width=True) 