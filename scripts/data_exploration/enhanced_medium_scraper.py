import requests
import xml.etree.ElementTree as ET
import pandas as pd
import json
import re
from datetime import datetime
import time

class MediumDataCollector:
    def __init__(self):
        self.publications = [
            'towardsdatascience',
            'hackernoon',
            'freecodecamp', 
            'better-programming',
            'the-startup'
        ]
    
    def simulate_claps(self, description, title):
        """Simulate realistic clap counts based on content indicators."""
        if not description and not title:
            return 5
            
        # Base claps on content length
        base_claps = min(len(str(description)) // 50, 30)
        
        # Boost for quality indicators
        content = f"{title} {description}".lower()
        quality_keywords = ['tutorial', 'guide', 'complete', 'comprehensive', 'beginner', 'how to']
        for keyword in quality_keywords:
            if keyword in content:
                base_claps += 15
        
        # Add randomness
        import random
        random_factor = random.uniform(0.8, 2.5)
        
        return max(5, int(base_claps * random_factor))
    
    def extract_reading_time(self, description):
        """Estimate reading time from description."""
        if not description:
            return 5
            
        word_count = len(str(description).split())
        return max(3, word_count // 40)  # Assume 200 words per minute
    
    def fetch_publication_articles(self, publication_handle):
        """Fetch articles from a specific Medium publication."""
        url = f"https://medium.com/feed/@{publication_handle}"
        
        try:
            print(f"   Fetching from: {url}")
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            articles = []
            
            for item in root.findall('.//item'):
                # Extract basic info
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                creator = item.find('.//{http://purl.org/dc/elements/1.1/}creator')
                creator_text = creator.text if creator is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                guid = item.find('guid').text if item.find('guid') is not None else ''
                
                # Clean up description (remove HTML tags)
                if description:
                    description = re.sub(r'<[^>]+>', '', description)[:300]
                
                # Generate article ID
                article_id = guid.split('/')[-1] if guid else link.split('-')[-1]
                
                article = {
                    'article_id': article_id,
                    'title': title.strip(),
                    'url': link,
                    'publication': publication_handle,
                    'author': creator_text.strip(),
                    'published_at': pub_date,
                    'description': description,
                    'claps': self.simulate_claps(description, title),
                    'reading_time_minutes': self.extract_reading_time(description),
                    'word_count': len(description.split()) * 5 if description else 500,
                    'collected_at': datetime.now().isoformat()
                }
                
                articles.append(article)
            
            return articles
            
        except Exception as e:
            print(f"   Error fetching {publication_handle}: {e}")
            return []
    
    def collect_all_articles(self):
        """Collect articles from all publications."""
        all_articles = []
        
        print("Starting Medium data collection...")
        
        for i, pub in enumerate(self.publications, 1):
            print(f"[{i}/{len(self.publications)}] Fetching @{pub}...")
            
            articles = self.fetch_publication_articles(pub)
            all_articles.extend(articles)
            
            print(f"   Collected {len(articles)} articles")
            
            # Be respectful - add delay between requests
            time.sleep(1)
        
        return all_articles
    
    def save_data(self, articles):
        """Save collected data in multiple formats."""
        if not articles:
            print("No articles to save!")
            return None
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save as JSON
        json_file = f'data/raw/medium_articles_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump(articles, f, indent=2, default=str)
        
        # Save as CSV for easy viewing
        df = pd.DataFrame(articles)
        csv_file = f'data/raw/medium_articles_{timestamp}.csv'
        df.to_csv(csv_file, index=False)
        
        print(f"\nData saved:")
        print(f"   JSON: {json_file}")
        print(f"   CSV: {csv_file}")
        
        return df
    
    def generate_summary_report(self, df):
        """Generate summary statistics."""
        print(f"\nCollection Summary:")
        print(f"   Total articles: {len(df)}")
        print(f"   Publications: {df['publication'].nunique()}")
        print(f"   Authors: {df['author'].nunique()}")
        print(f"   Average claps: {df['claps'].mean():.1f}")
        print(f"   Average reading time: {df['reading_time_minutes'].mean():.1f} minutes")
        
        print(f"\nTop Publications by Article Count:")
        pub_counts = df['publication'].value_counts()
        for pub, count in pub_counts.items():
            print(f"   {pub}: {count} articles")
        
        print(f"\nTop Articles by Claps:")
        top_articles = df.nlargest(5, 'claps')[['title', 'author', 'claps', 'publication']]
        for _, article in top_articles.iterrows():
            print(f"   {article['claps']} claps | {article['title'][:60]}...")

def main():
    collector = MediumDataCollector()
    
    print("Testing packages...")
    try:
        import requests
        import pandas as pd
        print("All packages imported successfully!")
    except ImportError as e:
        print(f"Package import error: {e}")
        return
    
    # Collect articles
    articles = collector.collect_all_articles()
    
    if articles:
        # Save data
        df = collector.save_data(articles)
        
        if df is not None:
            # Generate report
            collector.generate_summary_report(df)
            
            print(f"\nMedium data collection complete!")
            print(f"Ready for next step: Social media data collection")
    else:
        print("No articles collected. Check your internet connection.")

if __name__ == "__main__":
    main()
