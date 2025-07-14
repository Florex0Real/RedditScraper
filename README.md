# 🔍 Reddit Scraper

A user-friendly Streamlit application for extracting and analyzing Reddit data. Scrape subreddit posts, filter results, and export data to CSV format using free Reddit API access.

## ✨ Features

### 🎭 Demo Mode
- Test the interface with sample data without API setup
- Explore all features instantly

### 🔑 Personal API Access
- Easy input for your free Reddit API credentials
- Secure access to real Reddit data
- Step-by-step setup guide included

### 📊 Data Extraction Features
- **Multiple post types**: Hot, new, top posts
- **Time filters**: Daily, weekly, monthly, yearly, or all-time
- **Smart filtering**: Filter by score and comment count
- **Real-time progress**: Status updates during scraping

### 💾 Export Options
- Download data in CSV format
- Automatic file naming
- Export filtered datasets

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/yourusername/reddit-scraper.git
cd reddit-scraper
pip install streamlit praw pandas requests
```

### 2. Run the Application

```bash
streamlit run app.py
```

### 3. Open in Browser

The app will automatically open at `http://localhost:8501`

## 🔧 Reddit API Setup (Free)

### Step 1: Reddit Account
Go to [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) with your Reddit account.

### Step 2: Create Application
1. Click **"Create App"** or **"Create Another App"**
2. Fill out the form:
   - **Name**: Your app name (e.g., "My Reddit Scraper")
   - **App type**: Select **"script"**
   - **Description**: Optional
   - **About URL**: Leave blank
   - **Redirect URI**: `http://localhost:8080`
3. Click **"Create app"**

### Step 3: Get Credentials
- **Client ID**: Short string shown under your app name
- **Client Secret**: Long string revealed by clicking "reveal"

### Step 4: Use in Application
Enter these credentials in the Streamlit interface and click "Connect to Reddit API".

## 📋 Usage

### Demo Mode
1. Click **"Try Demo Mode"**
2. Explore the interface with sample data
3. Test all features

### Real Data Scraping
1. Enter your Reddit API credentials
2. Type the subreddit name you want to scrape (without r/)
3. Select post type (hot, new, top)
4. Set number of posts to scrape
5. Click **"Scrape Posts"**

### Filtering and Export
1. Set minimum score and comment filters
2. Review the results
3. Use **"Export to CSV"** to download data

## 📁 Project Structure

```
reddit-scraper/
├── app.py                 # Main Streamlit application
├── reddit_scraper.py      # Reddit API functions
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── README.md             # This file
```

## 🛠️ Technologies

- **[Streamlit](https://streamlit.io/)**: Web application framework
- **[PRAW](https://praw.readthedocs.io/)**: Python Reddit API Wrapper
- **[Pandas](https://pandas.pydata.org/)**: Data processing and analysis
- **[Python 3.11+](https://python.org/)**: Programming language

## 📊 Extracted Data

For each post, the following information is extracted:
- Title and URL
- Author information
- Score and upvote ratio
- Number of comments
- Creation date and time
- Post content (for text posts)
- Post type (text/link)
- Domain information
- Special tags (over_18, spoiler, stickied, locked)

## ⚖️ Legal and Ethical Usage

- Uses Reddit's official API
- Respects rate limiting rules
- Complies with terms of service
- Designed for personal and research use

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🆘 Support

If you encounter any issues:
1. Search the [Issues](https://github.com/yourusername/reddit-scraper/issues) page
2. Open a new issue
3. Test with demo mode and share results

## 🔄 Updates

### v1.0.0
- ✅ Initial release
- ✅ Demo mode added
- ✅ User-friendly API setup
- ✅ CSV export feature
- ✅ Smart filtering system

---

**Note**: This application can only scrape data from public subreddits. It does not provide access to private or restricted subreddits.