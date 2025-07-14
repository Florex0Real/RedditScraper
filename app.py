import streamlit as st
import pandas as pd
import time
from datetime import datetime
from reddit_scraper import RedditScraper
import os

# Page configuration
st.set_page_config(
    page_title="Reddit Scraper",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'scraper' not in st.session_state:
    st.session_state.scraper = RedditScraper()

if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = None

if 'scraping_status' not in st.session_state:
    st.session_state.scraping_status = None

if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = False

# Main title
st.title("🔍 Reddit Scraper")
st.markdown("Extract and export subreddit posts with filtering options")

# Sidebar configuration
st.sidebar.header("Reddit API Setup")

# API credentials section
with st.sidebar.expander("🔑 Enter Reddit API Credentials", expanded=not st.session_state.scraper.check_api_status()):
    st.markdown("**Get free Reddit API access:**")
    st.markdown("1. Go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)")
    st.markdown("2. Click 'Create App' → Select 'script'")
    st.markdown("3. Use `http://localhost:8080` as redirect URI")
    st.markdown("4. Copy your Client ID and Secret below")
    
    client_id = st.text_input(
        "Client ID",
        placeholder="Enter your Reddit Client ID",
        type="password",
        help="Found under your app name"
    )
    
    client_secret = st.text_input(
        "Client Secret", 
        placeholder="Enter your Reddit Client Secret",
        type="password",
        help="Click 'reveal' to see this value"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Connect to Reddit API", type="primary"):
            if client_id and client_secret:
                success = st.session_state.scraper.setup_reddit_client(client_id, client_secret)
                if success:
                    st.success("✅ Connected to Reddit API!")
                    st.rerun()
                else:
                    st.error("❌ Failed to connect. Check your credentials.")
            else:
                st.error("Please enter both Client ID and Secret")
    
    with col2:
        if st.button("Try Demo Mode"):
            st.session_state.demo_mode = True
            st.info("🎭 Demo mode enabled - showing sample data")

# Clear demo mode when API is connected
if st.session_state.demo_mode and st.session_state.scraper.check_api_status():
    if st.sidebar.button("🔄 Switch to Real Data"):
        st.session_state.demo_mode = False
        st.session_state.scraped_data = None
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("Scraping Configuration")

# Subreddit input
subreddit_name = st.sidebar.text_input(
    "Subreddit Name",
    placeholder="e.g., python, technology, news",
    help="Enter the subreddit name without 'r/'"
)

# Post type selection
post_type = st.sidebar.selectbox(
    "Post Type",
    ["hot", "new", "top"],
    help="Select the type of posts to scrape"
)

# Time period for top posts
time_filter = st.sidebar.selectbox(
    "Time Period (for top posts)",
    ["day", "week", "month", "year", "all"],
    index=2,
    help="Time period for top posts (only applies when 'top' is selected)"
)

# Number of posts
num_posts = st.sidebar.slider(
    "Number of Posts",
    min_value=10,
    max_value=100,
    value=25,
    step=5,
    help="Number of posts to scrape (respects Reddit's rate limits)"
)

# Scrape button
scrape_button = st.sidebar.button("🚀 Scrape Posts", type="primary")

# Reddit API status check
st.sidebar.markdown("### API Status")
if st.session_state.scraper.check_api_status():
    st.sidebar.success("✅ Reddit API Connected")
else:
    st.sidebar.error("❌ Reddit API Not Connected")
    st.sidebar.markdown("Enter your credentials above to start scraping!")

# Main content area
if scrape_button and (subreddit_name or st.session_state.demo_mode):
    # Handle demo mode
    if st.session_state.demo_mode:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🎭 Generating demo data...")
        progress_bar.progress(30)
        time.sleep(0.5)
        
        demo_subreddit = subreddit_name if subreddit_name else "demo"
        scraped_data = st.session_state.scraper.get_demo_data(demo_subreddit, post_type, num_posts)
        
        progress_bar.progress(80)
        status_text.text("✅ Demo data ready!")
        time.sleep(0.5)
        
        st.session_state.scraped_data = scraped_data
        st.session_state.scraping_status = "demo_success"
        progress_bar.progress(100)
        status_text.text("🎉 Demo data loaded successfully!")
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        st.info("🎭 You're viewing demo data. Enter your Reddit API credentials to scrape real posts!")
        
    # Handle real Reddit API scraping
    elif not st.session_state.scraper.check_api_status():
        st.error("Cannot connect to Reddit API. Please enter your credentials above or try demo mode.")
    else:
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🔍 Initializing scraper...")
            progress_bar.progress(10)
            
            status_text.text(f"📡 Connecting to r/{subreddit_name}...")
            progress_bar.progress(30)
            
            # Perform scraping
            status_text.text("📊 Scraping posts...")
            progress_bar.progress(50)
            
            scraped_data = st.session_state.scraper.scrape_subreddit(
                subreddit_name, 
                post_type, 
                num_posts,
                time_filter if post_type == "top" else "all"
            )
            
            progress_bar.progress(80)
            status_text.text("✅ Processing data...")
            
            if scraped_data and not scraped_data.empty:
                st.session_state.scraped_data = scraped_data
                st.session_state.scraping_status = "success"
                progress_bar.progress(100)
                status_text.text("🎉 Scraping completed successfully!")
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
            else:
                st.session_state.scraping_status = "no_data"
                progress_bar.empty()
                status_text.empty()
                st.warning(f"No posts found in r/{subreddit_name}. The subreddit might be empty or private.")
                
        except Exception as e:
            st.session_state.scraping_status = "error"
            progress_bar.empty()
            status_text.empty()
            st.error(f"Error scraping r/{subreddit_name}: {str(e)}")

elif scrape_button and not subreddit_name and not st.session_state.demo_mode:
    st.warning("Please enter a subreddit name or try demo mode first!")

# Display results
if st.session_state.scraped_data is not None and not st.session_state.scraped_data.empty:
    df = st.session_state.scraped_data
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Posts", len(df))
    
    with col2:
        avg_score = df['score'].mean()
        st.metric("Avg Score", f"{avg_score:.1f}")
    
    with col3:
        total_comments = df['num_comments'].sum()
        st.metric("Total Comments", f"{total_comments:,}")
    
    with col4:
        avg_upvote_ratio = df['upvote_ratio'].mean() * 100
        st.metric("Avg Upvote %", f"{avg_upvote_ratio:.1f}%")
    
    st.markdown("---")
    
    # Filters
    st.subheader("📋 Scraped Posts")
    
    # Filter controls
    col1, col2 = st.columns(2)
    
    with col1:
        min_score = st.number_input(
            "Minimum Score",
            min_value=0,
            value=0,
            help="Filter posts by minimum score"
        )
    
    with col2:
        min_comments = st.number_input(
            "Minimum Comments",
            min_value=0,
            value=0,
            help="Filter posts by minimum number of comments"
        )
    
    # Apply filters
    filtered_df = df[
        (df['score'] >= min_score) & 
        (df['num_comments'] >= min_comments)
    ]
    
    if len(filtered_df) == 0:
        st.warning("No posts match the current filters.")
    else:
        # Display filtered count
        if len(filtered_df) < len(df):
            st.info(f"Showing {len(filtered_df)} of {len(df)} posts after filtering")
        
        # Export functionality
        col1, col2 = st.columns([3, 1])
        
        with col2:
            csv_data = filtered_df.to_csv(index=False)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reddit_{subreddit_name}_{timestamp}.csv"
            
            st.download_button(
                label="📥 Export to CSV",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                help="Download the filtered data as CSV file"
            )
        
        # Pagination
        posts_per_page = 10
        total_pages = (len(filtered_df) - 1) // posts_per_page + 1
        
        if total_pages > 1:
            page = st.selectbox(
                "Page",
                range(1, total_pages + 1),
                format_func=lambda x: f"Page {x} of {total_pages}"
            )
            
            start_idx = (page - 1) * posts_per_page
            end_idx = start_idx + posts_per_page
            page_df = filtered_df.iloc[start_idx:end_idx]
        else:
            page_df = filtered_df
        
        # Display posts
        for idx, row in page_df.iterrows():
            with st.container():
                # Post header
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"### [{row['title']}]({row['url']})")
                
                with col2:
                    st.metric("Score", row['score'])
                
                with col3:
                    st.metric("Comments", row['num_comments'])
                
                # Post metadata
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.text(f"👤 u/{row['author']}")
                
                with col2:
                    st.text(f"📅 {row['created_date']}")
                
                with col3:
                    st.text(f"⬆️ {row['upvote_ratio']:.1%}")
                
                with col4:
                    if row['is_self']:
                        st.text("📝 Text Post")
                    else:
                        st.text("🔗 Link Post")
                
                # Post content preview
                if row['selftext'] and len(row['selftext']) > 0:
                    preview = row['selftext'][:200] + "..." if len(row['selftext']) > 200 else row['selftext']
                    st.markdown(f"**Content Preview:** {preview}")
                
                # Post URL if it's a link post
                if not row['is_self'] and row['url']:
                    st.markdown(f"**Link:** {row['url']}")
                
                st.markdown("---")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🔍 Reddit Scraper | Built with Streamlit & PRAW</p>
        <p><small>Please respect Reddit's API terms of service and rate limits</small></p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Usage instructions
with st.expander("ℹ️ How to Use"):
    st.markdown("""
    ### Getting Started
    1. **Try Demo Mode**: Click "Try Demo Mode" to see sample data without setup
    2. **OR Get Reddit API Access**: 
       - Go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
       - Create a new "script" app with redirect URI: `http://localhost:8080`
       - Enter your Client ID and Secret in the sidebar
    3. **Enter Subreddit Name**: Type the name without 'r/' (e.g., 'python', 'technology')
    4. **Configure Options**: Choose post type, time period, and number of posts
    5. **Click Scrape Posts**: Start extracting data
    
    ### Features
    - **Demo Mode**: Test the interface with sample data
    - **Real Reddit Data**: Extract actual posts with your API credentials
    - **Multiple Post Types**: Hot, new, or top posts with time filters
    - **Smart Filtering**: Filter by score and comment count
    - **Easy Export**: Download data as CSV files
    - **Responsive Design**: Works on any device
    
    ### Data Included
    - Post title and URL
    - Author information  
    - Score and upvote ratio
    - Number of comments
    - Creation date and time
    - Post content (for text posts)
    - Post type (text/link)
    
    ### Free & Legal
    This tool uses Reddit's official API with proper rate limiting and respects all terms of service.
    """)
