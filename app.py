from flask import Flask, render_template, redirect, url_for, session, request, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'my_secret_key' 

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            name TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/',methods = ['POST','GET'])
def home():
    if 'id' in session:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        conn.close()
        return render_template('home.html', users=rows)
    return redirect(url_for('login'))

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, password))
        result = c.fetchone()
        conn.close()
        if result:
            session['id'] = result[0]
            return redirect(url_for('home'))
        else:
            flash("Sai tài khoản hoặc mật khẩu!")
    return render_template('login.html')

@app.route('/register', methods = ['GET','POST'])
def register():
        if request.method == 'POST':
            user = request.form['user']
            password = request.form['password']
            email = request.form['email']
            fullname = request.form['fullname']
            try:
                conn = sqlite3.connect('users.db')
                c = conn.cursor()
                c.execute("INSERT INTO users (username, password, email, name) VALUES (?, ?, ?, ?)", (user, password, email,fullname))
                conn.commit()
                conn.close()
                flash("Đăng ký thành công! Vui lòng đăng nhập.")
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash("Tên đăng nhập đã tồn tại.")
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('login'))

@app.route('/edit/<int:u_id>', methods = ['POST', 'GET'])
def edit(u_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        email = request.form['email']
        fullname = request.form['fullname']
        c.execute("UPDATE users SET username=?, password=?, email=?, name=? WHERE id=?",(user, password, email, fullname, u_id))
        conn.commit()
        conn.close()
        flash('Cập nhật thành công!')
        return redirect(url_for('home'))
    c.execute("SELECT * FROM users WHERE id=?", (u_id,))
    user = c.fetchone()
    conn.close()
    return render_template('edit.html', user=user)

@app.route('/delete/<int:u_id>', methods = ['POST','GET'])
def delete(u_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (u_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))


if __name__ == "__main__":
    init_db() 
    app.run(debug=True)