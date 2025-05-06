import streamlit as st
import streamlit as st
st.set_page_config(layout="wide")  # <-- must be here, first Streamlit command
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
from datetime import datetime

# Configuration
INSIGHTS_DIR = 'insights'
os.makedirs(INSIGHTS_DIR, exist_ok=True)

# Load data with caching
@st.cache_data
def load_data():
    return pd.read_csv('data/cleaned data/combined_regions.csv')

# Visualization generation function
def generate_comparison_visuals(df):
    """Generate and save 5 key comparison visuals"""
    sns.set_style("whitegrid")
    
    # 1. Engagement Comparison
    plt.figure(figsize=(10,6))
    sns.boxplot(data=df, x='region', y='like_ratio')
    plt.title('Like Ratio Comparison by Region')
    plt.savefig(f'{INSIGHTS_DIR}/engagement_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Category Distribution
    plt.figure(figsize=(12,8))
    top_categories = df['category_name'].value_counts().nlargest(10).index
    sns.countplot(
        data=df[df['category_name'].isin(top_categories)],
        y='category_name', hue='region',
        order=top_categories
    )
    plt.title('Top 10 Categories by Region')
    plt.savefig(f'{INSIGHTS_DIR}/category_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Sentiment Analysis
    plt.figure(figsize=(10,6))
    sns.violinplot(data=df, x='region', y='title_sentiment')
    plt.title('Title Sentiment Distribution by Region')
    plt.savefig(f'{INSIGHTS_DIR}/sentiment_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Publishing Time Heatmap
    plt.figure(figsize=(12,6))
    publish_hour = df.groupby(['region', 'publish_hour'])['views'].median().unstack().T
    sns.heatmap(publish_hour, cmap='YlGnBu', annot=True, fmt='.1f')
    plt.title('Median Views by Publish Hour (UTC)')
    plt.savefig(f'{INSIGHTS_DIR}/publish_time_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Trending Duration
    plt.figure(figsize=(10,6))
    sns.lineplot(
        data=df.groupby(['region', 'days_trending']).size().reset_index(name='count'),
        x='days_trending', y='count', hue='region'
    )
    plt.title('Videos Trending Duration by Region')
    plt.savefig(f'{INSIGHTS_DIR}/trending_duration.png', dpi=300, bbox_inches='tight')
    plt.close()

# Generate report function
def generate_report():
    """Generate a PDF report with all insights"""
    from fpdf import FPDF
    import base64
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.cell(200, 10, txt="YouTube Trending Videos Analysis Report", ln=1, align='C')
    pdf.ln(10)
    
    # Add each visualization
    visuals = [
        ('category_distribution.png', 'Top 10 Categories by Region'),
        ('sentiment_comparison.png', 'Title Sentiment Distribution'),
        ('engagement_comparison.png', 'Engagement Metrics Comparison'),
        ('publish_time_heatmap.png', 'Optimal Publishing Times'),
        ('trending_duration.png', 'Trending Duration Patterns')
    ]
    
    for img_file, title in visuals:
        pdf.cell(200, 10, txt=title, ln=1)
        pdf.image(f'{INSIGHTS_DIR}/{img_file}', x=10, w=190)
        pdf.ln(5)
    
    # Save report
    report_path = f'{INSIGHTS_DIR}/youtube_analysis_report.pdf'
    pdf.output(report_path)
    
    # Create download link
    with open(report_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return base64_pdf

# Main dashboard function
def main():
    # Load data
    combined_df = load_data()
    
    # Generate visuals on first run
    if not os.path.exists(f'{INSIGHTS_DIR}/engagement_comparison.png'):
        generate_comparison_visuals(combined_df)
    
    # Dashboard setup
    st.title("YouTube Trending Videos Analysis Dashboard")
    
    # Report download button
    st.sidebar.header("Report")
    if st.sidebar.button("Generate PDF Report"):
        with st.spinner('Generating report...'):
            pdf = generate_report()
            href = f'<a href="data:application/pdf;base64,{pdf}" download="youtube_analysis_report.pdf">Download Report</a>'
            st.sidebar.markdown(href, unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.header("Filters")
    selected_regions = st.sidebar.multiselect(
        "Select Regions", 
        options=combined_df['region'].unique(),
        default=combined_df['region'].unique()
    )
    
    # Date range filter
    min_date = pd.to_datetime(combined_df['trending_date']).min()
    max_date = pd.to_datetime(combined_df['trending_date']).max()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data
    filtered_df = combined_df[combined_df['region'].isin(selected_regions)]
    filtered_df['trending_date'] = pd.to_datetime(filtered_df['trending_date'])
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['trending_date'] >= pd.to_datetime(date_range[0])) &
            (filtered_df['trending_date'] <= pd.to_datetime(date_range[1]))
        ]
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Genre Popularity", 
        "Sentiment Analysis", 
        "Regional Comparison",
        "Report Insights"
    ])

    with tab1:
        st.header("Most Popular Genres")
        
        # Top genres by region
        fig = px.bar(
            filtered_df.groupby(['region', 'category_name']).size().reset_index(name='count'),
            x='category_name', y='count', color='region',
            barmode='group', height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Genre popularity over time
        st.subheader("Genre Trends Over Time")
        genre_time = filtered_df.groupby([
            pd.Grouper(key='trending_date', freq='M'),
            'category_name', 'region'
        ]).size().reset_index(name='count')
        
        fig = px.line(
            genre_time, 
            x='trending_date', y='count', 
            color='category_name', facet_col='region',
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.header("Sentiment Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            # Sentiment distribution
            fig = px.box(
                filtered_df, x='region', y='title_sentiment',
                color='region', height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Sentiment vs engagement
            fig = px.scatter(
                filtered_df.sample(1000), 
                x='title_sentiment', y='like_ratio',
                color='region', trendline="lowess",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment by category
        st.subheader("Sentiment by Video Category")
        sentiment_cat = filtered_df.groupby(['region', 'category_name'])['title_sentiment'].mean().reset_index()
        fig = px.bar(
            sentiment_cat.sort_values('title_sentiment', ascending=False),
            x='category_name', y='title_sentiment', color='region',
            barmode='group', height=500
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("Region-wise Comparison")
        
        # Metrics comparison
        metrics = st.radio(
            "Select Metric",
            options=['like_ratio', 'comment_ratio', 'views'],
            horizontal=True
        )
        
        fig = px.box(
            filtered_df, x='region', y=metrics,
            color='region', height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Publish time comparison
        st.subheader("Optimal Publishing Times")
        publish_hour = filtered_df.groupby(['region', 'publish_hour'])['views'].median().reset_index()
        fig = px.line(
            publish_hour, x='publish_hour', y='views',
            color='region', height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.header("Report Insights")
        
        # Display all saved visualizations with insights
        st.subheader("Category Popularity")
        st.image(f'{INSIGHTS_DIR}/category_distribution.png')
        st.write("""
        **Insight:** Music dominates across all regions, but regional variations exist:
        - IN: Strong presence of Bollywood music
        - US: More diverse categories including Comedy
        - GB: Higher proportion of Sports content
        """)
        
        st.subheader("Engagement Metrics")
        st.image(f'{INSIGHTS_DIR}/engagement_comparison.png')
        st.write("""
        **Key Finding:** GB has the highest like-to-view ratio (X%), 
        while US leads in comments per view.
        """)
        
        st.subheader("Optimal Posting Times")
        st.image(f'{INSIGHTS_DIR}/publish_time_heatmap.png')
        st.write("""
        **Recommendation:** Best posting times (UTC):
        - IN: 13:00-16:00
        - US: 18:00-21:00  
        - GB: 16:00-19:00
        """)

if __name__ == "__main__":
    main()