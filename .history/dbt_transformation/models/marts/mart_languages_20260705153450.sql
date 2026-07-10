with developers as (
    select * from {{ ref()'github_developers'}}
)