with developers as (
    select * from {{ ref('stg_github_developers') }}
)

select 
    company,
    count(distinct id) as developer_count,
    round(avg(followers), 0) as avg_followers,
    round(avg(public_repos), 0) as avg_public_repos,
    listagg(distinct city, ', ')
        within group (order by city)  as cities_present

where company is not null
group by company
order by 