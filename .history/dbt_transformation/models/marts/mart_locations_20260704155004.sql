
with developers as (
    select * from {{ ref('stg_github_developers') }}
)

select
    city,
    count(distinct)