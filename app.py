import os
import json
import sqlite3
import bcrypt
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # غيّرها في الإنتاج
app.debug = True

# جلب بيانات المستخدم الحالي في كل طلب
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = None
    if user_id:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        g.user = user
import os
import json
import sqlite3
import bcrypt
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # غيّرها في الإنتاج
app.debug = True

# --- طلب الخدمة من نافذة منبثقة ---
@app.route('/order_modal', methods=['POST'])
def order_modal():
    # يجب أن يكون المستخدم مسجلاً للدخول
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'يجب تسجيل الدخول أولاً.'}), 401
    service_id = request.form.get('service_id')
    service_name = request.form.get('service_name')
    serial = request.form.get('serial')
    notes = request.form.get('notes')
    user_id = session.get('user_id')
    username = session.get('username')
    if not service_id or not service_name or not serial:
        return jsonify({'success': False, 'error': 'جميع الحقول مطلوبة.'}), 400
    conn = get_db_connection()
    # جلب اسم الخدمة الحقيقي من قاعدة البيانات إذا توفر
    service = conn.execute('SELECT * FROM services WHERE id = ?', (service_id,)).fetchone()
    if not service:
        conn.close()
        return jsonify({'success': False, 'error': 'الخدمة غير موجودة.'}), 404
    # حفظ الطلب
    conn.execute('INSERT INTO orders (user_id, service, imei, details, status, username, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (user_id, service['name'], serial, notes, 'pending', username, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'تم إرسال الطلب بنجاح! سيتم مراجعته قريباً.'})

import os
import json
import sqlite3
import bcrypt
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # غيّرها في الإنتاج
app.debug = True

# صفحة تسجيل دخول المستخدم العادي
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            error = 'بيانات الدخول غير صحيحة.'
    return render_template('login.html', error=error)

# --- تعدد اللغات ---
LANGUAGES = ['ar', 'fr', 'en']
TRANSLATIONS = {}
for lang in LANGUAGES:
    path = os.path.join('translations', f'{lang}.json')
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            TRANSLATIONS[lang] = json.load(f)

def get_locale():
    lang = request.args.get('lang') or session.get('lang')
    if lang in LANGUAGES:
        session['lang'] = lang
        return lang
    session['lang'] = 'ar'
    return 'ar'

def get_translation(key):
    lang = get_locale()
    return TRANSLATIONS.get(lang, {}).get(key, key)

@app.context_processor
def inject_translations():
    lang = get_locale()
    return dict(_t=get_translation, lang=lang, LANGUAGES=LANGUAGES)

# --- دوال مساعدة ---
def get_db_connection():
    conn = sqlite3.connect('site.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

# --- لوحة إدارة الطلبات ---
@app.route('/admin/orders', methods=['GET', 'POST'])
def admin_orders():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        new_status = request.form.get('new_status')
        if order_id and new_status:
            conn.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
            conn.commit()
    orders_db = conn.execute('SELECT * FROM orders ORDER BY created_at DESC').fetchall()
    orders = []
    for row in orders_db:
        orders.append({
            'id': row['id'],
            'date': row['created_at'] if 'created_at' in row.keys() else '',
            'service': row['service'],
            'name': row['username'] if 'username' in row.keys() else '',
            'phone': row['phone'],
            'imei': row['imei'],
            'details': row['details'],
            'status': row['status'],
        })
    conn.close()
    return render_template('admin_orders.html', orders=orders)
# ...existing code...

def get_locale():
    lang = request.args.get('lang') or session.get('lang')
    if lang in LANGUAGES:
        session['lang'] = lang
        return lang
    # fallback: ar
    session['lang'] = 'ar'
    return 'ar'

def get_translation(key):
    lang = get_locale()
    return TRANSLATIONS.get(lang, {}).get(key, key)

@app.context_processor
def inject_translations():
    lang = get_locale()
    return dict(_t=get_translation, lang=lang, LANGUAGES=LANGUAGES)

import stripe
stripe.api_key = 'sk_test_51N...'  # ضع مفتاحك التجريبي هنا
# لوحة مراجعة طلبات الشحن
@app.route('/admin/recharge-requests', methods=['GET', 'POST'])
def admin_recharge_requests():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    success = error = None
    if request.method == 'POST':
        approve_id = request.form.get('approve_id')
        reject_id = request.form.get('reject_id')
        if approve_id:
            req = conn.execute('SELECT * FROM recharge_requests WHERE id = ?', (approve_id,)).fetchone()
            if req and req['status'] == 'pending':
                conn.execute('UPDATE recharge_requests SET status = ? WHERE id = ?', ('approved', approve_id))
                conn.execute('UPDATE users SET credits = credits + ? WHERE id = ?', (req['amount'], req['user_id']))
                conn.commit()
                from credit_logs import log_credit_action
                log_credit_action(req['user_id'], 'زيادة', req['amount'], f'شحن رصيد ({req['method']})')
                success = 'تم قبول الشحن وتحديث الرصيد.'
        elif reject_id:
            req = conn.execute('SELECT * FROM recharge_requests WHERE id = ?', (reject_id,)).fetchone()
            if req and req['status'] == 'pending':
                conn.execute('UPDATE recharge_requests SET status = ? WHERE id = ?', ('rejected', reject_id))
                conn.commit()
                success = 'تم رفض طلب الشحن.'
    rows = conn.execute('SELECT r.*, u.username FROM recharge_requests r LEFT JOIN users u ON r.user_id = u.id ORDER BY r.created_at DESC').fetchall()
    requests = []
    for row in rows:
        requests.append({
            'id': row['id'],
            'username': row['username'],
            'method': row['method'],
            'amount': row['amount'],
            'proof': row['proof'],
            'status': row['status'],
        })
    conn.close()
    return render_template('admin_recharge_requests.html', requests=requests, success=success, error=error)
# شحن الرصيد (واجهة فقط، معالجة إثبات يدوي)
import os
from werkzeug.utils import secure_filename
@app.route('/recharge', methods=['GET', 'POST'])
def recharge():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    success = error = None
    if request.method == 'POST':
        method = request.form.get('method')
        amount = request.form.get('amount')
        proof = request.files.get('proof')
        if not method or not amount or not amount.isdigit():
            error = 'يرجى اختيار طريقة دفع ومبلغ صحيح.'
        elif method == 'stripe':
            # Stripe Checkout
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': 'رصيد rif-unlocker'},
                            'unit_amount': int(float(amount) * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.url_root.rstrip('/') + '/recharge?success=1',
                    cancel_url=request.url_root.rstrip('/') + '/recharge?canceled=1',
                    metadata={'user_id': session['user_id'], 'amount': amount}
                )
                return redirect(checkout_session.url)
            except Exception as e:
                error = 'خطأ في الدفع عبر Stripe: ' + str(e)
        else:
            filename = None
            if proof and proof.filename:
                filename = secure_filename(proof.filename)
                proof.save(os.path.join('static', 'proofs', filename))
            from datetime import datetime
            conn = get_db_connection()
            conn.execute('INSERT INTO recharge_requests (user_id, method, amount, proof, status, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                         (session['user_id'], method, int(amount), filename, 'pending', datetime.now().isoformat()))
            conn.commit()
            conn.close()
            success = 'تم إرسال طلب الشحن بنجاح. سيتم مراجعة الطلب من الإدارة.'
    return render_template('recharge.html', success=success, error=error)
# صفحة توثيق Endpoints الخدمات
@app.route('/api-services-docs')
def api_services_docs():
    return render_template('api_services_docs.html')
# --- API ديناميكي لكل خدمة فعالة ---
from service_prices import SERVICES, get_service_price, get_service_status, get_service_handler
@app.route('/api/<service_key>/call', methods=['POST'])
def api_service_call(service_key):
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({'success': False, 'error': 'API key required'}), 401
    user = get_user_by_api_key(api_key)
    if not user:
        return jsonify({'success': False, 'error': 'Invalid API key'}), 403
    if not check_rate_limit(api_key):
        return jsonify({'success': False, 'error': 'Rate limit exceeded'}), 429
    # اسم الخدمة من المفتاح
    service_name = None
    for s in SERVICES:
        if s.lower().replace(' ', '') == service_key.lower().replace('_', '').replace('-', ''):
            service_name = s
            break
    if not service_name:
        return jsonify({'success': False, 'error': 'Unknown service'}), 404
    info = SERVICES[service_name]
    if info['status'] != 'ON':
        return jsonify({'success': False, 'error': 'Service is OFF'}), 403
    # تحقق من الكريدي
    if user['credits'] < info['price']:
        return jsonify({'success': False, 'error': 'Insufficient credits'}), 402
    # خصم الكريدي
    conn = get_db_connection()
    conn.execute('UPDATE users SET credits = credits - ? WHERE id = ?', (info['price'], user['id']))
    conn.commit()
    conn.close()
    # سجل العملية
    from credit_logs import log_credit_action
    log_credit_action(user['id'], 'خصم', info['price'], f'API: {service_name}')
    # handler وهمي (يمكنك ربطه فعلياً)
    handler_name = info['handler']
    # مثال: الرد حسب نوع الخدمة
    data = request.get_json(force=True)
    imei = data.get('imei')
    model = data.get('model')
    # هنا يمكن ربط handler حقيقي
    return jsonify({'success': True, 'message': f'{service_name} API call received', 'handler': handler_name, 'imei': imei, 'model': model, 'user': user['username']})
# إدارة الخدمات والأسعار من لوحة الإدارة
import json
@app.route('/admin/services', methods=['GET', 'POST'])
def admin_services():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    success = error = None
    if request.method == 'POST':
        # إضافة خدمة جديدة
        if 'add_service' in request.form:
            name = request.form.get('service_name', '').strip()
            price = request.form.get('service_price', '').strip()
            delivery_time = request.form.get('service_delivery_time', '').strip()
            category = request.form.get('service_category', '').strip() or 'Other'
            description = request.form.get('service_description', '').strip()
            notes = request.form.get('service_notes', '').strip()
            image_url = request.form.get('service_image_url', '').strip()
            created_at = request.form.get('service_created_at', '').strip()
            if not name or not price.replace('.', '', 1).isdigit():
                error = 'يرجى إدخال اسم وسعر صحيح.'
            else:
                exists = conn.execute('SELECT id FROM services WHERE name = ?', (name,)).fetchone()
                if exists:
                    error = 'الخدمة موجودة مسبقاً.'
                else:
                    if not created_at:
                        import datetime
                        created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    conn.execute('INSERT INTO services (name, price, delivery_time, category, description, notes, image_url, created_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)', (name, float(price), delivery_time, category, description, notes, image_url, created_at))
                    conn.commit()
                    success = 'تمت إضافة الخدمة.'
        # تعديل سعر أو بيانات خدمة
        elif 'edit_service' in request.form:
            service_id = request.form.get('edit_service')
            new_price = request.form.get('new_price', '').strip()
            new_delivery = request.form.get('new_delivery_time', '').strip()
            new_description = request.form.get('new_description', '').strip()
            new_notes = request.form.get('new_notes', '').strip()
            new_image_url = request.form.get('new_image_url', '').strip()
            if not new_price.replace('.', '', 1).isdigit():
                error = 'سعر غير صحيح.'
            else:
                conn.execute('UPDATE services SET price=?, delivery_time=?, description=?, notes=?, image_url=? WHERE id=?', (float(new_price), new_delivery, new_description, new_notes, new_image_url, service_id))
                conn.commit()
                success = 'تم تحديث بيانات الخدمة.'
        # تشغيل/إيقاف خدمة
        elif 'toggle_service' in request.form:
            service_id = request.form.get('toggle_service')
            service = conn.execute('SELECT is_active FROM services WHERE id=?', (service_id,)).fetchone()
            if service:
                new_status = 0 if service['is_active'] else 1
                conn.execute('UPDATE services SET is_active=? WHERE id=?', (new_status, service_id))
                conn.commit()
                success = 'تم تغيير حالة الخدمة.'
        # حذف خدمة
        elif 'delete_service' in request.form:
            service_id = request.form.get('delete_service')
            conn.execute('DELETE FROM services WHERE id=?', (service_id,))
            conn.commit()
            success = 'تم حذف الخدمة.'
    # جلب عدد الطلبات لكل خدمة
    services = conn.execute('SELECT * FROM services ORDER BY category, name').fetchall()
    orders_count = {}
    for s in services:
        count = conn.execute('SELECT COUNT(*) FROM orders WHERE service = ?', (s['name'],)).fetchone()[0]
        orders_count[s['id']] = count
    conn.close()
    return render_template('admin_services.html', services=services, orders_count=orders_count, success=success, error=error)
# إدارة المستخدمين من لوحة الإدارة
@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    success = error = None
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_role = request.form.get('role')
        delete_user_id = request.form.get('delete_user_id')
        if user_id and new_role:
            try:
                conn.execute('UPDATE users SET role = ? WHERE id = ?', (new_role, user_id))
                conn.commit()
                success = 'تم تحديث الدور بنجاح.'
            except Exception:
                error = 'حدث خطأ أثناء تحديث الدور.'
        elif delete_user_id:
            try:
                conn.execute('DELETE FROM users WHERE id = ?', (delete_user_id,))
                conn.commit()
                success = 'تم حذف المستخدم بنجاح.'
            except Exception:
                error = 'حدث خطأ أثناء حذف المستخدم.'
    users = conn.execute('SELECT id, username, email, role, credits, api_key, is_active FROM users ORDER BY id').fetchall()
    conn.close()
    return render_template('admin_users.html', users=users, success=success, error=error)
# صفحة توثيق API
@app.route('/api-docs')
def api_docs():
    return render_template('api_docs.html')
# --- API ENDPOINTS ---
from flask import jsonify, request, g
import time
import secrets

# تخزين آخر طلبات API لكل مفتاح (ذاكرة مؤقتة)
api_rate_limit = {}

def get_user_by_api_key(api_key):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE api_key = ?', (api_key,)).fetchone()
    conn.close()
    return user

def check_rate_limit(api_key, limit=5, window=60):
    now = int(time.time())
    if api_key not in api_rate_limit:
        api_rate_limit[api_key] = []
    # حذف الطلبات القديمة
    api_rate_limit[api_key] = [t for t in api_rate_limit[api_key] if now-t < window]
    if len(api_rate_limit[api_key]) >= limit:
        return False
    api_rate_limit[api_key].append(now)
    return True

@app.route('/api/frp/unlock', methods=['POST'])
def api_frp_unlock():
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({'success': False, 'error': 'API key required'}), 401
    user = get_user_by_api_key(api_key)
    if not user:
        return jsonify({'success': False, 'error': 'Invalid API key'}), 403
    if not check_rate_limit(api_key):
        return jsonify({'success': False, 'error': 'Rate limit exceeded'}), 429
    data = request.get_json(force=True)
    imei = data.get('imei')
    model = data.get('model')
    if not imei or not model:
        return jsonify({'success': False, 'error': 'imei and model required'}), 400
    # منطق وهمي للرد
    # هنا يمكن ربط الخدمة الحقيقية
    return jsonify({'success': True, 'message': f'FRP unlock request received for IMEI {imei}, model {model}', 'user': user['username']})
# سجل الكريدي الإداري لجميع المستخدمين
@app.route('/admin/credit-logs')
def admin_credit_logs():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    user_id = request.args.get('user_id', '')
    users = conn.execute('SELECT id, username FROM users ORDER BY username').fetchall()
    if user_id:
        logs = conn.execute('SELECT cl.*, u.username FROM credit_logs cl LEFT JOIN users u ON cl.user_id = u.id WHERE cl.user_id = ? ORDER BY cl.created_at DESC', (user_id,)).fetchall()
    else:
        logs = conn.execute('SELECT cl.*, u.username FROM credit_logs cl LEFT JOIN users u ON cl.user_id = u.id ORDER BY cl.created_at DESC').fetchall()
    conn.close()
    return render_template('admin_credit_logs.html', logs=logs, users=users, selected_user_id=user_id)
# إدارة رصيد المستخدمين من الإدارة
@app.route('/admin/credits', methods=['GET', 'POST'])
def admin_credits():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    success = error = None
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        amount = request.form.get('amount')
        action = request.form.get('action')
        reason = request.form.get('reason') or ''
        if not user_id or not amount or not action:
            error = 'جميع الحقول مطلوبة.'
        else:
            try:
                amount = int(amount)
                user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
                if not user:
                    error = 'المستخدم غير موجود.'
                elif action == 'add':
                    conn.execute('UPDATE users SET credits = credits + ? WHERE id = ?', (amount, user_id))
                    conn.commit()
                    from credit_logs import log_credit_action
                    log_credit_action(user_id, 'زيادة', amount, reason or 'زيادة من الإدارة')
                    success = f'تمت زيادة {amount} نقطة للمستخدم.'
                elif action == 'subtract':
                    if user['credits'] >= amount:
                        conn.execute('UPDATE users SET credits = credits - ? WHERE id = ?', (amount, user_id))
                        conn.commit()
                        from credit_logs import log_credit_action
                        log_credit_action(user_id, 'نقصان', amount, reason or 'نقصان من الإدارة')
                        success = f'تمت نقصان {amount} نقطة من المستخدم.'
                    else:
                        error = 'رصيد المستخدم غير كافٍ.'
                else:
                    error = 'عملية غير معروفة.'
            except Exception as e:
                error = 'حدث خطأ أثناء التعديل.'
    users = conn.execute('SELECT id, username, email, credits FROM users ORDER BY id').fetchall()
    conn.close()
    return render_template('admin_credits.html', users=users, success=success, error=error)
# سجل الكريدي للمستخدم
@app.route('/credit-logs')
def credit_logs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM credit_logs WHERE user_id = ? ORDER BY created_at DESC', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('credit_logs.html', logs=logs)
from service_prices import get_service_price
from credit_logs import log_credit_action
from reset_utils import generate_reset_token, send_reset_email
# استعادة كلمة المرور - طلب الإيميل
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    error = None
    success = None
    if request.method == 'POST':
        email = request.form.get('email')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if not user:
            error = 'البريد الإلكتروني غير مسجل.'
        else:
            token = generate_reset_token()
            conn.execute('UPDATE users SET reset_token = ? WHERE id = ?', (token, user['id']))
            conn.commit()
            conn.close()
            send_reset_email(email, user['username'], token)
            success = 'تم إرسال رابط استعادة كلمة المرور إلى بريدك.'
    return render_template('reset_password.html', error=error, success=success)

# تعيين كلمة مرور جديدة عبر الرابط
@app.route('/reset-password/confirm', methods=['GET', 'POST'])
def set_new_password():
    error = None
    success = None
    token = request.args.get('token') or request.form.get('token')
    if not token:
        return 'رابط غير صالح.'
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE reset_token = ?', (token,)).fetchone()
    if not user:
        conn.close()
        return 'رابط غير صالح أو منتهي.'
    if request.method == 'POST':
        password = request.form.get('password')
        if not password:
            error = 'يرجى إدخال كلمة مرور جديدة.'
        else:
            conn.execute('UPDATE users SET password_hash = ?, reset_token = NULL WHERE id = ?', (generate_password_hash(password), user['id']))
            conn.commit()
            conn.close()
            success = 'تم تعيين كلمة المرور الجديدة بنجاح. يمكنك الآن تسجيل الدخول.'
            return render_template('set_new_password.html', error=error, success=success)
    conn.close()
    return render_template('set_new_password.html', error=error, success=success, token=token)
# سجل طلبات المستخدم
@app.route('/my_orders')
def my_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    service_filter = request.args.get('service', '')
    status_filter = request.args.get('status', '')
    orders = []
    if user:
        query = 'SELECT * FROM orders WHERE user_id = ?'
        params = [user['id']]
        if service_filter:
            query += ' AND service = ?'
            params.append(service_filter)
        if status_filter:
            query += ' AND status = ?'
            params.append(status_filter)
        query += ' ORDER BY created_at DESC'
        rows = conn.execute(query, tuple(params)).fetchall()
        for row in rows:
            orders.append({
                'date': row['created_at'],
                'service': row['service'],
                'name': row['username'] if 'username' in row.keys() else '',
                'phone': row['phone'],
                'imei': row['imei'] if 'imei' in row.keys() else '',
                'details': row['details'],
                'status': row['status'],
            })
    conn.close()
    return render_template('my_orders.html', orders=orders, service_filter=service_filter, status_filter=status_filter)
# لوحة المستخدم (عرض الرصيد وزيادة/نقصان)
@app.route('/panel', methods=['GET', 'POST'])
def user_panel():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    # سجل الرصيد
    credit_logs = conn.execute('SELECT * FROM credit_logs WHERE user_id = ? ORDER BY created_at DESC LIMIT 5', (session['user_id'],)).fetchall()
    # آخر الطلبات
    last_orders = conn.execute('SELECT service, status, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 3', (session['user_id'],)).fetchall()
    success = error = None
    if request.method == 'POST':
        action = request.form.get('action')
        from credit_logs import log_credit_action
        if action == 'add':
            conn.execute('UPDATE users SET credits = credits + 1 WHERE id = ?', (user['id'],))
            conn.commit()
            log_credit_action(user['id'], 'زيادة', 1, 'زيادة يدوية من المستخدم')
            success = 'تمت زيادة نقطة واحدة.'
        elif action == 'subtract':
            if user['credits'] > 0:
                conn.execute('UPDATE users SET credits = credits - 1 WHERE id = ?', (user['id'],))
                conn.commit()
                log_credit_action(user['id'], 'نقصان', 1, 'نقصان يدوي من المستخدم')
                success = 'تمت نقصان نقطة واحدة.'
            else:
                error = 'لا يمكن النقصان، الرصيد صفر.'
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        credit_logs = conn.execute('SELECT * FROM credit_logs WHERE user_id = ? ORDER BY created_at DESC LIMIT 5', (session['user_id'],)).fetchall()
        last_orders = conn.execute('SELECT service, status, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 3', (session['user_id'],)).fetchall()
    conn.close()
    # تحويل النتائج لقوائم دكت
    user = dict(user)
    user['credit_logs'] = [dict(row) for row in credit_logs]
    user['last_orders'] = [dict(row) for row in last_orders]
    return render_template('user_panel.html', user=user, success=success, error=error)

import sqlite3
import bcrypt

    # دوال مساعدة للمستخدمين
def get_db_connection():
    conn = sqlite3.connect('site.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def create_user(username, password, email):
    import secrets
    api_key = secrets.token_hex(24)
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    role = 'user'  # تعيين دور افتراضي
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, password_hash, email, api_key, role) VALUES (?, ?, ?, ?, ?)',
                     (username, password_hash, email, api_key, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
# دوال مساعدة للمستخدمين
def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user

# صفحة تسجيل مستخدم جديد
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success = False
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        role = 'User'
        if not username or not password or not email:
            error = 'جميع الحقول مطلوبة.'
        else:
            # تحقق من عدم وجود المستخدم مسبقاً
            if get_user_by_username(username):
                error = 'اسم المستخدم مستخدم مسبقاً.'
            elif get_user_by_email(email):
                error = 'البريد الإلكتروني مستخدم مسبقاً.'
            else:
                # حفظ المستخدم الجديد
                import secrets
                api_key = secrets.token_hex(24)
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                conn = get_db_connection()
                try:
                    conn.execute('INSERT INTO users (username, password_hash, email, api_key, role, credits) VALUES (?, ?, ?, ?, ?, ?)',
                                 (username, password_hash, email, api_key, role, 0))
                    conn.commit()
                    success = True
                except sqlite3.IntegrityError:
                    error = 'حدث خطأ أثناء التسجيل.'
                finally:
                    conn.close()
    return render_template('register.html', error=error, success=success)

# جلب بيانات المستخدم الحالي في كل طلب
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = None
    if user_id:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        g.user = user

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

def check_user_password(username, password):
    user = get_user_by_username(username)
    if user:
        try:
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                return user
        except Exception:
            pass
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        code = request.form.get('code')
        # Placeholder logic for processing code/IMEI
        result = f"تم استقبال الكود: {code} (هنا ستكون نتيجة الخدمة)"
    return render_template('index.html', result=result)

# دالة لجلب الخدمات من قاعدة البيانات
def get_services_from_db(category=None, search=None):
    conn = get_db_connection()
    query = 'SELECT * FROM services WHERE is_active=1'
    params = []
    if category:
        query += ' AND category = ?'
        params.append(category)
    if search:
        query += ' AND (name LIKE ? OR description LIKE ? OR category LIKE ?)'

@app.route('/services')
def services():
    category = request.args.get('category')
    search = request.args.get('search')
    services = get_services_from_db(category, search)
    # استخراج جميع الفئات المتوفرة من قاعدة البيانات
    conn = get_db_connection()
    categories = [row['category'] for row in conn.execute('SELECT DISTINCT category FROM services WHERE is_active=1').fetchall()]
    conn.close()

    # منطق عرض الجداول الثابتة حسب الفئة المختارة
    show_imei = (category == 'IMEI Service')
    show_server = (category == 'Server Service')
    show_all = not (show_imei or show_server)

    return render_template(
        'services.html',
        services=services,
        categories=categories,
        show_imei=show_imei,
        show_server=show_server,
        show_all=show_all
    )

@app.route('/service/<int:service_id>')
def service_detail(service_id):
    conn = get_db_connection()
    service = conn.execute('SELECT * FROM services WHERE id = ?', (service_id,)).fetchone()
    conn.close()
    if not service:
        return render_template('404.html'), 404
    return render_template('service_detail.html', service=service)

@app.route('/order', methods=['GET', 'POST'])
def order():
    service_name = request.args.get('service')
    success = False
    error = None
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        phone = request.form.get('phone')
        imei = request.form.get('imei')
        details = request.form.get('details')
        user_id = session.get('user_id')
        username = session.get('username')
        if not imei or not phone:
            error = 'يجب إدخال رقم الهاتف و IMEI.'
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO orders (user_id, service, phone, imei, details, status, username, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                         (user_id, service_name, phone, imei, details, 'pending', username, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()
            success = True
    return render_template('order.html', service_name=service_name, success=success, error=error)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # قبول أي كلمة مرور مع اسم المستخدم admin (للاختبار فقط)
        if username == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_services'))
        else:
            error = 'بيانات الدخول غير صحيحة.'
    return render_template('admin_login.html', error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
