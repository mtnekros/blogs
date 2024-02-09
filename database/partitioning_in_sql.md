# Partitioning in PostgreSQL
There are times when we come across tables that grows to millions and billion
rows. One of the ways we can deal with this problem is partitioning. In this blog,
we will learn about how to parition a table and advantages and disadvantages of
paritioning.

> Paritioning refers to splitting what is logically one large table into smaller physical pieces.

## Why do we do this?
* Performance: Partitioning, when utilzed properly, can make queries a lot
  faster. Because instead of scanning the entire tables, we only have to scan
  the smaller subsets.
* Load balancing and scalibility: If you have a large and growing dataset,
  partitioning can help distribute a large table across multiple smaller tables
  (or multiple disks or entirely different servers), improving performance and
  scalability.
* Efficient data management: Paritioning simplifies backup, archiving and
  deletion of specific data subsets. If a table is partitioned on a date column
  using quarterly or monthly data, we can bulk load or delets data by adding
  and removing paritions. However, date column is just an example, by choosing
  and effective column, we can simply archiving and deleting. As instead of
  scanning the whole table we will be deleting just the parition (which is a
  table under the hood).
* Massive tables: Dividing them into manageable chunks improves performance and
  makes data management easier.
* Time-based data: Partition by date (year, month, day) for efficient
  historical analysis and archiving.
* Frequently accessed subsets: Partition by frequently queried data to optimize
  query speed.
* Data with varying characteristics: Tailor partitions to specific data types
  or access patterns for even better performance.

> **Note**: "The exact point at which a table will benefit from partitioning depends
> on the application, although a rule of thumb is that the size of the table
> should exceed the physical memory of the database server."

## In PostgreSQL, we have 3 built-in forms of partitioning.
* Range Partitioning: Suppose we have age column in a customer column, we can
  have 4 partitions containing records with age, 0-30yrs, 30 to 50 and 50 to
  70, 70 to `MAX_VALUE`. This is an example of range partitioning which is
  ideal for time-series data or ordered datasets.
* List Partitioning: The table will be partitioned based on specific values
  in one of it's column. E.g.: regions, product categories. It is good for
  categorical data or filtering specific groups.
* Hash Partioning: Each partition will hold the rows for which the hash value
  of the partitioning key divided by the specified modulus will produce the
  specified remainder. This will ensure the rows will be distributed evenly
  across partitions but the filtering might not be as efficient as compared to 
  the other two types.

## Considerations:
* Query Patterns: First, we need to analyze your most frequent queries.
  Paritioning will only benefit queries that leverage the parititioning
  column(s) effectively. If the where clauses don't include the partitioning
  column(s), we might be better off without the partitioning. *And if retrival
  speed is the sole reason for partitioning, we might be better off with just
  indexing.*
* Partitioning Granularity: Too many or too few partitions can impact
  performance. We need to choose a granularity that balances efficiency and
  manageability.
* Partition Maintenance: Decide on strategies for handling new data as it
  arrives and how to rebalance partitions over time to avoid skewed workloads.
  Additionally, we also have to consider archiving or deleting old data as
  well.

## Creating a partiioned table
* Declare the column and the method of partitioning during table creation:
```sql
 CREATE TABLE sales (
  order_id INT PRIMARY KEY,
  customer_id INT,
  order_date DATE NOT NULL,
  sales_amount DECIMAL(10,2)
)
PARTITION BY RANGE (order_date);
```
* Add partitions:
```sql
CREATE TABLE sales_2023q1 PARTITION OF sales FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');
CREATE TABLE sales_2023q2 PARTITION OF sales FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');
CREATE TABLE sales_2023q3 PARTITION OF sales FOR VALUES FROM ('2023-07-01') TO ('2023-10-01');
CREATE TABLE sales_2023q4 PARTITION OF sales FOR VALUES FROM ('2023-10-01') TO ('2024-01-01');
```
* Select queries work as normal but we want to leverage the partitioning column.
```
-- normal query
SELECT * FROM sales WHERE customer_id = 12;;
-- leveraging partitioning column
SELECT * FROM sales WHERE order_date = '2023-10-01' and customer_id = 12;
```


## Partitioning an existing table
There is no way in PostgreSQL to add partitioning to an already existing
unpartitioned table. We have to create a new partitioned table and import the
data from the unpartitioned table to the new partitioned one.
1. Backup your data: Safety first!
2. Create a new, partitioned table: Define the desired scheme.
3. Transfer data: Move data from the old table to the new one, following your partition scheme.
4. Switch over: Make the new table the active one.


Bonus Tip: Regularly monitor and maintain your partitions. Archive, drop, or
reorganize them as needed to keep your data kingdom optimized and efficient.

Remember, the best partitioning strategy depends on your specific data and
needs. Experiment, explore, and conquer those large tables with confidence!
