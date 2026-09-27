import psycopg
import sys
import os


def main():
    sql0 = psycopg.sql.SQL("""
        SET work_mem = '512MB';
        SET max_parallel_workers_per_gather = 0;

        CREATE TABLE customers_new AS
        SELECT DISTINCT *
        FROM customers;
            """)
    sql1 = psycopg.sql.SQL("DROP TABLE customers;")

    sql2 = psycopg.sql.SQL("""CREATE TABLE customers AS
        SELECT event_time, event_type, product_id, price, user_id, user_session
        FROM (
            SELECT *,
                event_time - LAG(event_time) OVER (
                    PARTITION BY event_type, product_id, price, user_id, user_session
                    ORDER BY event_time
                ) AS gap
            FROM customers_new
        ) t
        WHERE gap IS NULL OR gap > interval '1 second';""")
    sql3 = psycopg.sql.SQL("DROP TABLE customers_new;")

    with psycopg.connect(
        host="127.0.0.1", port=5432, dbname="piscineds", user="luicasad"
    ) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"SELECT COUNT(*) FROM customers;")
                exist = cur.fetchone()[0];
                print(sql0.as_string(conn))
                cur.execute(sql0)  # removes identical records
                cur.execute(f"SELECT COUNT(*) FROM customers_new;")
                remai = cur.fetchone()[0];
                print(f"From {exist} records, {exist - remai} duplicates removed succesfully")
                cur.execute(sql1)  # deletes table customer
                cur.execute(sql2)  # removes SIMULTENEOUS records
                cur.execute(f"SELECT COUNT(*) FROM customers;")
                exist = cur.fetchone()[0];
                print(f"Additionally, {remai - exist} 'Simultaneous' records' removed succesfully") 
                cur.execute(sql3)  # deletes table custoners_new
                conn.commit()     
            except Exception as e:
                conn.rollback()
                print(f"Error removing duplicates from customers: {e}")
            finally:
                cur.close()
                conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("python ./remove_duplicates.py")
        sys.exit(1)
    main()

