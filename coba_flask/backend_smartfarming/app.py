from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_cors import CORS

import sqlite3

DATABASE_NAME = 'dbsmartfarming.db'

app = Flask(__name__)
CORS(app)


# Fungsi untuk menginisialisasi database
def init_db():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        jadwalTable = cursor.execute('''
            CREATE TABLE IF NOT EXISTS jadwal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deskripsi TEXT NOT NULL,
                hari TEXT NOT NULL,
                jam TEXT NOT NULL
            )
        ''')

        # if jadwalTable:
        #     cursor.execute("INSERT INTO jadwal (deskripsi, hari,jam) VALUES (?, ?,?)",("Pemberian pupuk NPK di ruangan 1", "Senin", "08.00"))
        #     cursor.execute("INSERT INTO jadwal (deskripsi, hari,jam) VALUES (?, ?,?)",("Pemberian pupuk Urea di ruangan 1", "Selasa", "08.00"))
        #     cursor.execute("INSERT INTO jadwal (deskripsi, hari,jam) VALUES (?, ?,?)",("Pemberian pupuk NPK di ruangan 2", "Kamis", "08.00"))
        #     cursor.execute("INSERT INTO jadwal (deskripsi, hari,jam) VALUES (?, ?,?)",("Pemberian pupuk Urea di ruangan 2", "Jumat", "08.00"))
        #     cursor.execute("INSERT INTO jadwal (deskripsi, hari,jam) VALUES (?, ?,?)",("Pemberian pestisida di ruangan 1", "Minggu", "08.00"))

        conn.commit()
        # conn.close()

        print("Tabel Jadwal berhasil dibuat dan diisikan datanya")


@app.route('/')
def index():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jadwal")
        items = cursor.fetchall()
    return render_template('index.html', items=items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        deskripsi = request.form['deskripsi']
        hari = request.form['hari']
        jam = request.form['jam']

        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO jadwal(deskripsi,hari,jam) VALUES (?, ?, ?)",
                (deskripsi, hari, jam))
            conn.commit()

        return redirect(url_for('index'))
    return render_template('add_item.html')

# Edit barang
@app.route('/edit_item/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        if request.method == 'POST':
            deskripsi = request.form['deskripsi']
            hari = request.form['hari']
            jam = request.form['jam']

            cursor.execute(
                "UPDATE jadwal SET deskripsi = ?, hari = ?, jam = ? WHERE id = ?",
                (deskripsi,hari,jam, id))
            conn.commit()

            return redirect(url_for('index'))

        cursor.execute("SELECT id,hari,jam,deskripsi FROM jadwal WHERE id = ?", (id,))
        item = cursor.fetchone()

    return render_template('edit_item.html', item=item)

# Hapus barang
@app.route('/delete_item/<int:id>')
def delete_item(id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jadwal WHERE id = ?", (id,))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/api/jadwal', methods=['GET'])
def get_jadwal():
    with sqlite3.connect(DATABASE_NAME) as conn:
        conn.row_factory = sqlite3.Row  # Mengembalikan hasil sebagai dictionary
        cursor = conn.cursor()
        cursor.execute('SELECT id, deskripsi, hari, jam FROM jadwal')
        jadwalAll = cursor.fetchall()
    
    return jsonify([{'id': jadwal['id'], 'deskripsi': jadwal['deskripsi'], 'hari': jadwal['hari'], 'jam':jadwal['jam']} for jadwal in jadwalAll])

# Panggil fungsi inisialisasi saat aplikasi mulai
if __name__ == '__main__':
    init_db()
    app.run(host="192.168.2.116",debug=True,port='8000')