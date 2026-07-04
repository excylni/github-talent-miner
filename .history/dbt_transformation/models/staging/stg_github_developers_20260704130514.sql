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

        -- take the first part of the location
        case
            when location is null or trim(location) = '' then null
            else trim((split_part(location, ',', 1)))
)