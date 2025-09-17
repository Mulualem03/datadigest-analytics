import pandas as pd
import json
import random
import time
from datetime import datetime, timedelta

class SocialMediaDataGenerator:
    def __init__(self):
        self.twitter_usernames = ['TechGuru2024', 'DataScienceFan', 'DevCommunity', 'AIEnthusiast', 'CodeNewbie', 'MLExpert']
        self.reddit_subreddits = ['programming', 'datascience', 'MachineLearning', 'webdev', 'Python', 'javascript']
    
    def generate_twitter_data(self, articles):
        """Generate realistic Twitter mention data for articles."""
        twitter_mentions = []
        
        print("Generating Twitter mention data...")
        
        for article in articles:
            # 40% chance of having Twitter mentions
            if random.random() < 0.4:
                num_tweets = random.randint(1, 5)
                
                for _ in range(num_tweets):
                    tweet = {
                        'tweet_id': f"tw_{random.randint(100000000, 999999999)}",
                        'article_url': article['url'],
                        'article_title': article['title'][:100],
                        'tweet_text': self.generate_tweet_text(article['title']),
                        'username': random.choice(self.twitter_usernames),
                        'user_followers': random.randint(50, 10000),
                        'like_count': random.randint(0, 100),
                        'retweet_count': random.randint(0, 25),
                        'reply_count': random.randint(0, 10),
                        'created_at': self.random_recent_date(),
                        'collected_at': datetime.now().isoformat()
                    }
                    twitter_mentions.append(tweet)
        
        return twitter_mentions
    
    def generate_reddit_data(self, articles):
        """Generate realistic Reddit submission data for articles."""
        reddit_submissions = []
        
        print("Generating Reddit submission data...")
        
        for article in articles:
            # 25% chance of having Reddit submissions
            if random.random() < 0.25:
                submission = {
                    'post_id': f"r_{random.randint(10000, 99999)}",
                    'article_url': article['url'],
                    'article_title': article['title'][:100],
                    'post_title': self.generate_reddit_title(article['title']),
                    'subreddit': random.choice(self.reddit_subreddits),
                    'author': f"user_{random.randint(1000, 9999)}",
                    'score': random.randint(1, 500),
                    'upvote_ratio': round(random.uniform(0.6, 0.95), 2),
                    'num_comments': random.randint(0, 50),
                    'created_at': self.random_recent_date(),
                    'collected_at': datetime.now().isoformat()
                }
                reddit_submissions.append(submission)
        
        return reddit_submissions
    
    def generate_tweet_text(self, title):
        """Generate realistic tweet text based on article title."""
        templates = [
            f"Just read this: {title[:80]}... Great insights!",
            f"Interesting article about {title[:60]}... Worth a read",
            f"This is helpful: {title[:70]}...",
            f"Good resource: {title[:75]}..."
        ]
        return random.choice(templates)
    
    def generate_reddit_title(self, title):
        """Generate Reddit-style post titles."""
        templates = [
            f"Found this helpful: {title}",
            f"Thoughts on: {title}",
            f"Good read: {title}",
            title  # Sometimes use original title
        ]
        return random.choice(templates)[:200]
    
    def random_recent_date(self):
        """Generate random date within last 30 days."""
        days_ago = random.randint(1, 30)
        return (datetime.now() - timedelta(days=days_ago)).isoformat()

