with source as (
    select * from {{ source('raw', 'github_developers')}}
),

cleaned as (
    select
        id,
        login,
        html_url,
        score,
        type,
        ingested_at,

        -- strip @ from company names and trim whitespace
        case 
            when company is null or trim(company) = '' then null
            else trim((ltrim(trim(company), @)))
        end as company

        -- 
)