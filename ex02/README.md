# Count duplicates

5.25% of the rows are duplicated

```sql
SELECT count(*) AS total,
       count(*) - (SELECT count(*) FROM (SELECT DISTINCT * FROM customers) d) AS duplicados
FROM customers;
```

```sh
Password for user luicasad: 
  total   | duplicados 
----------+------------
 16532615 |     868444
(1 row)

real    0m 59.42s
user    0m 0.02s
sys     0m 0.01s
```

# show some duplicates

Some records appear up to 29 times.

```sql
SELECT event_time, event_type, product_id, price, user_id, user_session, count(*)
FROM customers
GROUP BY 1,2,3,4,5,6
HAVING count(*) > 1
ORDER BY count(*) DESC
LIMIT 20;
```

```sh
time psql -U luicasad -h localhost -d piscineds -c "SELECT event_time, event_type, product_id, price, user_id, user_session, count(*) FROM customers GROU
P BY event_time, event_type, product_id, price, user_id, user_session HAVING count(*) > 1 ORDER BY count(*) DESC LIMIT 20;"

       event_time       |    event_type    | product_id | price |  user_id  |             user_session             | count 
------------------------+------------------+------------+-------+-----------+--------------------------------------+-------
 2023-01-12 13:39:18+01 | remove_from_cart |    5700082 | 16.51 | 245068553 | 1bdcb724-31d4-4afb-b969-2d9862a96b2f |    29
 2022-11-21 19:46:01+01 | remove_from_cart |    5819114 |  0.67 | 527089613 | 11285886-37b7-4487-ba38-01ca9a01a271 |    23
 2022-12-17 17:32:26+01 | remove_from_cart |    5587744 |  1.59 | 578765531 | 18fba739-d6aa-447c-abe6-86ef8ce9102e |    20
 2022-11-15 15:08:23+01 | remove_from_cart |    5758984 |  1.49 | 559500288 | 1d2c4867-d62b-4326-beeb-ee17c0d1b825 |    20
 2022-11-29 16:31:05+01 | remove_from_cart |    5700032 |  0.38 | 559238872 | ef80e069-35c2-4af3-895f-1ee1a2cd0c4c |    19
 2022-11-08 16:18:56+01 | remove_from_cart |    5773392 |  1.43 | 539918440 | 018ee332-436a-44fe-96fc-c5318c5e2d5a |    19
 2022-12-25 13:29:33+01 | cart             |    5802433 |  0.35 | 543714981 | f581c117-5ba6-4e91-bdb5-b50ec01e28b7 |    19
 2023-01-30 15:27:55+01 | remove_from_cart |    5835947 |  2.06 | 429307612 | 94b62bff-deb1-4cb9-bac8-ee6b8b0b13e5 |    19
 2023-01-12 13:39:33+01 | remove_from_cart |    5700082 | 16.51 | 245068553 | 1bdcb724-31d4-4afb-b969-2d9862a96b2f |    19
 2022-10-18 17:25:34+02 | remove_from_cart |    5801339 |  6.35 | 492309267 | da2c3c3d-db4c-fcec-b25b-01a843475f9c |    19
 2023-01-12 13:39:18+01 | remove_from_cart |    5902798 |  1.94 | 245068553 | 1bdcb724-31d4-4afb-b969-2d9862a96b2f |    18
 2022-11-12 18:49:12+01 | cart             |       5310 |  0.40 | 405346718 | f0e2ae04-7ee3-4244-9ce5-ced188608371 |    17
 2022-11-04 12:32:17+01 | cart             |    5685678 |  0.32 | 444025079 | 544c668b-28d3-40d7-9c3d-61dfeec08509 |    17
 2023-01-12 13:38:48+01 | remove_from_cart |    5860160 |  0.78 | 245068553 | 1bdcb724-31d4-4afb-b969-2d9862a96b2f |    17
 2022-11-13 19:42:30+01 | remove_from_cart |    5764301 |  3.65 | 527739278 | 07989261-7478-4c32-a63e-ad4f3bfa8dee |    15
 2023-01-12 13:39:18+01 | remove_from_cart |    5839959 |  1.11 | 245068553 | 1bdcb724-31d4-4afb-b969-2d9862a96b2f |    15
 2023-01-22 13:01:04+01 | remove_from_cart |    5700037 |  0.40 | 443900126 | cd1f000e-44e7-4b91-819f-df0e61375bf8 |    15
 2023-01-05 09:27:06+01 | cart             |    5700032 |  0.40 | 521484087 | d3eb8591-a3ff-47a0-bd89-f739f22058c2 |    15
 2022-11-29 16:31:35+01 | remove_from_cart |    5700032 |  0.38 | 559238872 | ef80e069-35c2-4af3-895f-1ee1a2cd0c4c |    15
 2023-01-18 20:15:36+01 | cart             |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617 |    15
(20 rows)

real    0m 52.36s
user    0m 0.02s
sys     0m 0.01s
```
This confirms that the same record appears 15 times.

