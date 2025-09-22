import requests
import json
import pandas as pd
from datetime import datetime
import time
import os
from urllib.parse import quote

class TwitterAPICollector:
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        self.headers = {"Authorization": f"Bearer {bearer_token}"}
    
    def search_tweets_for_medium_articles(self, articles, max_results_per_article=10):
        """Search Twitter for mentions of Medium articles."""
        all_tweets = []
        
        print("Searching Twitter for real article mentions...")
        
        for i, article in enumerate(articles[:20], 1):  # Limit to 20 for API quota
            print(f"[{i}/20] Searching: {article['title'][:50]}...")
            
            # Extract domain from article URL for search
            try:
                # Search for the article URL
                search_query = f'url:"{article["url"]}"'
                
                params = {
                    'query': search_query,
                    'max_results': min(max_results_per_article, 10),
                    'tweet.fields': 'created_at,author_id,public_metrics,lang',
                    'user.fields': 'username,name,public_metrics',
                    'expansions': 'author_id'
                }
                
                response = requests.get(
                    f"{self.base_url}/tweets/search/recent",
                    headers=self.headers,
                    params=params,
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    tweets = self.process_twitter_response(data, article)
                    all_tweets.extend(tweets)
                    print(f"   Found {len(tweets)} tweets")
                elif response.status_code == 429:
                    print("   Rate limit hit, waiting...")
                    time.sleep(15)
                else:
                    print(f"   API error: {response.status_code}")
                
                # Respect rate limits
                time.sleep(2)
                
            except Exception as e:
                print(f"   Error: {e}")
        
        return all_tweets
    
    def process_twitter_response(self, data, article):
        """Process Twitter API response."""
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
            
            tweet_data = {
                'tweet_id': tweet['id'],
                'article_url': article['url'],
                'article_title': article['title'][:100],
                'tweet_text': tweet['text'],
                'created_at': tweet['created_at'],
                'username': user_info.get('username', ''),
                'user_followers': user_info.get('public_metrics', {}).get('followers_count', 0),
                'like_count': tweet['public_metrics']['like_count'],
                'retweet_count': tweet['public_metrics']['retweet_count'],
                'reply_count': tweet['public_metrics']['reply_count'],
                'quote_count': tweet['public_metrics']['quote_count'],
                'collected_at': datetime.now().isoformat()
            }
            tweets.append(tweet_data)
        
        return tweets

def main():
    # Check for Twitter Bearer Token
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    if not bearer_token:
        print("Twitter Bearer Token not found in environment variables.")
        print("To get real Twitter data:")
        print("1. Go to https://developer.twitter.com/portal/dashboard")
        print("2. Create a new app and get Bearer Token")
        print("3. Add to your .env: TWITTER_BEARER_TOKEN=your_token_here")
        print("4. Load environment: source .env")
        return
    
    # Load Medium articles
    import glob
    files = glob.glob('data/raw/medium_articles_enhanced_*.json')
    if not files:
        print("No Medium articles found. Run the Medium collector first.")
        return
    
    latest_file = max(files)
    with open(latest_file, 'r') as f:
        articles = json.load(f)
    
    print(f"Loaded {len(articles)} Medium articles")
    
    # Collect Twitter data
    collector = TwitterAPICollector(bearer_token)
    twitter_data = collector.search_tweets_for_medium_articles(articles)
    
    if twitter_data:
        # Save data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        json_file = f'data/raw/twitter_real_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump(twitter_data, f, indent=2)
        
        df = pd.DataFrame(twitter_data)
        csv_file = f'data/raw/twitter_real_{timestamp}.csv'
        df.to_csv(csv_file, index=False)
        
        print(f"\nReal Twitter data collected:")
        print(f"   Records: {len(twitter_data)}")
        print(f"   Files: {json_file}, {csv_file}")
    else:
        print("No Twitter data collected.")

if __name__ == "__main__":
    main()
