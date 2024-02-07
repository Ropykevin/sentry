import sentry_sdk, psycopg2
from flask import Flask, render_template, flash
from sentry_sdk import capture_exception

sentry_sdk.init(
    dsn="https://ae1085d73eeb378b00f5f8aacb4811e7@o4506695501611008.ingest.sentry.io/4506695661584384",

    # Enable performance monitoring
    enable_tracing=True,
)

app=Flask(__name__)
app.secret_key='secretkey'

try:
    conn = psycopg2.connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'")
except Exception as e:
    capture_exception(e)

@app.route("/products")
def prods():
    try:
        cur = conn.cursor()
        cur.execute("Select * from products")
        prods = cur.fetchall()
        flash("Products fetched succcessfully.")
        return render_template("products.html", prods=prods)
    except Exception as e:
        capture_exception(e)
        flash("Server error. Try again later.")
        return render_template("products.html")
    
@app.route("/")
def sentry():
    return render_template('sentry.html')
app.run()