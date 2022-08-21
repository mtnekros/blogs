![fixed value fields](./images/enums.png)
<h1 style="text-align: center">Enums in postgresql </h1>


<h2 style="text-align: center">The need for enum types</h2>
Ever been in a situation when you need to have finite specific values in one
of the columns in your table? I was in a similar siutation. I needed to track
the status of some process. And the following are the posible solutions:

## The solutions
1. If you really don't care or in a real hurry, you can create a text column and
make sure everyone inserts/updates the column with the fixed, prespecified values. 
2. If you really care about consistency, you could just create a foreign table
where you store all those data and reference it by a foreign key. This is a
better solution. But there's is something much better for static values that isn't
going to be updated a lot.
3. You could use custom enumerated types. It's like creating a foreign table with
constants but much better without all the hassles.

## So what is an enum?
> Enumerated (enum) types are data types that comprise a static, ordered set of
> values. They are equivalent to the enum types supported in a number of
> programming languages. An example of an enum type might be the days of the week,
> or a set of status values for a piece of data.

In this blog, we are just going to go over how to create and use this enums in
postgresql

## 1. Creating a custom enumerated type
In this particular example, we are going to create an enum for tracking status
of any process.

```sql
CREATE TYPE public.status AS ENUM ('pending', 'in process', 'completed');
-- that's how easy it is to create an enum.
-- Note: that the order that they are laid out in does matter and you can do comparisons based on their order. More on this later
```
This will create a new type called status in the public schema and now you can
use this as your datatype when creating columns.

## 2. Creating a table that uses that enum
Next, let's create a table to track the status of different process in using the
enum as type of one of the columns.
```sql
CREATE TABLE public.process_tracker (
    id SERIAL PRIMARY KEY,
    batch_id integer
    process_name text,
    process_status status
)
```

## 3. Inserting data into the process_tracker
```sql
INSERT INTO public.process_tracker
    (batch_id, process_name, process_status)
VALUES 
    (140, 'text-processing', 'pending'),
    (140, 'video-processing', 'in process'),
    (140, 'web-processing', 'in process'),
    (140, 'image-processing', 'completed');
```

Table:
|id (serial)|batch_id(integer)|process_name(text)|process_status(status)|
|-----------|-----------------|------------------|----------------------|
|1 |     140|text-processing  |pending|
|2 |     140|video-processing |in process|
|3 |     140|web-processing |processing|
|4 |     140|image-processing |completed|

## 4. Inserting/Updating the process_status column with wrong values?
Now if you try to update/insert the process_status column with incorrect values,
you will get an error.
```sql
INSERT INTO public.process_tracker
    (batch_id, process_name, process_status)
VALUES
    (140, 'text-processing', 'asdf');
```
```log
ERROR:  invalid input value for enum status: "asdf"
LINE 3:  ('text', 'asdf')
                  ^
SQL state: 22P02
Character: 60
```

>It's always good to never have an option to make an error instead of just trying to
>be careful not to make that error.  With enums that's possible without the
>headache having to create a different table and foreign key constraint.

### 5. Altering the enum type values
Another benefit of using an enum is, if you want to change the enum values you can change the name
and they will be reflected in all the records that use that value automatically.

```sql
ALTER  TYPE public.status RENAME VALUE 'in process' TO 'processing';
```

Now the table will look like this
|id (serial)|batch_id(integer)|process_name(text)|process_status(status)|
|-----------|-----------------|------------------|----------------------|
|1 |     140|text-processing  |pending|
|2 |     140|video-processing |processing|
|3 |     140|web-processing |processing|
|4 |     140|image-processing |completed|

## Conclusion:
Therefore, never use text fields for columns that have option/choice values. If
they are going to be dynamic and keep changing a lot or you just have a long
list of choices, then a foreign table is the way to go. But if you have finite
values for a column in a table that aren't going to change, go with enums.

## References
* [Postgresql Enum documentations](https://www.postgresql.org/docs/current/datatype-enum.html)
* [More information on ALTER TYPE](https://www.postgresql.org/docs/current/sql-altertype.html)
