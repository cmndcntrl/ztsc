from flask import Flask, render_template, request, redirect, url_for, flash
from forms import RegistrationForm, LoginForm
import psycopg2
import bcrypt

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'FUkmybQYeoiT'  # Replace with a real secret key

# Database connection parameters
DB_NAME = "users"
DB_USER = "admin"
DB_PASS = "P05tGr35!"
DB_HOST = "localhost"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()

        # Insert new user into the database
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                        (username, hashed_password))
            conn.commit()
        except psycopg2.Error as e:
            # Handle database errors, e.g., user already exists
            conn.rollback()
            flash('Registration error: ' + str(e))
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()

        # Check if user exists and password is correct
        cur.execute("SELECT password FROM users WHERE email = %s", (email,))
        user_record = cur.fetchone()
        cur.close()
        conn.close()

        if user_record and bcrypt.checkpw(password.encode('utf-8'), user_record[0].encode('utf-8')):
            # User authenticated successfully
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')

    return render_template('login.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
#@login_required
def upload():
    if request.method == 'POST':
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = photos.save(file)
            # Additional logic to associate the file with the current_user can be added here
            return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
