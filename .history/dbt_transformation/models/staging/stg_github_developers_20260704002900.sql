with source as (
    select * from {{ source('raw', 'github_developers')}}
)