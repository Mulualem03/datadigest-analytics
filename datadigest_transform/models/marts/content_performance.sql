-- Content Performance Mart: Unified analytics across all platforms
WITH articles AS (
    SELECT * FROM {{ ref('stg_medium_articles') }}
),

twitter AS (
    SELECT 
        url,
        COUNT(*) as twitter_mention_count,
        SUM(likes) as total_twitter_likes
    FROM {{ ref('stg_twitter_mentions') }}
    GROUP BY url
),

reddit AS (
    SELECT 
        url,
        COUNT(*) as reddit_submission_count,
        SUM(upvotes) as total_reddit_upvotes
    FROM {{ ref('stg_reddit_submissions') }}
    GROUP BY url
),

web_traffic AS (
    SELECT 
        url,
        SUM(sessions) as total_sessions,
        SUM(users) as total_users,
        SUM(pageviews) as total_pageviews,
        AVG(sessions) as avg_daily_sessions
    FROM {{ ref('stg_web_analytics') }}
    GROUP BY url
)

SELECT 
    a.url,
    a.title,
    a.author,
    a.publication,
    a.claps,
    a.word_count,
    
    -- Social engagement metrics
    COALESCE(t.twitter_mention_count, 0) as twitter_mentions,
    COALESCE(t.total_twitter_likes, 0) as twitter_likes,
    COALESCE(r.reddit_submission_count, 0) as reddit_submissions,
    COALESCE(r.total_reddit_upvotes, 0) as reddit_upvotes,
    
    -- Web traffic metrics
    COALESCE(w.total_sessions, 0) as total_sessions,
    COALESCE(w.total_users, 0) as total_users,
    COALESCE(w.total_pageviews, 0) as total_pageviews,
    COALESCE(w.avg_daily_sessions, 0) as avg_daily_sessions,
    
    -- Calculated engagement score (weighted)
    (
        a.claps + 
        COALESCE(t.total_twitter_likes, 0) * 2 + 
        COALESCE(r.total_reddit_upvotes, 0) * 3
    ) as social_engagement_score,
    
    a.extracted_at
FROM articles a
LEFT JOIN twitter t ON a.url = t.url
LEFT JOIN reddit r ON a.url = r.url
LEFT JOIN web_traffic w ON a.url = w.url
