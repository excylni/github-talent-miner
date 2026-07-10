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
            else 
                -- applying normalization map
                case trim(ltrim(trim(company), '@'))

                    -- Google
                    when 'google' then 'Google'
                    when 'Google LLC' then 'Google'
                    when 'Google Germany' then 'Google'

                    -- SAP
                    when 'SAP SE' then 'SAP'

                    -- AWS 
                    when 'aws' then 'AWS'
                    when 'Amazon Web Services' then 'AWS'

                    -- innovex
                    when 'inovex GmbH' then 'inovex'

                    -- GitHub
                    when 'github' then 'GitHub'

                    -- DKFZ variations
                    when 'German Cancer Research Center (DKFZ)' then 'DKFZ'

                    -- EMBL variations
                    when 'EMBL Heidelberg' then 'EMBL'
                    when 'European Molecular Biology Laboratory (EMBL)' then 'EMBL'

                    -- KIT variations
                    when 'Karlsruhe Institute of Technology' then 'KIT'
                    when 'Karlsruhe Institute of Technology (KIT)' then 'KIT'
                    when 'Karlsruher Institut für Technologie' then 'KIT'
                    when 'Karlsruher Institut für Technologie (KIT)' then 'KIT'

                    -- Freelance variations
                    when 'Freelancer' then 'Freelance'

                    -- Zalando variations
                    when 'zalando' then 'Zalando'

                    -- Vercel variations
            when 'vercel' then 'Vercel'

            -- Elastic variations
            when 'elastic' then 'Elastic'

            -- Prisma variations
            when 'prisma' then 'Prisma'

            -- TUM variations
            when 'TUM' then 'Technical University of Munich'
            when 'TU Munich' then 'Technical University of Munich'


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