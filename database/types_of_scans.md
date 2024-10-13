# Did you know: that PostgreSQL doesn't always use the index to filter by an indexed column?
**An explanation of different ways PostgreSQL scan a table querying.**

## What is an index?

Without an index, we have to scan the table to search for a value. An index helps you to locate matching rows more quickly. It is a mapping from row values to tuple identifiers (TIDs). TIDs are a like pointer to the row of the table.

Tables are stored in the disk in blocks/pages. Each block holds several rows. To read a particular row, we first need to load the block into memory and iterate through the rows in that block to get to a particular record. Tuple Identifiers hold the information of the block number and item number, with which we can easily identify that row.

## A simplified represention of indices in python

Let's create a table as follows to use in our examples:
```
-- creating the table
create table persons(
  id serial not null,
  name varchar(255) not null,
  age int
);

-- creating the index on name column
create index persons_name_idx on persons(name);


-- table information "public.persons"
 Column |     Type     | Nullable |               Default
--------+--------------+ ---------+------------------------------------
 id     | integer      | not null | nextval('persons_id_seq'::regclass)
 name   | varchar(255) | not null |
 age    | integer      |          |

Indexes:
    "persons_name_idx" btree (name)
```

This is a simplified version of the value that the index will hold. It is a mapping from the values of the name column to its location in the disks.


```python
persons_name_idx = {
  "Diwash": [{"block_number": 0, "item_number": 12},],
  "Moderick": [{"block_number": 0, "item_number": 12},],
  "Mohammed": [ # example of collision
    {"block_number": 1, "item_number": 2},
    {"block_number": 10, "item_number": 2}
   ],
}
```

>> Note: All indexes in PostgreSQL are stored in a separate physical location from the table file it describes. 

I always thought that using the index was always better. But turns out my life was a lie and that isn't the case. The use of an index is determined based on the distribution of the values of the indexed column.

To simulate the 3 different conditions for the 3 different scans, we have to create the following 3 distinct sets of records.

* 80% of the records with the same name 'Mohammed'
* 15 % of the records with the same name 'Maria'
* 5 % of the records with unique names

```sql
-- 80 % data with same name 'Mohammed'
insert into persons(name, age)
select 'Mohammed' as name, i%50 + 1 as age
from generate_series(1, 8000) s(i);

-- 15 % of the records with same name 'Maria'
inser into persons(name, age)
select 'Maria' as name, i%50 + 1 as age
from generate_series(1, 1500) s(i);

-- some record with unique names
insert into persons(name, age)
select concat('unique', i::text) as name, i%50 + 1 as age
from generate_series(1, 500) s(i);
```

Running a group by on the indexed column name, shows the following output.

```sql
select name, count(*) from persons
group by name order by count(*) desc limit 5;

Output:
   name    | count
-----------+-------
 Mohammed  |  8000
 Maria     |  1500
 unique429 |     1
 unique205 |     1
 unique204 |     1
```

## Sequential Scan:
This is the simplest scan where each row is read sequentially from the disk. There's no preparation cost for this. (As you would have with for example index scan to load the index into memory before querying the table).

**Preferred Condition**:
Used when the majority (40 & above or so) of the rows will pass the filter. If almost all rows satisfy the index condition, then there's no point in using the index. We will be loading the index and then again going through the majority of the rows. So a sequential scan is better in this case.

Example:
```
QUERY:
explain (analyze, verbose)
select * from persons
where name = 'Mohammed';

                          QUERY PLAN
-----------------------------------------------------------------------------------------------------------------
 Seq Scan on public.persons  (cost=0.00..187.69 rows=8400 width=16) (actual time=0.019..1.215 rows=8000 loops=1)
   Output: id, name, age
   Filter: ((persons.name)::text = 'Mohammed'::text)
   Rows Removed by Filter: 2000
 Planning Time: 0.083 ms
 Execution Time: 1.438 ms
```
As you can see in the query plan, a sequential scan (Seq Scan) was used.

## Index Scan:
Index scan as the name suggests will make use of the index to retrieve the scan. The engine will load the index into memory, to check the location of the filtered rows in the index and then retrieve the records from the actual table one by one.

*Preferred When:*
When there is a relatively low number of return values. Meaning the filter conditions only match a few rows.

