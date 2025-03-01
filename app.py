from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )''')
    c.execute('''CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                building_block TEXT,
                floor INTEGER,
                wooden_stool INTEGER DEFAULT 0,
                steel_stool INTEGER DEFAULT 0,
                ceiling_fan INTEGER DEFAULT 0,
                wall_mount_fan INTEGER DEFAULT 0,
                pedestal_fan INTEGER DEFAULT 0,
                water_dispenser INTEGER DEFAULT 0,
                bubble_tap INTEGER DEFAULT 0,
                notice_board INTEGER DEFAULT 0,
                marker_board INTEGER DEFAULT 0
            )''')
    c.execute('''CREATE TABLE IF NOT EXISTS record_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id TEXT,
                change_description TEXT,
                change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect(url_for('login'))
        except:
            return "Username exists"
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if (request.form['username'] == "naveenr2k05@gmail.com" and 
            request.form['password'] == "nav2k05"):
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        return "Invalid admin credentials"
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', users=users)

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/choose_building', methods=['GET', 'POST'])
def choose_building():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        return redirect(url_for('asset_management', building_block=request.form['building_block']))
    return render_template('choose_building.html')

@app.route('/asset_management', methods=['GET', 'POST'])
def asset_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    building_block = request.args.get('building_block')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        data = request.get_json()
        for item in data:
            c.execute('''UPDATE assets SET
                wooden_stool=?, steel_stool=?, ceiling_fan=?,
                wall_mount_fan=?, pedestal_fan=?, water_dispenser=?,
                bubble_tap=?, notice_board=?, marker_board=?
                WHERE id=?''', (
                item['wooden_stool'], item['steel_stool'], item['ceiling_fan'],
                item['wall_mount_fan'], item['pedestal_fan'], item['water_dispenser'],
                item['bubble_tap'], item['notice_board'], item['marker_board'], item['id']
            ))
            asset_id = f"AST{int(item['id']):03d}"
            c.execute('''INSERT INTO record_history 
                        (asset_id, change_description, change_date)
                        VALUES (?, ?, ?)''', (
                asset_id, "Updated asset", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
        conn.commit()
        return jsonify({'status': 'Changes Updated Successfully!'})
    
    c.execute("SELECT * FROM assets WHERE building_block=?", (building_block,))
    assets = c.fetchall()
    if not assets:
        for floor in range(0, 4):
            c.execute('''INSERT INTO assets (building_block, floor) VALUES (?, ?)''', (building_block, floor))
        conn.commit()
        c.execute("SELECT * FROM assets WHERE building_block=?", (building_block,))
        assets = c.fetchall()
    conn.close()
    return render_template('asset_management.html', assets=assets, building_block=building_block)

@app.route('/record_history', methods=['GET', 'POST'])
def record_history():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if request.method == 'POST':
        c.execute('''INSERT INTO record_history (change_description) VALUES (?)''', (request.form['description'],))
        conn.commit()
    c.execute("SELECT * FROM record_history ORDER BY change_date DESC")
    history = c.fetchall()
    conn.close()
    return render_template('record_history.html', history=history)
@app.route('/asset_total')
def asset_total():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    buildings = ['Amar Das Block', 'Arjan Dev Block', 'Hari Krishnan Block', 
                'Maharaja Block', 'Siddhu Block', 'Ram Das Block']
    
    totals = {}
    for building in buildings:
        c.execute('''SELECT 
                    SUM(wooden_stool), SUM(steel_stool), SUM(ceiling_fan),
                    SUM(wall_mount_fan), SUM(pedestal_fan), SUM(water_dispenser),
                    SUM(bubble_tap), SUM(notice_board), SUM(marker_board)
                    FROM assets WHERE building_block=?''', (building,))
        building_total = c.fetchone()
        totals[building] = building_total
        
        c.execute('''SELECT floor, 
                    SUM(wooden_stool), SUM(steel_stool), SUM(ceiling_fan),
                    SUM(wall_mount_fan), SUM(pedestal_fan), SUM(water_dispenser),
                    SUM(bubble_tap), SUM(notice_board), SUM(marker_board)
                    FROM assets WHERE building_block=? GROUP BY floor''', (building,))
        floor_totals = c.fetchall()
        totals[f"{building}_floors"] = floor_totals
    
    conn.close()
    return render_template('asset_total.html', totals=totals, buildings=buildings)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)