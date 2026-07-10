with developers as (
    select * from {{ ref('stg_github_developers') }}
)

select 
    primary_language,
    count(distinct id) as developer_count
    count(distinct)