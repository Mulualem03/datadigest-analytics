WITH source AS (
    SELECT * FROM {{ source('raw', 'medium_articles') }}
),

cleaned AS (
    SELECT
        url,
        title,
        author,
        publication,
        CAST(claps AS INT64) AS claps,
        CAST(word_count AS INT64) AS word_count,
        description,
        _airbyte_extracted_at AS extracted_at
    FROM source
    WHERE url IS NOT NULL
)

SELECT * FROM cleaned
