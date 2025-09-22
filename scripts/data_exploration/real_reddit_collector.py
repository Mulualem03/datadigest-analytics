import requests
import json
import pandas as pd
from datetime import datetime
import time
from urllib.parse import urlparse

class RedditAPICollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'DataDigest-Analytics/1.0 (Educational Research Project)'
        }
        self.base_url = "https://www.reddit.com"
    
    def search_reddit_for_articles(self, articles):
        """Search Reddit for submissions containing Medium article URLs."""
        all_submissions = []
        
        print("Searching Reddit for real article submissions...")
        
        for i, article in enumerate(articles[:30], 1):  # Limit for respectful usage
            print(f"[{i}/30] Searching: {article['title'][:50]}...")
            
            try:
                # Search for the specific URL
                search_url = f"{self.base_url}/search.json"
                params = {
                    'q': f'url:{article["url"]}',
                    'sort': 'relevance',
                    'limit': 10,
                    't': 'all'  # All time
                }
                
                response = requests.get(
                    search_url,
                    headers=self.headers,
                    params=params,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    submissions = self.process_reddit_response(data, article)
                    all_submissions.extend(submissions)
                    print(f"   Found {len(submissions)} submissions")
                else:
                    print(f"   Error: {response.status_code}")
                
                # Be respectful with rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"   Error: {e}")
        
        return all_submissions
    
    def process_reddit_response(self, data, article):
        """Process Reddit API response."""
        submissions = []
        
        if 'data' not in data or 'children' not in data['data']:
            return submissions
        
        for item in data['data']['children']:
            if item['kind'] != 't3':  # Only link/text submissions
                continue
                
            post = item['data']
            
            submission = {
                'post_id': post['id'],
                'article_url': article['url'],
                'article_title': article['title'][:100],
                'post_title': post['title'],
                'subreddit': post['subreddit'],
                'author': post['author'],
                'score': post['score'],
                'upvote_ratio': post['upvote_ratio'],
                'num_comments': post['num_comments'],
                'created_utc': post['created_utc'],
                'permalink': f"https://reddit.com{post['permalink']}",
                'selftext': post.get('selftext', '')[:200],
                'collected_at': datetime.now().isoformat()
            }
            submissions.append(submission)
        
        return submissions

def main():
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
    
    # Collect Reddit data
    collector = RedditAPICollector()
    reddit_data = collector.search_reddit_for_articles(articles)
    
    if reddit_data:
        # Save data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        json_file = f'data/raw/reddit_real_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump(reddit_data, f, indent=2)
        
        df = pd.DataFrame(reddit_data)
        csv_file = f'data/raw/reddit_real_{timestamp}.csv'
        df.to_csv(csv_file, index=False)
        
        print(f"\nReal Reddit data collected:")
        print(f"   Records: {len(reddit_data)}")
        print(f"   Unique subreddits: {df['subreddit'].nunique()}")
        print(f"   Files: {json_file}, {csv_file}")
    else:
        print("No Reddit data found for these articles.")

if __name__ == "__main__":
    main()
