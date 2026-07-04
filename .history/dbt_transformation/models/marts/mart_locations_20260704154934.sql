
with developers as (
    select * from {{ ref('stg')}}
)