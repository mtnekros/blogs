# Partitioning in PostgreSQL
There are times when we come across tables that grows to millions and billion
rows. One of the ways we can deal with this problem is partitioning. In this
blog, we will learn about how to parition a table and advantages and
disadvantages of paritioning. We will only be delving into declarative
partitioning.

> Paritioning refers to splitting what is logically one large table into
> smaller physical pieces.

## Why do we do this?
1. Performance: Partitioning, when utilzed properly, can make queries a lot
   faster. Because instead of scanning the entire tables, we only have to scan
   the smaller subsets. By partitioning based on frequently queried columns, we
   can optimize query speed.
2. Load balancing and scalibility: If you have a large and growing dataset,
   partitioning can help distribute a large table across multiple smaller
   tables (or multiple disks or entirely different servers), improving
   performance and scalability.
3. Efficient data management: Paritioning simplifies backup, archiving and
   deletion of specific data subsets. If a table is partitioned on a date
   column using quarterly or monthly data, we can bulk load or delets data by
   adding and removing paritions. However, date column is just an example, by
   choosing and effective column, we can simply archiving and deleting. As
   instead of scanning the whole table we will be deleting just the parition
   (which is a table under the hood).
4. Data with varying characteristics: Tailor partitions to specific data types
   or access patterns for even better performance.

Note: "The exact point at which a table will benefit from partitioning depends
on the application, although a rule of thumb is that the size of the table
should exceed the physical memory (RAM)hof the database server."

## In PostgreSQL, we have 3 built-in forms of partitioning.
1. Range Partitioning: Suppose we have age column in a customer column, we can
   have 4 partitions containing records with age, 0-30yrs, 30 to 50 and 50 to
   70, 70 to `MAX_VALUE`. This is an example of range partitioning which is
   ideal for time-series data or ordered datasets.
2. List Partitioning: The table will be partitioned based on specific values in
   one of it's column. E.g.: regions, product categories. It is good for
   categorical data or filtering specific groups.
3. Hash Partioning: In this method, each partition will contain rows determined
   by dividing the hash value of the partitioning key by a specified modulus
   and then checking if it produces a specified remainder. This approach aims
   to evenly distribute rows across partitions. However, it's worth noting that
   filtering data in hash-partitioned tables may not be as efficient as in
   tables partitioned using other methods.

Note: Hashing is a process of mapping data of arbitrary size to fixed-size values. The algorithm aims to generate a unique hash value for each unique input while minimizing the likelihood of collisions (two inputs producing the same hash value). PostgreSQL doesn't specify which specific has function it uses internally, but it has to be a hash function optimized for performance and good distribution of hash values across partitions, such as MurmurHash, FarmHash, etc.

## Considerations:
1. Query Patterns: First, we need to analyze your most frequent queries.
   Paritioning will only benefit queries that leverage the parititioning
   column(s) effectively. If the where clauses don't include the partitioning
   column(s), we might be better off without the partitioning. *And if retrival
   speed is the sole reason for partitioning, we might be better off with just
   indexing.*
2. Partitioning Granularity: Too many or too few partitions can impact
   performance. We need to choose a granularity that balances efficiency and
   manageability.
3. Partition Maintenance/Skewed Partitions: Decide on strategies for handling
   new data as it arrives and how to rebalance partitions over time to avoid
   skewed workloads. Because if one of the partition holds most of the data,
   queries in that partition won't be very effective. Additionally, we also
   have to consider archiving or deleting old data as well.

## Creating a partiioned table
### Range Partitioning
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
```sql
-- normal query
SELECT * FROM sales WHERE customer_id = 12;;
-- leveraging partitioning column
SELECT * FROM sales WHERE order_date = '2023-10-01' and customer_id = 12;
```
### List Partitioning
```sql
CREATE TABLE public.products (
    product_id serial,
    product_name character varying(100),
    category character varying(50) NOT NULL,
    price numeric
)
PARTITION BY LIST (category);
```
* Add partitions
```sql
CREATE TABLE products_foods PARTITION OF products
FOR VALUES IN ('Food', 'Kitchen');
CREATE TABLE products_clothing PARTITION OF products
FOR VALUES IN ('Shirts', 'Dresses');
```
### Hash Partitioning
* Create table
```sql
CREATE TABLE orders (
    order_id SERIAL,
    customer_id INT,
    product_id INT,
    quantity INT,
    total_amount DECIMAL(10, 2)
) PARTITION BY HASH(order_id);
```
* Add partitions
```
CREATE TABLE orders_partition_1 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE orders_partition_2 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

CREATE TABLE orders_partition_3 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);

CREATE TABLE orders_partition_4 PARTITION OF orders
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);

-- The MODULUS 4 part indicates that we're dividing the hash space into 4
-- partitions. The REMAINDER x part specifies which portion of the hash space each
-- partition will cover. Each partition covers a range of hash values based on
-- their remainders when divided by 4. For example, orders_partition_1 covers hash
-- values where hash(order_id) % 4 = 0, orders_partition_2 covers hash values
-- where hash(order_id) % 4 = 1, and so on. By using hash partitioning, we
-- distribute the data across multiple partitions based on the hash value of the
-- order_id column. This can help in achieving better performance by evenly
-- distributing the data and reducing contention on specific partitions.
```

## Attaching and detaching partitions
```sql
-- detaching partition
ALTER TABLE public.products DETACH PARTITION products_foods;
-- attaching partition
ALTER TABLE ONLY public.products ATTACH PARTITION public.products_foods
FOR VALUES IN ('Food', 'Snacks');
```

## Partitioning an existing table
There is no way in PostgreSQL to add partitioning to an already existing
unpartitioned table. We have to create a new partitioned table and import the
data from the unpartitioned table to the new partitioned one.
1. Backup your data: Safety first!
2. Create a new, partitioned table: Define the desired scheme.
3. Transfer data: Move data from the old table to the new one, following your
   partition scheme.
4. Switch over: Make the new table the active one.


Bonus Tip: Regularly monitor and maintain your partitions. Archive, drop, or
reorganize them as needed to keep your data kingdom optimized and efficient.
Remember, the best partitioning strategy depends on your specific data and
needs. Experiment, explore, and conquer those large tables with confidence!

