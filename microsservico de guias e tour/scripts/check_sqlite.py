import uuid
import httpx
import sqlite3
import os
import sys


def main():
    base = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
    gid = str(uuid.uuid4())
    payload = {
        "titulo": "Persist Test",
        "descricao": "Teste de persistencia SQLite",
        "dias": ["segunda"],
        "horarios": ["09:00"],
    }

    print("POST ->", f"{base}/guias/{gid}/passeios")
    try:
        r = httpx.post(f"{base}/guias/{gid}/passeios", json=payload, timeout=5.0)
    except Exception as e:
        print("POST failed:", e)
        sys.exit(2)

    print("POST status:", r.status_code)
    try:
        print("POST body:", r.json())
    except Exception:
        print("POST body (raw):", r.text)

    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data.db"))
    print("Checking DB path:", db_path)
    if not os.path.exists(db_path):
        print("data.db not found at", db_path)
        # also try relative path in cwd
        alt = os.path.abspath("data.db")
        print("alt path:", alt, "exists:", os.path.exists(alt))
        if not os.path.exists(alt):
            print("No database file found. If the app is running with in-memory persistence, data won't be saved to disk.")
            sys.exit(3)
        db_path = alt

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info('passeios')")
        schema = cur.fetchall()
        print("schema:", schema)

        cur.execute("SELECT id, guia_id, titulo, descricao, dias, horarios, criado_em FROM passeios ORDER BY criado_em DESC LIMIT 5")
        rows = cur.fetchall()
        print(f"found {len(rows)} rows (latest up to 5):")
        for r in rows:
            print(r)
    except Exception as e:
        print("DB query failed:", e)
        sys.exit(4)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
