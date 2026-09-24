import psycopg
import sys
import os


def main():
    sql0 = psycopg.sql.SQL("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name ~ 'data_202[0-9]_[a-z]{3}';
    """)
    union = psycopg.sql.SQL("""
        CREATE TABLE customers AS
    """)

    with psycopg.connect(
        host="127.0.0.1", port=5432, dbname="piscineds", user="luicasad"
    ) as conn:
        with conn.cursor() as cur:
            # cur.execute("SELECT version();")
            cur.execute(sql0)
            tables = [ table[0] for table in cur.fetchall()]
            if not tables:
                raise SystemExit("No se encontraron tablas con el patrón")

            union = psycopg.sql.SQL(" UNION ALL ").join(
                [psycopg.sql.SQL("SELECT * FROM {}").format(
                    psycopg.sql.Identifier(t)
                    ) 
                    for t in tables]
                )
            sql1 = psycopg.sql.SQL("CREATE TABLE customers AS ") + \
                union + \
                psycopg.sql.SQL(";")
            print(sql1.as_string(conn))

            try:
                cur.execute(sql1)
                print(f"Union of tables created succesfully")
                conn.commit()        
                cur.execute(f"SELECT COUNT(*) FROM customers;")
                rows_imported = cur.fetchone()[0];
                print(f"Table customers populated succesfully with {rows_imported} rows")
            except Exception as e:
                conn.rollback()
                print(f"Error importing {table_path}: {e}")
            finally:
                cur.close()
                conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("python ./custome_table.py")
        sys.exit(1)
    main()

