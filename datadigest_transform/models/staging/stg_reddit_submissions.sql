WITH source AS (
    SELECT * FROM {{ source('raw', 'reddit_submissions') }}
),

cleaned AS (
    SELECT
        permalink AS url,
        CAST(score AS INT64) AS upvotes,
        author,
        subreddit,
        selftext,
        _airbyte_extracted_at AS extracted_at
    FROM source
    WHERE permalink IS NOT NULL
)

SELECT * FROM cleaned
