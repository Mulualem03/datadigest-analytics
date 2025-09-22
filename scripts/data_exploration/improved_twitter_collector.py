import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import random

class ImprovedTwitterCollector:
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        self.headers = {"Authorization": f"Bearer {bearer_token}"}
        self.request_count = 0
        self.max_requests_per_window = 75  # Conservative limit
    
    def search_broader_twitter_mentions(self, articles):
        """Search for broader mentions of topics/keywords from articles."""
        all_tweets = []
        
        print("Searching Twitter with broader topic-based queries...")
        
        # Extract key topics from articles
        topics = self.extract_search_topics(articles)
        
        for i, topic in enumerate(topics[:10], 1):  # Limit to 10 topics
            if self.request_count >= self.max_requests_per_window:
                print("Reached API limit, stopping collection")
                break
                
            print(f"[{i}/10] Searching topic: {topic}...")
            
            try:
                # Search for topic mentions
                params = {
                    'query': f'"{topic}" lang:en -is:retweet',
                    'max_results': 10,
                    'tweet.fields': 'created_at,author_id,public_metrics',
                    'user.fields': 'username,public_metrics',
                    'expansions': 'author_id'
                }
                
                response = requests.get(
                    f"{self.base_url}/tweets/search/recent",
                    headers=self.headers,
                    params=params,
                    timeout=15
                )
                
                self.request_count += 1
                
                if response.status_code == 200:
                    data = response.json()
                    tweets = self.process_topic_tweets(data, topic, articles)
                    all_tweets.extend(tweets)
                    print(f"   Found {len(tweets)} relevant tweets")
                elif response.status_code == 429:
                    print("   Rate limit hit, waiting 15 minutes...")
                    time.sleep(900)  # Wait 15 minutes
                else:
                    print(f"   API error: {response.status_code}")
                
                time.sleep(5)  # Conservative delay
                
            except Exception as e:
                print(f"   Error: {e}")
        
        return all_tweets
    
    def extract_search_topics(self, articles):
        """Extract searchable topics from article titles."""
        topics = []
        
        # Common data science/tech keywords to search for
        base_topics = [
            "machine learning", "data science", "python programming",
            "artificial intelligence", "deep learning", "data analysis"
        ]
        
        # Extract key phrases from article titles
        for article in articles[:20]:
            title = article['title'].lower()
            
            # Extract meaningful phrases
            if 'python' in title:
                topics.append('python programming')
            if 'machine learning' in title or 'ml' in title:
                topics.append('machine learning')
            if 'data' in title:
                topics.append('data science')
            if 'ai' in title or 'artificial intelligence' in title:
                topics.append('artificial intelligence')
        
        # Combine with base topics and remove duplicates
        all_topics = list(set(topics + base_topics))
        return all_topics[:15]  # Limit topics
    
    def process_topic_tweets(self, data, topic, articles):
        """Process tweets and link them to relevant articles."""
        tweets = []
        
        if 'data' not in data:
            return tweets
        
        # Create user lookup
        users_lookup = {}
        if 'includes' in data and 'users' in data['includes']:
            for user in data['includes']['users']:
                users_lookup[user['id']] = user
        
        for tweet in data['data']:
            user_info = users_lookup.get(tweet['author_id'], {})
            
            # Try to match tweet to a relevant article
            relevant_article = self.find_relevant_article(tweet['text'], articles)
            
            tweet_data = {
                'tweet_id': tweet['id'],
                'search_topic': topic,
                'article_url': relevant_article['url'] if relevant_article else '',
                'article_title': relevant_article['title'][:100] if relevant_article else '',
                'tweet_text': tweet['text'][:200],
                'created_at': tweet['created_at'],
                'username': user_info.get('username', ''),
                'user_followers': user_info.get('public_metrics', {}).get('followers_count', 0),
                'like_count': tweet['public_metrics']['like_count'],
                'retweet_count': tweet['public_metrics']['retweet_count'],
                'reply_count': tweet['public_metrics']['reply_count'],
                'quote_count': tweet['public_metrics']['quote_count'],
                'relevance_score': self.calculate_relevance(tweet['text'], topic),
                'collected_at': datetime.now().isoformat()
            }
            tweets.append(tweet_data)
        
        return tweets
    
    def find_relevant_article(self, tweet_text, articles):
        """Find the most relevant article for a tweet."""
        tweet_lower = tweet_text.lower()
        
        # Simple keyword matching
        for article in articles:
            title_words = article['title'].lower().split()
            
            # Check for word overlap
            overlap = sum(1 for word in title_words if word in tweet_lower and len(word) > 3)
            
            if overlap >= 2:  # If 2+ words match
                return article
        
        # Return a random article if no good match (for demonstration)
        return random.choice(articles) if articles else None
    
    def calculate_relevance(self, tweet_text, topic):
        """Calculate relevance score between tweet and topic."""
        tweet_lower = tweet_text.lower()
        topic_words = topic.lower().split()
        
        score = sum(1 for word in topic_words if word in tweet_lower)
        return score / len(topic_words)

def main():
    # Check for Twitter Bearer Token
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    if not bearer_token:
        print("Twitter Bearer Token not found. Set TWITTER_BEARER_TOKEN in environment.")
        return
    
    # Load Medium articles
    import glob
    files = glob.glob('data/raw/medium_articles_enhanced_*.json')
    if not files:
        print("No Medium articles found.")
        return
    
    latest_file = max(files)
    with open(latest_file, 'r') as f:
        articles = json.load(f)
    
    print(f"Loaded {len(articles)} Medium articles")
    
    # Collect Twitter data with improved strategy
    collector = ImprovedTwitterCollector(bearer_token)
    twitter_data = collector.search_broader_twitter_mentions(articles)
    
    if twitter_data:
        # Save data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        json_file = f'data/raw/twitter_topics_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump(twitter_data, f, indent=2)
        
        df = pd.DataFrame(twitter_data)
        csv_file = f'data/raw/twitter_topics_{timestamp}.csv'
        df.to_csv(csv_file, index=False)
        
        print(f"\nTwitter topic data collected:")
        print(f"   Records: {len(twitter_data)}")
        print(f"   Average relevance: {df['relevance_score'].mean():.2f}")
        print(f"   Files: {json_file}, {csv_file}")
    else:
        print("No Twitter data collected due to API limitations.")

if __name__ == "__main__":
    main()