```sh
 psql -U luicasad -h localhost -d piscineds -c "SELECT ctid, * FROM customers WHERE event_time = '2023-01-18 20:15:36+01' AND event_type = 'cart' AND product_id = 5878933 AND price = 2.38 AND user_id = 597258708 AND user_session = '5b00800c-fd1b-405c-a4de-fc4cc049c617';"
     ctid     |       event_time       | event_type | product_id | price |  user_id  |             user_session             
-------------+------------------------+------------+------------+-------+-----------+--------------------------------------
 (116309,88) | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116309,89) | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116309,90) | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116309,91) | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116309,92) | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116309,93) | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116309,94) | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116309,95) | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116309,96) | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116310,1)  | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116310,2)  | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116310,3)  | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116310,4)  | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116310,5)  | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 (116310,6)  | 2023-01-18 20:15:36+01 | cart       |    5878933 |  2.38 | 597258708 | 5b00800c-fd1b-405c-a4de-fc4cc049c617
 ```
 

# Most convenient way to remove duplicate records

Context: the customers table holds 16,532,615 rows, of which 868,444 (about 5%) are exact duplicates across all six columns. The table has no foreign keys and no dependencies on other tables.

Recommended method: rebuild the table with SELECT DISTINCT.

Both approaches, rebuilding or deleting in place, must read and sort (or hash) all 16.5 million rows to find the duplicates, so that part of the cost is the same. The difference lies in what remains afterwards.

With an in-place DELETE, the deleted rows stay in the table file as dead tuples. VACUUM marks that space as reusable but does not shrink the file; reclaiming it requires VACUUM FULL, which rewrites the entire table again. In addition, every deleted row generates WAL (write-ahead log) records and updates to every index on the table.

With CREATE TABLE AS SELECT DISTINCT, the new table is written once, compactly, with no dead space. In practice this is usually faster than DELETE followed by VACUUM FULL, and the result is cleaner.

### The size of customers table

```sql
SELECT pg_size_pretty(pg_relation_size('customers'));
 pg_size_pretty 
----------------
 1207 MB
(1 row)
```


### Disk space available

PostgreSql 18 stores the data in `/var/lib/postgresql/18/data`

```sql
postgres=# SHOW data_directory;
       data_directory        
-----------------------------
 /var/lib/postgresql/18/data
(1 row)

postgres=# 
```
There are `18.6 GB` available in the hard disk `/dev/sda3` where is mounted the PostgreSql 's data folder.

```sh
/home/luicasad/ds # df -h /var/lib/postgresql/18/data
Filesystem                Size      Used Available Use% Mounted on
/dev/sda3                30.7G     10.6G     18.6G  36% /
```

## Virtual machine available memory
When only a sshd conection from visual studio code
```sh
              total        used        free      shared  buff/cache   available
Mem:           2556         668        1146         143         743        1598
Swap:          4096           0        4096
```

When logged with labwc GUI
```sh
              total        used        free      shared  buff/cache   available
Mem:           2556         243         533         143        1780        2011
Swap:          4096           0        4096
```

When logge with ssh
```sh
              total        used        free      shared  buff/cache   available
Mem:           2556         134         562         143        1860        2122
Swap:          4096           0        4096
```


This is the leanest configuration so far. With a plain SSH session (no labwc, no VS Code), only 134 MB are used and 2,122 MB are available.


|Scenario                                        |	  Used|Available|
|------------------------------------------------|--------|---------|
|Plain SSH from a terminal (no graphical session)|	134 MB|	2,122 MB|
|Local labwc session                             |	243 MB|	2,011 MB|
|SSH from VS Code                                |	668 MB|	1,598 MB|

The labwc session costs only about 110 MB, while the VS Code remote server costs over 500 MB. 
For heavy database operations on a small VM, a plain terminal SSH session is the best option.


EXPLAIN (ANALYZE, BUFFERS) SELECT count(*) FROM (SELECT DISTINCT * FROM customers);


### The size of customers table without duplicates
```sql
SELECT pg_size_pretty(pg_relation_size('customers'));
 pg_size_pretty 
----------------
 1144 MB
(1 row)
```

# Most convenient way to remove simultaneous records

First identify records almost duplicated, except by the fact of had been registred in differente moments.
I work with one that has 100 distinct entries
```sql
SELECT event_type, product_id, price, user_id, user_session, count(*) FROM customers GROUP BY 1,2,3,4,5 HAVING count(*) = 100 ORDER BY 6 DESC LIMIT 3;
 event_type | product_id | price |  user_id  |             user_session             | count 
------------+------------+-------+-----------+--------------------------------------+-------
 cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 |   100
 ```
