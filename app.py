from flask import Flask, render_template, request, redirect, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# بيانات تسجيل الدخول للمشرف
admin_username = 'admin'
admin_password = 'password'

# قائمة لتخزين بيانات العملاء
clients = []

@app.route('/')
def home():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    id_number = request.form['id_number']
    phone_fixed = request.form['phone_fixed']
    phone_mobile = request.form['phone_mobile']
    problem_type = request.form['problem_type']  # الحصول على نوع المشكلة

    if not name or not id_number or not phone_fixed or not phone_mobile or not problem_type:
        flash('Please fill out all fields.')
        return redirect('/')
    
    # تخزين بيانات العميل
    clients.append({
        'name': name,
        'id_number': id_number,
        'phone_fixed': phone_fixed,
        'phone_mobile': phone_mobile,
        'problem_type': problem_type  # إضافة نوع المشكلة
    })
    flash('Registration successful!')
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            return redirect('/admin')
        else:
            flash('Invalid credentials. Please try again.')
            return redirect('/login')
    
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('admin.html', clients=clients)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/login')


