WITH source AS (
    SELECT * FROM {{ source('raw', 'twitter_mentions') }}
),

cleaned AS (
    SELECT
        article_url AS url,
        CAST(like_count AS INT64) AS likes,
        tweet_text,
        username,
        created_at,
        _airbyte_extracted_at AS extracted_at
    FROM source
    WHERE article_url IS NOT NULL
)

SELECT * FROM cleaned
