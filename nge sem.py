from flask import Flask, render_template_string, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    index_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Department Inventory Management</title>
    </head>
    <body>
        <h1>Welcome to Department Inventory Management System</h1>
        <a href="{{ url_for('login') }}">Login</a>
    </body>
    </html>
    '''
    return render_template_string(index_html)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
    </head>
    <body>
        <h1>Login</h1>
        <form method="POST" action="{{ url_for('login') }}">
            <label for="department_id">Department ID:</label>
            <input type="text" name="department_id" id="department_id" required>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    '''

    if request.method == 'POST':
        department_id = request.form['department_id']
        conn = get_db_connection()
        department = conn.execute('SELECT * FROM departments WHERE department_id = ?', (department_id,)).fetchone()
        conn.close()
        
        if department:
            session['department_id'] = department['department_id']
            session['department_name'] = department['name']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Department ID"

    return render_template_string(login_html)

@app.route('/dashboard')
def dashboard():
    if 'department_id' not in session:
        return redirect(url_for('login'))
    
    dashboard_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
    </head>
    <body>
        <h1>{{ session['department_name'] }} Dashboard</h1>
        <p>Inventory items available:</p>
        <ul>
        {% for item in inventory_items %}
            <li>{{ item['item_name'] }}: {{ item['quantity'] }} units</li>
        {% endfor %}
        </ul>
        <a href="{{ url_for('report') }}">Generate Monthly Report</a>
    </body>
    </html>
    '''

    department_id = session['department_id']
    conn = get_db_connection()
    inventory_items = conn.execute('SELECT * FROM inventory WHERE department_id = ?', (department_id,)).fetchall()
    conn.close()
    
    return render_template_string(dashboard_html, inventory_items=inventory_items)

@app.route('/report')
def report():
    if 'department_id' not in session:
        return redirect(url_for('login'))
    
    report_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Monthly Report</title>
    </head>
    <body>
        <h1>Monthly Inventory Usage Report</h1>
        <ul>
        {% for item in report_data %}
            <li>{{ item['item_name'] }}: {{ item['total_used'] }} units used</li>
        {% endfor %}
        </ul>
        <a href="{{ url_for('dashboard') }}">Back to Dashboard</a>
    </body>
    </html>
    '''

    department_id = session['department_id']
    conn = get_db_connection()
    report_data = conn.execute('SELECT item_name, SUM(quantity) as total_used FROM inventory WHERE department_id = ? GROUP BY item_name', (department_id,)).fetchall()
    conn.close()
    
    return render_template_string(report_html, report_data=report_data)

if __name__ == "__main__":
    # Initialize the database (run this only once)
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()

    # Create the departments table
    c.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        department_id TEXT UNIQUE)
    ''')

    # Create the inventory table
    c.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        item_name TEXT, 
        department_id INTEGER, 
        quantity INTEGER,
        FOREIGN KEY(department_id) REFERENCES departments(department_id))
    ''')

    # Insert example data (run this only once)
    c.execute("INSERT OR IGNORE INTO departments (name, department_id) VALUES ('Mechanical Engineering', 'MECH001')")
    c.execute("INSERT OR IGNORE INTO departments (name, department_id) VALUES ('Electrical Engineering', 'ELEC001')")
    c.execute("INSERT OR IGNORE INTO inventory (item_name, department_id, quantity) VALUES ('Resistor', 1, 200)")
    c.execute("INSERT OR IGNORE INTO inventory (item_name, department_id, quantity) VALUES ('Capacitor', 2, 150)")

    conn.commit()
    conn.close()

    # Run the Flask app
    app.run(debug=True)
