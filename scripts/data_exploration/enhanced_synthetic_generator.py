import pandas as pd
import json
import random
import time
from datetime import datetime, timedelta
import numpy as np

class RealisticSyntheticDataGenerator:
    def __init__(self):
        self.twitter_usernames = [
            'DataScienceDaily', 'MLEngineer_', 'PythonDev23', 'AIResearcher', 'TechWriter_',
            'CodeNewbie2024', 'DevCommunity', 'OpenAIFan', 'DataAnalyst_', 'WebDev_Pro'
        ]
        
        self.reddit_subreddits = [
            'MachineLearning', 'datascience', 'Python', 'programming', 'webdev',
            'javascript', 'artificial', 'learnmachinelearning', 'analytics', 'coding'
        ]
        
        self.reddit_users = [
            'ml_enthusiast', 'data_guru', 'python_learner', 'code_explorer', 'ai_student',
            'dev_beginner', 'analytics_pro', 'tech_reader', 'algorithm_lover', 'stats_nerd'
        ]
    
    def generate_realistic_twitter_data(self, articles):
        """Generate realistic Twitter mentions based on article characteristics."""
        twitter_data = []
        
        print("Generating realistic Twitter mentions...")
        
        for article in articles:
            # Probability of Twitter mentions based on engagement
            mention_probability = min(0.6, (article['claps'] / 100) + 0.1)
            
            if random.random() < mention_probability:
                num_tweets = random.choices(
                    [1, 2, 3, 4, 5], 
                    weights=[40, 30, 20, 7, 3]  # Most articles get 1-2 tweets
                )[0]
                
                for _ in range(num_tweets):
                    tweet = self.create_realistic_tweet(article)
                    twitter_data.append(tweet)
        
        print(f"Generated {len(twitter_data)} Twitter mentions")
        return twitter_data
    
    def create_realistic_tweet(self, article):
        """Create a realistic tweet based on article content."""
        # Tweet templates based on article type
        templates = [
            "Just read this insightful piece on {topic}: {title} {url}",
            "Great article about {topic}! {title} {url} #datascience",
            "This is helpful: {title} {url}",
            "Interesting perspective on {topic} - {title} {url}",
            "Must-read for anyone interested in {topic}: {title} {url}"
        ]
        
        # Extract topic from title
        title_lower = article['title'].lower()
        if 'python' in title_lower:
            topic = 'Python programming'
        elif any(word in title_lower for word in ['ml', 'machine learning', 'ai']):
            topic = 'machine learning'
        elif 'data' in title_lower:
            topic = 'data science'
        else:
            topic = 'tech'
        
        template = random.choice(templates)
        tweet_text = template.format(
            topic=topic,
            title=article['title'][:80] + "..." if len(article['title']) > 80 else article['title'],
            url=article['url']
        )
        
        # Engagement based on article quality and randomness
        base_engagement = max(1, article['claps'] // 10)
        
        return {
            'tweet_id': f"tw_{random.randint(10**15, 10**16-1)}",
            'article_url': article['url'],
            'article_title': article['title'][:100],
            'tweet_text': tweet_text[:280],  # Twitter limit
            'username': random.choice(self.twitter_usernames),
            'user_followers': random.randint(50, 20000),
            'like_count': max(0, int(np.random.exponential(base_engagement))),
            'retweet_count': max(0, int(np.random.exponential(base_engagement * 0.3))),
            'reply_count': max(0, int(np.random.exponential(base_engagement * 0.2))),
            'quote_count': max(0, int(np.random.exponential(base_engagement * 0.1))),
            'created_at': self.random_recent_datetime().isoformat(),
            'collected_at': datetime.now().isoformat()
        }
    
    def generate_realistic_reddit_data(self, articles):
        """Generate realistic Reddit submissions based on article characteristics."""
        reddit_data = []
        
        print("Generating realistic Reddit submissions...")
        
        for article in articles:
            # Lower probability for Reddit (articles need more traction first)
            submission_probability = min(0.3, (article['claps'] / 200) + 0.05)
            
            if random.random() < submission_probability:
                submission = self.create_realistic_reddit_submission(article)
                reddit_data.append(submission)
        
        print(f"Generated {len(reddit_data)} Reddit submissions")
        return reddit_data
    
    def create_realistic_reddit_submission(self, article):
        """Create a realistic Reddit submission."""
        # Reddit title patterns
        title_patterns = [
            article['title'],  # Original title
            f"Found this helpful: {article['title']}",
            f"Thoughts on this article? {article['title']}",
            f"Good read: {article['title']}"
        ]
        
        # Choose subreddit based on article content
        title_lower = article['title'].lower()
        if 'python' in title_lower:
            subreddit = random.choice(['Python', 'programming', 'learnpython'])
        elif any(word in title_lower for word in ['ml', 'machine learning', 'ai']):
            subreddit = random.choice(['MachineLearning', 'datascience', 'artificial'])
        elif 'data' in title_lower:
            subreddit = random.choice(['datascience', 'analytics', 'statistics'])
        else:
            subreddit = random.choice(['programming', 'webdev', 'coding'])
        
        # Engagement based on article quality
        base_score = max(1, article['claps'] // 5)
        score = max(1, int(np.random.exponential(base_score)))
        
        return {
            'post_id': f"r_{random.randint(10**6, 10**7-1)}",
            'article_url': article['url'],
            'article_title': article['title'][:100],
            'post_title': random.choice(title_patterns)[:300],
            'subreddit': subreddit,
            'author': random.choice(self.reddit_users),
            'score': score,
            'upvote_ratio': round(random.uniform(0.7, 0.95), 2),
            'num_comments': max(0, int(np.random.exponential(score * 0.1))),
            'created_utc': int(self.random_recent_datetime().timestamp()),
            'permalink': f"/r/{subreddit}/comments/{random.randint(10**6, 10**7)}/",
            'selftext': self.generate_reddit_comment(),
            'collected_at': datetime.now().isoformat()
        }
    
    def generate_reddit_comment(self):
        """Generate realistic Reddit post comments."""
        comments = [
            "This is really helpful, thanks for sharing!",
            "Great explanation of the concepts.",
            "I was just looking for something like this.",
            "Bookmarked for later reading.",
            "The author did a good job explaining this topic.",
            "Anyone else try implementing this?",
            ""  # Many posts have no additional text
        ]
        return random.choice(comments)
    
    def random_recent_datetime(self):
        """Generate random datetime within last 30 days."""
        days_ago = random.randint(1, 30)
        hours_ago = random.randint(0, 23)
        return datetime.now() - timedelta(days=days_ago, hours=hours_ago)
    
    def generate_comprehensive_dataset(self, articles_file):
        """Generate complete synthetic social media dataset."""
        # Load articles
        with open(articles_file, 'r') as f:
            articles = json.load(f)
        
        print(f"Generating synthetic data for {len(articles)} articles...")
        
        # Generate social media data
        twitter_data = self.generate_realistic_twitter_data(articles)
        reddit_data = self.generate_realistic_reddit_data(articles)
        
        # Save datasets
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save Twitter data
        if twitter_data:
            twitter_json = f'data/raw/twitter_synthetic_{timestamp}.json'
            with open(twitter_json, 'w') as f:
                json.dump(twitter_data, f, indent=2)
            
            pd.DataFrame(twitter_data).to_csv(f'data/raw/twitter_synthetic_{timestamp}.csv', index=False)
            print(f"Saved Twitter data: {len(twitter_data)} records")
        
        # Save Reddit data
        if reddit_data:
            reddit_json = f'data/raw/reddit_synthetic_{timestamp}.json'
            with open(reddit_json, 'w') as f:
                json.dump(reddit_data, f, indent=2)
            
            pd.DataFrame(reddit_data).to_csv(f'data/raw/reddit_synthetic_{timestamp}.csv', index=False)
            print(f"Saved Reddit data: {len(reddit_data)} records")
        
        self.generate_summary_report(articles, twitter_data, reddit_data)
        
        return twitter_data, reddit_data
    
    def generate_summary_report(self, articles, twitter_data, reddit_data):
        """Generate comprehensive summary report."""
        print(f"\n" + "="*60)
        print("ENHANCED SYNTHETIC DATA GENERATION SUMMARY")
        print("="*60)
        
        print(f"Articles processed: {len(articles)}")
        print(f"Twitter mentions: {len(twitter_data)}")
        print(f"Reddit submissions: {len(reddit_data)}")
        
        if twitter_data:
            twitter_df = pd.DataFrame(twitter_data)
            twitter_coverage = len(set(t['article_url'] for t in twitter_data))
            print(f"Twitter coverage: {twitter_coverage}/{len(articles)} articles ({100*twitter_coverage/len(articles):.1f}%)")
            print(f"Average Twitter engagement: {twitter_df['like_count'].mean():.1f} likes")
        
        if reddit_data:
            reddit_df = pd.DataFrame(reddit_data)
            reddit_coverage = len(set(r['article_url'] for r in reddit_data))
            print(f"Reddit coverage: {reddit_coverage}/{len(articles)} articles ({100*reddit_coverage/len(articles):.1f}%)")
            print(f"Average Reddit score: {reddit_df['score'].mean():.1f}")
        
        print(f"\nDataset characteristics:")
        print(f"- Engagement correlates with article clap counts")
        print(f"- Realistic probability distributions")
        print(f"- Authentic social media text patterns")
        print(f"- Proper subreddit/topic matching")

def main():
    # Find latest Medium articles
    import glob
    
    files = glob.glob('data/raw/medium_articles_enhanced_*.json')
    if not files:
        print("No Medium articles found. Run the Medium collector first.")
        return
    
    latest_file = max(files)
    print(f"Using articles from: {latest_file}")
    
    # Generate synthetic data
    generator = RealisticSyntheticDataGenerator()
    generator.generate_comprehensive_dataset(latest_file)

if __name__ == "__main__":
    main()
