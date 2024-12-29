from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Koneksi ke SQL Server
conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=kubukas;UID=sa;PWD=P@ssw0rd'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Route Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Login gagal. Periksa username dan password Anda."

    return render_template('login.html')

# Route Dashboard (Menu Utama)
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

# Route untuk Pencatatan Pemasukan
@app.route('/pemasukan', methods=['GET', 'POST'])
def pemasukan():
    if request.method == 'POST':
        jumlah = request.form['jumlah']
        kategori = request.form['kategori']
        tanggal = request.form['tanggal']  # Ambil tanggal dari form
#        cursor.execute("INSERT INTO transaksi (jenis, jumlah, kategori, tanggal) VALUES ('Pemasukan', ?, ?, ?, GETDATE())", (jumlah, kategori, tanggal))
#        cursor.execute("INSERT INTO transaksi (jenis, jumlah, kategori, tanggal) VALUES ('Pemasukan', ?, ?, ?)", (jumlah, kategori, tanggal))
        cursor.execute("INSERT INTO transaksi (jenis, jumlah, kategori, tanggal) VALUES ('Pemasukan', ?, ?, GETDATE())", (jumlah, kategori))



        conn.commit()
        return redirect(url_for('dashboard'))

    return render_template('transaksi.html', jenis='Pemasukan')

# Route untuk Pencatatan Pengeluaran
@app.route('/pengeluaran', methods=['GET', 'POST'])
def pengeluaran():
    if request.method == 'POST':
        jumlah = request.form['jumlah']
        kategori = request.form['kategori']
        tanggal = request.form['tanggal']  # Ambil tanggal dari form
        cursor.execute("INSERT INTO transaksi (jenis, jumlah, kategori, tanggal) VALUES ('Pengeluaran', ?, ?, ?)", (jumlah, kategori, tanggal))
        conn.commit()
        return redirect(url_for('dashboard'))

    return render_template('transaksi.html', jenis='Pengeluaran')

# Route untuk Menampilkan Sisa Saldo
@app.route('/saldo')
def saldo():
    cursor.execute("SELECT SUM(jumlah) FROM transaksi WHERE jenis='Pemasukan'")
    pemasukan = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(jumlah) FROM transaksi WHERE jenis='Pengeluaran'")
    pengeluaran = cursor.fetchone()[0] or 0
    saldo = pemasukan - pengeluaran
    return render_template('dashboard.html', saldo=saldo)

# Route untuk Mencatat Hutang
@app.route('/hutang', methods=['GET', 'POST'])
def hutang():
    if request.method == 'POST':
        jumlah = request.form['jumlah']
        deskripsi = request.form['deskripsi']
        tanggal = request.form['tanggal']
        cursor.execute("INSERT INTO hutang (jumlah, deskripsi, tanggal) VALUES (?, ?, ?)", (jumlah, deskripsi, tanggal))
        conn.commit()
        return redirect(url_for('dashboard'))

    return render_template('hutang.html')


# create user login

@app.route('/users', methods=['GET','POST'])
def users():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #cursor.execute("INSERT INTO users (username, password) VALUES ('users', ?, ?)", (username, password))
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))


        conn.commit()
        return redirect(url_for('dashboard'))
    return render_template('users.html', jenis='users')

# get users
@app.route('/getusers')
def getusers():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()  # Mengambil semua pengguna
    return render_template('users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
