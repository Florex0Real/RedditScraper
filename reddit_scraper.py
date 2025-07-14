import praw
import pandas as pd
import time
from datetime import datetime
import os
import requests

class RedditScraper:
    def __init__(self):
        """Initialize Reddit scraper."""
        self.reddit = None
        self.client_id = None
        self.client_secret = None
        self.user_agent = "RedditScraper/1.0 by YourUsername"
    
    def setup_reddit_client(self, client_id=None, client_secret=None):
        """Setup Reddit client with provided credentials."""
        try:
            # Use provided credentials or stored ones
            if client_id and client_secret:
                self.client_id = client_id
                self.client_secret = client_secret
            
            # Check if credentials are available
            if not self.client_id or not self.client_secret:
                self.reddit = None
                return False
            
            # Initialize Reddit client
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )
            
            # Test the connection
            self.reddit.auth.limits
            return True
            
        except Exception as e:
            print(f"Error setting up Reddit client: {str(e)}")
            self.reddit = None
            return False
    
    def check_api_status(self):
        """Check if Reddit API is accessible."""
        try:
            if self.reddit is None:
                return False
            
            # Try to access a public subreddit to test connection
            test_subreddit = self.reddit.subreddit("python")
            list(test_subreddit.hot(limit=1))
            return True
            
        except Exception as e:
            print(f"API status check failed: {str(e)}")
            return False
    
    def scrape_subreddit(self, subreddit_name, post_type="hot", limit=25, time_filter="all"):
        """
        Scrape posts from a specific subreddit.
        
        Args:
            subreddit_name (str): Name of the subreddit to scrape
            post_type (str): Type of posts to get ('hot', 'new', 'top')
            limit (int): Maximum number of posts to scrape
            time_filter (str): Time filter for top posts ('day', 'week', 'month', 'year', 'all')
        
        Returns:
            pandas.DataFrame: Scraped post data
        """
        try:
            if self.reddit is None:
                raise Exception("Reddit client not initialized")
            
            # Get the subreddit
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Check if subreddit exists and is accessible
            try:
                subreddit_info = subreddit.display_name
            except Exception as e:
                if "404" in str(e) or "Forbidden" in str(e):
                    raise Exception(f"Subreddit 'r/{subreddit_name}' not found or is private")
                else:
                    raise Exception(f"Error accessing subreddit: {str(e)}")
            
            # Get posts based on type
            posts = []
            
            if post_type == "hot":
                posts_iterator = subreddit.hot(limit=limit)
            elif post_type == "new":
                posts_iterator = subreddit.new(limit=limit)
            elif post_type == "top":
                posts_iterator = subreddit.top(time_filter=time_filter, limit=limit)
            else:
                raise Exception(f"Invalid post type: {post_type}")
            
            # Extract post data
            scraped_posts = []
            
            for post in posts_iterator:
                try:
                    # Rate limiting - small delay between requests
                    time.sleep(0.1)
                    
                    post_data = {
                        'title': post.title,
                        'author': str(post.author) if post.author else '[deleted]',
                        'score': post.score,
                        'upvote_ratio': post.upvote_ratio,
                        'num_comments': post.num_comments,
                        'created_utc': post.created_utc,
                        'created_date': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        'url': post.url,
                        'permalink': f"https://reddit.com{post.permalink}",
                        'selftext': post.selftext if hasattr(post, 'selftext') else '',
                        'is_self': post.is_self,
                        'subreddit': str(post.subreddit),
                        'post_id': post.id,
                        'domain': post.domain if hasattr(post, 'domain') else '',
                        'over_18': post.over_18,
                        'spoiler': post.spoiler,
                        'stickied': post.stickied,
                        'locked': post.locked
                    }
                    
                    scraped_posts.append(post_data)
                    
                except Exception as e:
                    print(f"Error processing post: {str(e)}")
                    continue
            
            if not scraped_posts:
                return pd.DataFrame()
            
            # Create DataFrame
            df = pd.DataFrame(scraped_posts)
            
            # Sort by score descending
            df = df.sort_values('score', ascending=False).reset_index(drop=True)
            
            return df
            
        except Exception as e:
            raise Exception(f"Error scraping subreddit: {str(e)}")
    
    def get_subreddit_info(self, subreddit_name):
        """
        Get basic information about a subreddit.
        
        Args:
            subreddit_name (str): Name of the subreddit
        
        Returns:
            dict: Subreddit information
        """
        try:
            if self.reddit is None:
                raise Exception("Reddit client not initialized")
            
            subreddit = self.reddit.subreddit(subreddit_name)
            
            info = {
                'name': subreddit.display_name,
                'title': subreddit.title,
                'description': subreddit.public_description,
                'subscribers': subreddit.subscribers,
                'created_utc': subreddit.created_utc,
                'over18': subreddit.over18,
                'lang': subreddit.lang,
                'url': f"https://reddit.com/r/{subreddit.display_name}"
            }
            
            return info
            
        except Exception as e:
            raise Exception(f"Error getting subreddit info: {str(e)}")
    
    def search_posts(self, subreddit_name, query, sort="relevance", time_filter="all", limit=25):
        """
        Search for posts within a subreddit.
        
        Args:
            subreddit_name (str): Name of the subreddit to search
            query (str): Search query
            sort (str): Sort method ('relevance', 'hot', 'top', 'new', 'comments')
            time_filter (str): Time filter ('all', 'day', 'week', 'month', 'year')
            limit (int): Maximum number of posts to return
        
        Returns:
            pandas.DataFrame: Search results
        """
        try:
            if self.reddit is None:
                raise Exception("Reddit client not initialized")
            
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Perform search
            search_results = subreddit.search(
                query=query,
                sort=sort,
                time_filter=time_filter,
                limit=limit
            )
            
            # Extract post data
            scraped_posts = []
            
            for post in search_results:
                try:
                    # Rate limiting
                    time.sleep(0.1)
                    
                    post_data = {
                        'title': post.title,
                        'author': str(post.author) if post.author else '[deleted]',
                        'score': post.score,
                        'upvote_ratio': post.upvote_ratio,
                        'num_comments': post.num_comments,
                        'created_utc': post.created_utc,
                        'created_date': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        'url': post.url,
                        'permalink': f"https://reddit.com{post.permalink}",
                        'selftext': post.selftext if hasattr(post, 'selftext') else '',
                        'is_self': post.is_self,
                        'subreddit': str(post.subreddit),
                        'post_id': post.id,
                        'domain': post.domain if hasattr(post, 'domain') else '',
                        'over_18': post.over_18,
                        'spoiler': post.spoiler,
                        'stickied': post.stickied,
                        'locked': post.locked
                    }
                    
                    scraped_posts.append(post_data)
                    
                except Exception as e:
                    print(f"Error processing search result: {str(e)}")
                    continue
            
            if not scraped_posts:
                return pd.DataFrame()
            
            # Create DataFrame
            df = pd.DataFrame(scraped_posts)
            
            return df
            
        except Exception as e:
            raise Exception(f"Error searching posts: {str(e)}")
    
    def get_demo_data(self, subreddit_name="demo", post_type="hot", limit=25):
        """
        Generate demo data for testing purposes.
        
        Args:
            subreddit_name (str): Name for the demo subreddit
            post_type (str): Type of posts (for demo labeling)
            limit (int): Number of demo posts to generate
        
        Returns:
            pandas.DataFrame: Demo post data
        """
        import random
        
        demo_titles = [
            "How to get started with Python programming",
            "Best practices for web development in 2024",
            "Amazing sunset photo from my backyard",
            "Just finished my first machine learning project!",
            "Tips for debugging code efficiently",
            "New breakthrough in renewable energy technology",
            "Cozy reading nook setup - what do you think?",
            "Free online courses that changed my career",
            "My homemade pizza turned out better than expected",
            "Quick tutorial: Setting up a development environment",
            "Interesting documentary recommendation",
            "Local coffee shop with incredible atmosphere",
            "Weekend project: Building a simple web app",
            "Nature photography from my recent hiking trip",
            "Book recommendation for aspiring entrepreneurs"
        ]
        
        demo_authors = ["user123", "coder_pro", "nature_lover", "tech_enthusiast", "student_dev", 
                       "photo_guru", "learning_always", "code_newbie", "adventure_seeker", "book_worm"]
        
        demo_posts = []
        current_time = time.time()
        
        for i in range(min(limit, len(demo_titles))):
            post_data = {
                'title': demo_titles[i],
                'author': random.choice(demo_authors),
                'score': random.randint(5, 500),
                'upvote_ratio': round(random.uniform(0.7, 0.98), 2),
                'num_comments': random.randint(0, 100),
                'created_utc': current_time - random.randint(3600, 86400 * 7),  # Last week
                'created_date': datetime.fromtimestamp(current_time - random.randint(3600, 86400 * 7)).strftime('%Y-%m-%d %H:%M:%S'),
                'url': f"https://reddit.com/r/{subreddit_name}/post_{i}",
                'permalink': f"https://reddit.com/r/{subreddit_name}/comments/demo_{i}",
                'selftext': "This is demo content for testing the Reddit scraper interface." if random.choice([True, False]) else "",
                'is_self': random.choice([True, False]),
                'subreddit': subreddit_name,
                'post_id': f"demo_{i}",
                'domain': "self.reddit" if random.choice([True, False]) else "example.com",
                'over_18': False,
                'spoiler': False,
                'stickied': False,
                'locked': False
            }
            demo_posts.append(post_data)
        
        # Create DataFrame and sort by score
        df = pd.DataFrame(demo_posts)
        df = df.sort_values('score', ascending=False).reset_index(drop=True)
        
        return df

    def export_to_csv(self, df, filename=None):
        """
        Export DataFrame to CSV file.
        
        Args:
            df (pandas.DataFrame): Data to export
            filename (str): Optional filename, if not provided will use timestamp
        
        Returns:
            str: CSV data as string
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"reddit_scrape_{timestamp}.csv"
            
            # Convert to CSV string
            csv_data = df.to_csv(index=False)
            
            return csv_data
            
        except Exception as e:
            raise Exception(f"Error exporting to CSV: {str(e)}")
