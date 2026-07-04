
with developers as (
    select * from {{ ref('stg_github_developers') }}
)

select
    city,
    count(distinct id) as developer_count,
    round(avg(followers), 0) as avg_followers,
    round(avg(public_repos), 0) as avg_