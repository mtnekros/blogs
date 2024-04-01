# Understanding Dead Tuples

In database systems, dead tuples are rows that are no longer required or relevant to ongoing operations. These tuples are created during updates and deletions. When a row is updated or deleted, the old version of the row is marked as inactive or logically deleted, resulting in a dead tuples. Although dead tuples still occupy space within the database, they are not visible to queries or transactions as active data.

# Why are dead tuples created then?
Why can't we just delete the row instead of marking them as deleted? Why do we keep the old version of the row instead of just updating the existing ones?
1. MVCC (Multi-Version Concurrency Control):
When a database is accessed from multiple users/places, we need a way to read and write to the database concurrently without interfering each other.  Say, person person A is trying to update a record in the table. Person B & C are querying for a record in a table at the same time. Before MVCC, the update transaction would lock the record until the it's completed and perons B & C would have to wait for it. With MVCC, instead of locking the record entirely, we create a new version of the record. B & C would receive the highest version of the record at the time of their query instantly (.i.e. version before the update as it's still going on). While person C would create a new higher version of the record with their update query. Any queries after this, will received the newly updated version of the row. This significantly boosts the speed of the database, while still maintaining data integrity. This also follows the rule that transactions should provide isolation and atomicity, ensuring that changes made by one transaction are not visible to other transactions until they are commited. And the older version of the record now becomes the dead tuple.

Same thing happens with delete queries as well. Only difference being instead of creating a newer version of the record, delete only marks the older version as inactive or as a dead tuple.

Additionally, if a transaction is rolled back or aborted, the changes made by that transaction may result in dead tuples. Keeping the dead tuples allow the system to maintain transactional consistency and rollback changes if necessary.

## The problem with dead tuples
While dead tuples offer clear benefits, their continued presence can lead to drawbacks:

* Storage inefficiency: Dead tuples, though not visible to queries, still occupy storage space. This can inflate the database size unnecessarily, impacting storage costs and performance.
* Query performance: As the number of dead tuples increases, queries may take longer to execute as they need to shift through both active and inactive data.

## What is vacuuming?
Vacuuming is a database maintenance process that reclaims the storage space
occupied by dead tuples. It essentially cleans up the database by removing
these inactive records, optimizing storage efficiency and potentially improving
query performance.

## Types of vacuuming in PostgreSQL
PostgreSQL offers different vacuuming options, each with varying
functionalities:

* VACUUM: This basic vacuum process removes dead tuples and updates table
  statistics. However, it leaves behind any leftover bloat (unused space)
  within the table.
* VACUUM FULL: This more intensive process performs a full table rewrite,
  removing dead tuples, reclaiming all available space, and updating table
  statistics. It's generally performed less frequently than VACUUM due to its
  resource-intensive nature.
* CLUSTER: This advanced option rearranges table data physically, potentially
  improving query performance for certain access patterns. However, it's not a
  substitute for regular vacuuming.

## Why can't we delete the dead tuples immediately after there are no references to them left?
There are a few reasons why immediate deletion of dead tuples isn't ideal:

* Performance impact: Continuously deleting individual dead tuples can be more
  resource-intensive than periodically performing a bulk vacuum operation.
* Concurrency challenges: Deleting tuples concurrently while other transactions
  are accessing the table can lead to inconsistencies and data corruption.
* Transactional consistency: As mentioned earlier, dead tuples are crucial for
  rolling back transactions and ensuring data integrity. Immediate deletion
  would compromise this functionality.

By implementing a scheduled vacuuming routine, you can balance the benefits of
MVCC and rollback functionality with the need for efficient storage and optimal
query performance.


References:
https://cloud.google.com/blog/products/databases/deep-dive-into-postgresql-vacuum-garbage-collector
