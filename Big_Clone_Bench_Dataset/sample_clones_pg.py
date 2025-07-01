import json
import psycopg2

print("Starting sampling…")
conn = psycopg2.connect(dbname="bcb") 
cur  = conn.cursor()

# Each tuple is (SQL condition on clones, output-file suffix)
CATS = [
    ("syntactic_type = 1",                                           "T1"),
    ("syntactic_type = 2",                                           "T2"),
    ("syntactic_type = 3 AND similarity_line >= 0.9",                "VST3"),
    ("syntactic_type = 3 AND similarity_line >= 0.7 AND similarity_line < 0.9", "ST3"),
    ("syntactic_type = 3 AND similarity_line >= 0.5 AND similarity_line < 0.7", "MT3"),
    ("syntactic_type = 3 AND similarity_line < 0.5",                 "WT3_T4"),
]

for condition, suffix in CATS:
    print(f"Sampling 300 for {suffix}…")
    cur.execute(f"""
        SELECT c.function_id_one,
               c.function_id_two,
               p1.text AS code1,
               p2.text AS code2
          FROM clones c
          JOIN pretty_printed_functions p1
            ON p1.function_id = c.function_id_one
          JOIN pretty_printed_functions p2
            ON p2.function_id = c.function_id_two
         WHERE {condition}
         ORDER BY random()
         LIMIT 300
    """)
    rows = cur.fetchall()
    out_file = f"{suffix}_300.jsonl"
    with open(out_file, "w") as fp:
        for m1, m2, c1, c2 in rows:
            json.dump({
                "clone_type":  suffix,
                "method1_id":  m1,
                "method2_id":  m2,
                "code1":       c1,
                "code2":       c2
            }, fp)
            fp.write("\n")
    print(f" → Wrote {len(rows)} items to {out_file}")

cur.close()
conn.close()
print("All done!")