Then i show all 100 entries
```sql
piscineds=# SELECT * FROM customers WHERE event_type = 'cart' AND product_id = '5809912' AND price = 5.24 AND  user_id = '570030304' ORDER BY event_time ;
```
|       event_time           | event_type | product_id | price |  user_id  |             user_session              |
|----------------------------|------------|------------|-------|-----------|---------------------------------------|
|   2022-12-12 07:19:56+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:19:57+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:19:58+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:19:59+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:20:00+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:20:01+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:20:45+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:20:46+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:28:17+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:28:20+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:37:43+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:37:47+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:37:51+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:38:02+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:38:34+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:38:53+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:38:54+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:38:57+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:38:58+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:39:00+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:39:01+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:39:05+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:39:06+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:39:07+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:39:12+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:39:13+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:39:32+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:39:33+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:39:48+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:39:51+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:39:54+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:39:56+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:40:01+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:42:20+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:44:55+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:46:52+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:46:54+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:46:55+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 07:46:56+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:46:58+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:47:00+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:47:07+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:47:15+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:47:22+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:50:19+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:55:22+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:55:28+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 07:55:36+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:00:32+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:00:52+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:00:55+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:00:56+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:00:57+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:00:58+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:00:59+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:01:00+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:01:01+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:01:03+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:01:04+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:01:05+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:01:08+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:01:09+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:01:10+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:01:11+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:01:13+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:01:14+01**   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:02:47+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:02:53+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:02:57+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:03:04+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:04:39+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:04:47+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:06:15+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:06:16+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:30:50+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:30:51+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:30:52+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:30:53+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:30:55+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:30:56+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:30:58+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:30:59+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:31:00+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 08:31:01+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 08:36:51+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 09:05:06+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 09:05:11+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 09:05:12+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 09:05:17+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 09:08:21+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 09:12:45+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 09:12:46+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 09:18:45+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 09:38:02+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 10:00:36+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 10:04:49+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 10:04:52+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 10:07:53+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
|   2022-12-12 10:08:49+01   | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |
| **2022-12-12 10:08:50+01** | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1  |

At hand i selected what i have to delete. 

Which SQL sentence produces same result?

```sql
FROM (
    SELECT *,
           event_time - LAG(event_time) OVER (
               PARTITION BY event_type, product_id, price, user_id, user_session
               ORDER BY event_time
           ) AS gap
    FROM customers
    WHERE user_session = '08d5a2ba-7a90-4a75-b26a-d8b602da0fd1'
      AND product_id   = 5809912
      AND event_type   = 'cart'
) t
WHERE gap <= interval '1 second'
ORDER BY event_time;
```


|       event_time       | event_type | product_id | price |  user_id  |             user_session             |   gap   |
|------------------------|------------|------------|-------|-----------|--------------------------------------|---------|
| 2022-12-12 07:19:57+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:19:58+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:19:59+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:20:00+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:20:01+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:20:46+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:38:54+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:38:58+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:39:01+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:39:06+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:39:07+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:39:13+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:39:33+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:46:55+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 07:46:56+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:00:56+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:00:57+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:00:58+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:00:59+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:01:00+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:01:01+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:01:04+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:01:05+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:01:09+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:01:10+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:01:11+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:01:14+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:06:16+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:30:51+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:30:52+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:30:53+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:30:56+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:30:59+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:31:00+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 08:31:01+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 09:05:12+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 09:12:46+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|
| 2022-12-12 10:08:50+01 | cart       |    5809912 |  5.24 | 570030304 | 08d5a2ba-7a90-4a75-b26a-d8b602da0fd1 | 00:00:01|



Which sql sentence counts records to remove from this customer?

```sql
SELECT count(*) 
FROM (
    SELECT *,
           event_time - LAG(event_time) OVER (
               PARTITION BY event_type, product_id, price, user_id, user_session
               ORDER BY event_time
           ) AS gap
    FROM customers
    WHERE user_session = '08d5a2ba-7a90-4a75-b26a-d8b602da0fd1'
      AND product_id   = 5809912
      AND event_type   = 'cart'
) t
WHERE gap <= interval '1 second';
 count 
-------
    38
(1 row)
```

which SQL sentence counts how many duplicates to remove?

```sql
piscineds=# SELECT count(*)
FROM (
    SELECT *,
           event_time - LAG(event_time) OVER (
               PARTITION BY event_type, product_id, price, user_id, user_session
               ORDER BY event_time
           ) AS gap
    FROM customers
    ) t
WHERE gap <= interval '1 second';
 count  
--------
 329888
(1 row)
```