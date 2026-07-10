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
            else trim(ltrim(trim(company), '@'))
        end as company,

        -- take the first part of the location
        case
            when location is null or trim(location) = '' then null
            else trim(split_part(location, ',', 1))
        end as city,

        -- keeping raw location just in case
        location as location_raw,

        followers::int as followers,
        public_repos::int as public_repos,
        bio,
        primary_language,
        top_languages

        from source
), 

-- remove duplicates
deduplicated as (
    select *
    from cleaned
    qualify row_number() over (
        partition by id
        order by ingested_at desc
    ) = 1
)

select * from deduplicated