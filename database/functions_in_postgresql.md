```sql
select category, status_code, count from dbo.ia_process_status a
left join (
    select category, status_code, count(distinct file_name) count
    from dbo.ia_model_outputs
    group by category, status_code
) s
    on s.cateogry = a.category
```
