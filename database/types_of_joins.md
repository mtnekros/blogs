# How does the query planner decide joining strategies in PostgreSQL?

## Overview
If you have ever tried reading execution plan of your queries & been frustrated, you might find this blog useful. Specifically, I am going to discuss the different joining algorithms used by PostgreSQL for different situation.

IMPORTANT: Rewrite the overview once the blog is complete.
<!--The cost of choosing different joining algorithm differs depending on the size of the table and presence/absence of indexes on the joining columns. Query planner will estimate the costs of each strategy and use the one with the smallest costs. In this blog, we are going to look at different types of joining strategies & when they are preferred with the help of some examples.-->
<!---->
<!--These usually come up when reading the query plans of queries. Without understanding how different types of joins works, it is a bit difficult to understand the whole query plan as well.-->

Example of a query plan:
```

```


## Let's create some tables to verify our assumptions

## Types of Join
PostreSQL mainly uses mainly three algorithms for joining.
1. Nested Loop Join
2. Merge Join
3. Hash Join

## Nested Join
In nested loop join, the engine will take each row from one table and match it with every row in the other table. So every row in one table will be match against every row in the other table. As the name suggests it uses the nested loop approach with O(n^2) time complexity.

```
 for each row r1 in t1 do
        for each row r2 in t2 do
            if r1 and r2 satisfy the join condition then
                yield row <r1, r2>
```

I know that this sounds inefficient. But it is actually the best method when the table sizes are both small, as it doesn't take much time to run a nested loop through two small sized tables. Additionaly, this also doesn't have any type of overhead costs.

## Hash Join
In a hash join, we first prepare a hash map using the contents of one table (lets say t1), ideally whichever one is smaller after applying local predicates (explain local predicates here). This is also called the build side of join. It maps the joining column to the columns needed in the final output.

Once the hash map is built, we scan the other table, t2 (AKA the probe side). For each row of t2, we match the rows in t1, using the hash map and prepare the final joined rows.

Hash join alwasy has a high startup cost, which is to build the hash map. It also costs memory (RAM) to store the hash map. However once that is done, the execution of the join is pretty fast.

Hash join only usuable for equality condition. Example: `SELECT * FROM t1 JOIN t2 ON t1.c1 = t2.c2`


## Merge Join
In a merge join, we have two tables, each sorted by the columns we want to join on. Let's say we have:

* Table 1 (t1) sorted by column c1
* Table 2 (t2) sorted by column c2

Here's how the merge join works step-by-step:

1. Start with the first row from both t1 and t2.
2. Compare the values of c1 (from t1) and c2 (from t2).
    * If they are equal, it’s a match! We can join these rows together.
    * If c1 is smaller, we move to the next row in t1.
    * If c2 is smaller, we move to the next row in t2.
3. Repeat step 2 with the new rows until we reach the end of both tables.


Since the tables are sorted, we can continually keep searching forward to match rows. We don't need to look back at previously checked rows in both tables once they are checked. That makes this approach really efficient especially for large tables.

However, merge joins require both tables to be sorted on the joining columns, which can lead to a high startup cost if sorting is needed. However, if the joining column has an ordered index, PostgreSQL can skip the sorting step, as the index already maintains the required order.


## Examples
Let's create some tables and verify our assumptions.

```
-- create table t1 with random data
SELECT id, LEFT(MD(RANDOM()::text), 10) AS name
INTO t1
FROM generate_series(1, 50000) s(id)
ORDER BY RANDOM();

-- create table t2 using t1
SELECT id, name INTO t2
FROM t1
ORDER BY RANDOM()
```

Nested Loop Examples (Change this a photo & use krita to add comments and notes)
```
EXPLAIN VERBOSE
SELECT * FROM t1
INNER JOIN t2
    ON t1.id = t2.id
WHERE
    t1.name IN ('asdfasdf', 'asdfasdfd','asdfasdf23') AND
    t2.name IN ('asdf','asdff', '123','134');

                                    QUERY PLAN
-----------------------------------------------------------------------------------
 Nested Loop  (cost=0.00..1979.69 rows=1 width=30)
   Output: t1.id, t1.name, t2.id, t2.name
   Join Filter: (t1.id = t2.id)
   ->  Seq Scan on public.t2  (cost=0.00..1021.00 rows=4 width=15)
         Output: t2.id, t2.name
         Filter: (t2.name = ANY ('{asdf,asdff,123,134}'::text[]))
   ->  Materialize  (cost=0.00..958.51 rows=3 width=15)
         Output: t1.id, t1.name
         ->  Seq Scan on public.t1  (cost=0.00..958.50 rows=3 width=15)
               Output: t1.id, t1.name
               Filter: (t1.name = ANY ('{asdfasdf,asdfasdfd,asdfasdf23}'::text[]))
```

Hash Join Example:
```
EXPLAIN VERBOSE
SELECT * FROM t1
INNER JOIN t2
    ON t1.id = t2.id
WHERE
    t1.name IN ('asdfasdf', 'asdfasdfd','asdfasdf23');
                                    QUERY PLAN
-----------------------------------------------------------------------------------
 Hash Join  (cost=958.54..1917.07 rows=3 width=30)
   Output: t1.id, t1.name, t2.id, t2.name
   Hash Cond: (t2.id = t1.id)
   ->  Seq Scan on public.t2  (cost=0.00..771.00 rows=50000 width=15)
         Output: t2.id, t2.name
   ->  Hash  (cost=958.50..958.50 rows=3 width=15)
         Output: t1.id, t1.name
         ->  Seq Scan on public.t1  (cost=0.00..958.50 rows=3 width=15)
               Output: t1.id, t1.name
               Filter: (t1.name = ANY ('{asdfasdf,asdfasdfd,asdfasdf23}'::text[]))
```

Smaller table used for hashing and the other table is probed.

Merge Join Example: (This one needs to be checked more!!!)
```
postgres=# explain verbose select * from t1 inner join t2 on t1.id = t2.id;
                                 QUERY PLAN
----------------------------------------------------------------------------
 Merge Join  (cost=4425.32..49140.69 rows=2972897 width=72)
   Output: t1.id, t1.name, t2.id, t2.name
   Merge Cond: (t1.id = t2.id)
   ->  Sort  (cost=2212.66..2273.62 rows=24384 width=36)
         Output: t1.id, t1.name
         Sort Key: t1.id
         ->  Seq Scan on public.t1  (cost=0.00..435.84 rows=24384 width=36)
               Output: t1.id, t1.name
   ->  Sort  (cost=2212.66..2273.62 rows=24384 width=36)
         Output: t2.id, t2.name
         Sort Key: t2.id
         ->  Seq Scan on public.t2  (cost=0.00..435.84 rows=24384 width=36)
               Output: t2.id, t2.name
```


## Conclusion
In this blog, we explored different algorithms for joining tables in PostgreSQL. This information can be especially useful when you're interpreting query plans. Have you ever looked at a query plan and wondered what it all meant? After reading this blog, you'll have a better understanding of how PostgreSQL handles jions, helping you make sense of your query plans with more confidence.
