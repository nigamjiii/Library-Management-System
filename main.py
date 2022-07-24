from asyncio.windows_events import NULL
from flask import Flask, redirect, render_template, request, url_for,flash
import psycopg2 
import psycopg2.extras
 
app = Flask(__name__)
app.secret_key = "nigam123"

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "utkarsh123"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route("/")
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account==None:
            flash('Invalid Username/Password')
        elif password==account['password']:
            return redirect(url_for('home'))
        else:
            flash('Invalid Username/Password')
    return redirect(url_for('login_page'))
    
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'name' in request.form and 'email' in request.form:
        name=request.form['name']
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']

        if not username or not password or not email:
            flash('Please fill out the form!')
        else:
            cursor.execute("INSERT INTO users (name,email,username,password) VALUES (%s,%s,%s,%s)",(name,email,username,password))
            conn.commit()
            flash('User registered successfully, Now back to login page')  
    else:
        flash('Enter valid response')          
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('base.html')

@app.route("/add")
def add():
    return render_template('add.html')
  
@app.route("/view")
def view():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = """SELECT * FROM library_data ORDER BY id ASC"""
    cur.execute(s) # Execute the SQL
    list_books = cur.fetchall()
    return render_template('view.html', list_books = list_books)
    
@app.route("/add_book",methods=['POST'])
def add_book():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        book = request.form['book']
        author = request.form['author']
        edition = request.form['edition']
        cur.execute("INSERT INTO library_data (book,author,edition) VALUES (%s,%s,%s)", (book,author,edition))
        conn.commit()
        flash('Book Added successfully')
        return redirect(url_for('view'))

@app.route("/edit/<id>", methods=['GET','POST'])
def edit_book(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""SELECT * FROM library_data where id=%s""" %(id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit.html', book = data[0])


@app.route('/update/<id>', methods=['POST'])
def update_book(id):
    if request.method == 'POST':
        book = request.form['book']
        author = request.form['author']
        edition = request.form['edition']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE library_data
            SET book = %s,
                author = %s,
                edition = %s
            WHERE id = %s
        """, (book,author,edition,id))
        flash('Book Updated Successfully')
        conn.commit()
        return redirect(url_for('view'))

@app.route('/delete/<id>',methods=['GET','POST'])
def delete_book(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM library_data where id=%s'%(id))
    conn.commit()
    flash('Book removed Successfully')
    return redirect(url_for('view'))


if __name__== "__main__":
  app.run(debug=True,port=3000)