>>Note: Indexes are not directly aware that under MVCC, there may be multiple extant versions of the same logical row; to an index, each tuple is an independent object that needs its own index entry. Thus, an update of a row always creates all-new index entries for the row, even if the key values did not change. Index entries for dead tuples are reclaimed (by vacuuming) when the dead tuples themselves are reclaimed.

Example:
```sql
QUERY:
explain (analyze, verbose)
select * from persons where name = 'unique1';

                        QUERY PLAN
----------------------------------------------------------------------------------------------------------------------------------
 Index Scan using persons_name_idx on public.persons  (cost=0.29..8.14 rows=1 width=16) (actual time=0.021..0.022 rows=1 loops=1)
   Output: id, name, age
   Index Cond: ((persons.name)::text = 'unique1'::text)
 Planning Time: 0.072 ms
 Execution Time: 0.034 ms
```

## Index-Only Scan:
When we have a query like, SELECT indexed_column FROM table WHERE indexed_column = 'somevalue', all the information is available in the index. As the index stores the values of the indexed column, it doesn't need to look into the table for anything. That makes this one of the most efficient scans you can perform.

*Preferred When*:
* When only the indexed column is returned and the where clause also only uses the indexed column.
* When only the index column is returned and there's an order by the index. (This is useful when we have an index type that is ordered by design. For eg: BTree, which is also the deafult index type)

Example 1:
```sql
explain (analyze, verbose) select name from persons order by name;

                             QUERY PLAN
-----------------------------------------------------------------------------------------------------------------------------------------------
 Index Only Scan using persons_name_idx on public.persons  (cost=0.29..221.54 rows=9975 width=8) (actual time=0.017..0.867 rows=10000 loops=1)
   Output: name
   Heap Fetches: 512
 Planning Time: 0.075 ms
 Execution Time: 1.142 ms
```

As you can see, we are using index-only scan here.

## Bitmap Scan:
Bitmap Scan can be called somewhat of a middle ground between index scan and sequential scan. 
It involves two separate types of scans. First, the engine scans the index and creates bitmap of matching rows. Then, the engine will use that bitmap to fetch the rows from the table in batches. This is different from normal index scan which will check the index and look for a single row one at a time.

There are possibly 3 steps of a bit map scan:
1. First, we have the Bitmap Index Scan which scans the indexes and creates an in-memory bitmap of matching rows. Example: 001 000 111 000 101
2. Optional Step: In case the filter clause contains conditions on two indexed columns (where indexed_col1 = 'someval' and indexed_col2 = 'someotherval'), the engine will create two different bitmaps and perform bitwise AND and OR operations on the two bitmaps to further filter the final output efficiently.
3. Once the complete bitmap is created, the engine will perform the Bitmap Heap Scan. This will scan the rows in the table sequentially, fetch all rows that are marked as 1 in the bitmap and skip the ones marked with 0. It will also skip whole blocks/pages if the bitmap value for the whole page is 0. This means we retrieve only relevant rows without scanning the whole table.

**Preferred When**:
* It is usually preferred when the filtered output rows are around 5–30% of the total rows. It's better than the index scan in case of a greater number of output rows.
* When there is a filter condition that involves two or more indexed columns. Because it can perform bitwise AND OR operations to efficiently filter the rows, once the bitmap for each index column is created using the Bitmap Index Scan.
Example:
```sql
QUERY: 
explain (analyze, verbose) select * from persons where name = 'Maria';

                           QUERY PLAN
--------------------------------------------------------------------------------------------------------------------------------
 Bitmap Heap Scan on public.persons  (cost=24.49..107.18 rows=1575 width=16) (actual time=0.077..0.183 rows=1500 loops=1)
   Output: id, name, age
   Recheck Cond: ((persons.name)::text = 'Maria'::text)
   Heap Blocks: exact=10
   ->  Bitmap Index Scan on persons_name_idx  (cost=0.00..24.10 rows=1575 width=0) (actual time=0.069..0.069 rows=1500 loops=1)
         Index Cond: ((persons.name)::text = 'Maria'::text)
 Planning Time: 0.104 ms
 Execution Time: 0.255 ms
```

## Conclusion:
We looked at different types of scans, namely Sequential Scan, Index Scan, Index-Only Scan, Bitmap Scan. We also looked when different types of scan is preferred by the query planner using the explain analyze query. 

Thank you for reading! If you learnt something new from the blog, please leave us some claps.
