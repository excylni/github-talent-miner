with developers as (
    select * from {{ ref('stg_github_developers') }}
)

select 
    company,
    count(distinct id) as developer_count,
    round(avg(followers), 0)