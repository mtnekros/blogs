# Killing processes in postgresql

Ever been in a situation where you just ran a query on a million row table, and
forgot to put the limit or the where clause? Well, there is a way to kill that
process instead a waiting forever for that query to finish.

* First use the following query to find the pid (process id) for the query that
    you ran.
```sql
SELECT pid, datname, usename, query FROM pg_stat_activity
where usename = 'webapp'
```
* Now use the pg_terminate_backend command to kill the specific process.
```sql
SELECT pg_terminate_backend(19589);
```
