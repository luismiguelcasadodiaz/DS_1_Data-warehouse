import psycopg

tables = ['uno','dos','tres']

aux = [psycopg.sql.Identifier(t) for t in tables]
print(aux)

aux2 = [psycopg.sql.SQL("SELECT * FROM {}").format(psycopg.sql.Identifier(t)) for t in tables]
print(aux2)

union = psycopg.sql.SQL(" UNION ALL ").join(aux2)
print(union)

union = psycopg.sql.SQL(" UNION ALL ").join([psycopg.sql.SQL("SELECT * FROM {}").format(psycopg.sql.Identifier(t)) for t in tables])

sql1 = psycopg.sql.SQL("CREATE TABLE customers AS ") + union + psycopg.sql.SQL(";")
print(sql1)
with psycopg.connect("dbname=piscineds user=luicasad password=mysecretpasswd host=localhost") as conn:
    print(sql1.as_string(conn))