WITH source AS (
    SELECT * FROM {{ source('raw', 'web_analytics') }}
),

cleaned AS (
    SELECT
        article_url AS url,
        PARSE_DATE('%Y-%m-%d', date) AS date,
        CAST(sessions AS INT64) AS sessions,
        CAST(users AS INT64) AS users,
        CAST(pageviews AS INT64) AS pageviews,
        CAST(new_users AS INT64) AS new_users,
        _airbyte_extracted_at AS extracted_at
    FROM source
    WHERE article_url IS NOT NULL
)

SELECT * FROM cleaned
