import psycopg
import sys


def main():
    sql0 = psycopg.sql.SQL("""
        SET work_mem = '512MB';
        SET max_parallel_workers_per_gather = 0;

        CREATE TABLE join_customer_items AS
            SELECT c.event_time, c.event_type, c.product_id, i.category_id,
                c.user_id, c.user_session, c.price, i.category_code, i.brand
        FROM customers AS c
        LEFT JOIN (
            SELECT product_id,
                MAX(category_id)   AS category_id,
                MAX(category_code) AS category_code,
                MAX(brand)         AS brand
            FROM items
            GROUP BY product_id
        ) AS i ON c.product_id = i.product_id;
            """)
    sql1 = psycopg.sql.SQL("DROP TABLE customers;")
    sql2 = psycopg.sql.SQL("""ALTER TABLE join_customer_items
                           RENAME TO customers;""")

    with psycopg.connect(
        host="127.0.0.1", port=5432, dbname="piscineds", user="luicasad"
    ) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT COUNT(*) FROM customers;")
                before = cur.fetchone()[0]
                print(sql0.as_string(conn))
                cur.execute(sql0)  # Executes join
                cur.execute("SELECT COUNT(*) FROM join_customer_items;")
                after = cur.fetchone()[0]
                print(f"Before: {before} records. After: {after} records.")
                cur.execute(sql1)
                cur.execute(sql2)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(f"Error joining customerer wiht items: {e}")
            finally:
                cur.close()
                conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("python ./remove_duplicates.py")
        sys.exit(1)
    main()
