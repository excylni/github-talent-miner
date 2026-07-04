with source as (
    select * from {{ source('raw', 'github_developers')}}
),

cleaned as (
    select
        id,
        login,
        html_url
)