class WebAnalyticsGenerator:
    def __init__(self):
        self.traffic_sources = ['organic', 'social', 'direct', 'referral', 'email']
        self.devices = ['desktop', 'mobile', 'tablet']
        self.countries = ['US', 'GB', 'CA', 'DE', 'IN', 'AU']
    
    def generate_analytics_data(self, articles):
        """Generate realistic web analytics data for articles."""
        analytics_data = []
        
        print("Generating web analytics data...")
        
        for article in articles:
            # Generate 30 days of traffic data per article
            base_daily_sessions = self.calculate_base_sessions(article)
            
            for days_ago in range(30, 0, -1):
                date = datetime.now() - timedelta(days=days_ago)
                
                # Apply traffic decay and patterns
                daily_sessions = self.apply_traffic_patterns(base_daily_sessions, days_ago)
                
                analytics_record = {
                    'date': date.strftime('%Y-%m-%d'),
                    'article_url': article['url'],
                    'article_title': article['title'][:100],
                    'publication': article['publication'],
                    'sessions': daily_sessions,
                    'users': int(daily_sessions * random.uniform(0.7, 0.9)),
                    'new_users': int(daily_sessions * random.uniform(0.6, 0.8)),
                    'pageviews': int(daily_sessions * random.uniform(1.1, 2.2)),
                    'bounce_rate': round(random.uniform(0.3, 0.8), 3),
                    'avg_session_duration': round(random.uniform(60, 400), 1),
                    'pages_per_session': round(random.uniform(1.2, 3.5), 2)
                }
                
                # Add traffic source breakdown
                analytics_record.update(self.distribute_traffic_sources(daily_sessions))
                
                # Add device breakdown
                analytics_record.update(self.distribute_devices(daily_sessions))
                
                analytics_data.append(analytics_record)
        
        return analytics_data
    
    def calculate_base_sessions(self, article):
        """Calculate base daily sessions based on article engagement."""
        # Base sessions from clap count (engagement indicator)
        base_sessions = max(5, article['claps'] // 3)
        
        # Publication multiplier
        pub_multipliers = {
            'towardsdatascience': 2.0,
            'freecodecamp': 2.5,
            'hackernoon': 1.5,
            'better-programming': 1.3
        }
        
        multiplier = pub_multipliers.get(article['publication'], 1.0)
        return int(base_sessions * multiplier * random.uniform(0.8, 1.5))
    
    def apply_traffic_patterns(self, base_sessions, days_ago):
        """Apply realistic traffic decay and weekly patterns."""
        sessions = base_sessions
        
        # Traffic decay over time
        if days_ago > 7:
            decay = 0.8 ** ((days_ago - 7) / 7)
            sessions *= decay
        
        # Weekly pattern (less traffic on weekends)
        day_of_week = (datetime.now() - timedelta(days=days_ago)).weekday()
        if day_of_week in [5, 6]:  # Weekend
            sessions *= 0.7
        
        return max(1, int(sessions))
    
    def distribute_traffic_sources(self, total_sessions):
        """Distribute sessions across traffic sources."""
        distribution = {
            'sessions_organic': int(total_sessions * random.uniform(0.35, 0.55)),
            'sessions_social': int(total_sessions * random.uniform(0.15, 0.35)),
            'sessions_direct': int(total_sessions * random.uniform(0.10, 0.25)),
            'sessions_referral': int(total_sessions * random.uniform(0.05, 0.15)),
        }
        distribution['sessions_email'] = max(0, total_sessions - sum(distribution.values()))
        return distribution
    
    def distribute_devices(self, total_sessions):
        """Distribute sessions across device types."""
        desktop = int(total_sessions * random.uniform(0.45, 0.65))
        mobile = int(total_sessions * random.uniform(0.25, 0.45))
        tablet = max(0, total_sessions - desktop - mobile)
        
        return {
            'sessions_desktop': desktop,
            'sessions_mobile': mobile,
            'sessions_tablet': tablet
        }

class ComprehensiveDataGenerator:
    def __init__(self):
        self.social_generator = SocialMediaDataGenerator()
        self.analytics_generator = WebAnalyticsGenerator()
    
    def generate_complete_dataset(self, articles_file):
        """Generate comprehensive dataset from Medium articles."""
        # Load Medium articles
        print(f"Loading articles from {articles_file}...")
        
        try:
            with open(articles_file, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            print(f"Loaded {len(articles)} articles")
        except Exception as e:
            print(f"Error loading articles: {e}")
            return
        
        # Generate social media data
        twitter_data = self.social_generator.generate_twitter_data(articles)
        reddit_data = self.social_generator.generate_reddit_data(articles)
        
        # Generate web analytics data
        analytics_data = self.analytics_generator.generate_analytics_data(articles)
        
        # Save all datasets
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        datasets = {
            'twitter_mentions': twitter_data,
            'reddit_submissions': reddit_data,
            'web_analytics': analytics_data
        }
        
        for dataset_name, data in datasets.items():
            if data:
                # Save JSON
                json_file = f'data/raw/{dataset_name}_{timestamp}.json'
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # Save CSV
                csv_file = f'data/raw/{dataset_name}_{timestamp}.csv'
                pd.DataFrame(data).to_csv(csv_file, index=False, encoding='utf-8')
                
                print(f"Saved {len(data)} {dataset_name} records")
        
        self.generate_summary_report(articles, twitter_data, reddit_data, analytics_data)
    
    def generate_summary_report(self, articles, twitter_data, reddit_data, analytics_data):
        """Generate comprehensive data summary."""
        print(f"\n" + "="*60)
        print("COMPREHENSIVE DATA COLLECTION SUMMARY")
        print("="*60)
        
        print(f"\nMedium Articles: {len(articles)}")
        print(f"Twitter Mentions: {len(twitter_data)}")
        print(f"Reddit Submissions: {len(reddit_data)}")
        print(f"Web Analytics Records: {len(analytics_data)}")
        
        # Coverage analysis
        articles_with_twitter = len(set(t['article_url'] for t in twitter_data))
        articles_with_reddit = len(set(r['article_url'] for r in reddit_data))
        
        print(f"\nCross-Platform Coverage:")
        print(f"Articles with Twitter mentions: {articles_with_twitter}/{len(articles)} ({100*articles_with_twitter/len(articles):.1f}%)")
        print(f"Articles with Reddit posts: {articles_with_reddit}/{len(articles)} ({100*articles_with_reddit/len(articles):.1f}%)")
        print(f"Articles with analytics: {len(analytics_data)//30}/{len(articles)} ({100*(len(analytics_data)//30)/len(articles):.1f}%)")
        
        print(f"\nDataset ready for Modern Data Stack implementation!")

def main():
    # Find the most recent enhanced Medium articles file
    import glob
    
    files = glob.glob('data/raw/medium_articles_enhanced_*.json')
    if not files:
        print("No enhanced Medium articles found. Run enhanced_medium_scraper_v2.py first.")
        return
    
    latest_file = max(files)
    print(f"Using latest articles file: {latest_file}")
    
    # Generate comprehensive dataset
    generator = ComprehensiveDataGenerator()
    generator.generate_complete_dataset(latest_file)

if __name__ == "__main__":
    main()
