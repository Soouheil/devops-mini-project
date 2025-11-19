from flask import Flask
import os
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "devopsdb"),
        user=os.environ.get("DB_USER", "devopsuser"),
        password=os.environ.get("DB_PASSWORD", "devopspassword"),
    )
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    # Créer la table si elle n'existe pas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            ts TIMESTAMPTZ DEFAULT NOW()
        );
    """)

    # Insérer une nouvelle visite
    cur.execute("INSERT INTO visits DEFAULT VALUES RETURNING id, ts;")
    conn.commit()

    # Compter le nombre total de visites
    cur.execute("SELECT COUNT(*) FROM visits;")
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return f"Hello DevOps from Souheil! Nombre total de visites: {count}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
