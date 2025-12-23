import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page config
st.set_page_config(
    page_title="Social Media Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# No Custom CSS needed for standard Light Theme
# Streamlit's default is clean and readable.

@st.cache_data
def load_data():
    if os.path.exists("results_output.csv"):
        return pd.read_csv("results_output.csv")
    return None

def main():
    st.title("📊 Social Media Analysis Dashboard")

    df = load_data()

    if df is None:
        st.error("No results found! Run `python main.py` first to generate data.")
        return

    # Sidebar Filters
    st.sidebar.header("Filter Options")
    
    # Filter by Sentiment
    sentiment_filter = st.sidebar.multiselect(
        "Select Sentiment:",
        options=df["sentiment"].unique(),
        default=df["sentiment"].unique()
    )

    # Filter by Cluster
    cluster_filter = st.sidebar.multiselect(
        "Select Topic Cluster:",
        options=sorted(df["cluster"].unique()),
        default=sorted(df["cluster"].unique())
    )

    # Apply Filters
    filtered_df = df[
        (df["sentiment"].isin(sentiment_filter)) &
        (df["cluster"].isin(cluster_filter))
    ]

    # KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Posts", len(filtered_df))
    
    with col2:
        positive_count = len(filtered_df[filtered_df['sentiment'] == 'Positive'])
        st.metric("Positive Posts", positive_count)
    
    with col3:
        negative_count = len(filtered_df[filtered_df['sentiment'] == 'Negative'])
        st.metric("Negative Posts", negative_count)

    with col4:
        # Determine dominant topic
        if not filtered_df.empty:
            top_cluster = filtered_df['cluster'].mode()[0]
            st.metric("Dominant Topic ID", int(top_cluster))
        else:
            st.metric("Dominant Topic ID", "N/A")

    st.markdown("---")

    # Layout: Charts
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("Sentiment Distribution")
        sentiment_counts = filtered_df['sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count'] 
        
        fig_pie = px.pie(
            sentiment_counts, 
            values='Count', 
            names='Sentiment',
            hole=0.4,
            color='Sentiment',
            color_discrete_map={'Positive':'#00cc96', 'Negative':'#ef553b', 'Neutral':'#ffa15a'}
        )
        # Using plotly_white for clean look
        fig_pie.update_layout(template="plotly_white", margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.subheader("Topic Cluster Volume")
        cluster_counts = filtered_df['cluster'].value_counts().reset_index()
        cluster_counts.columns = ['Cluster ID', 'Count']
        cluster_counts = cluster_counts.sort_values('Cluster ID')
        
        fig_bar = px.bar(
            cluster_counts,
            x='Cluster ID', 
            y='Count',
            color='Count',
            color_continuous_scale="Viridis",
            text='Count' 
        )
        fig_bar.update_layout(template="plotly_white", showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_bar, use_container_width=True)

    # Treemap (Topic Keywords)
    st.subheader("Topic > Sentiment Hierarchy")
    
    if not filtered_df.empty:
        # Add a dummy 'All' column for root node
        filtered_df["All"] = "Social Media Posts"
        
        fig_tree = px.treemap(
            filtered_df, 
            path=['All', 'cluster', 'sentiment'], 
            color='sentiment',
            color_discrete_map={'Positive':'#00cc96', 'Negative':'#ef553b', 'Neutral':'#ffa15a'},
            maxdepth=3
        )
        fig_tree.update_layout(template="plotly_white", margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig_tree, use_container_width=True)

    # Data Table
    st.markdown("---")
    st.subheader("Raw Data Explorer")
    search_term = st.text_input("🔍 Search in tweets:", "")
    
    if search_term:
        display_df = filtered_df[filtered_df['text'].str.contains(search_term, case=False, na=False)]
    else:
        display_df = filtered_df

    st.dataframe(
        display_df[['date', 'user', 'text', 'sentiment', 'cluster']],
        use_container_width=True,
        hide_index=True
    )

if __name__ == "__main__":
    main()
