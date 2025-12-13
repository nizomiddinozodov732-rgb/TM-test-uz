import sys
import os

# Parent directory ni path ga qo'shish (models_simple.py uchun)
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from models_simple import get_db, init_db
import random
import string

# Flask app yaratish - templates va static papkalarini ko'rsatish
app = Flask(__name__, 
            template_folder=os.path.join(parent_dir, 'templates'),
            static_folder=os.path.join(parent_dir, 'static'),
            static_url_path='/static')

# CORS sozlamalari - barcha manbalarga ruxsat
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Database yaratish - lazy initialization (faqat kerak bo'lganda)
# SQLite Vercel'da ishlamaydi, shuning uchun try-except qo'shildi
_db_initialized = False

def ensure_db():
    """Database ni faqat kerak bo'lganda yaratish"""
    global _db_initialized
    if not _db_initialized:
        try:
            init_db()
            _db_initialized = True
        except Exception as e:
            # Vercel'da SQLite ishlamaydi - bu normal
            # Production'da cloud database ishlatish kerak
            print(f"Database initialization warning: {e}")
            _db_initialized = True  # Xatolikni qayta-qayta ko'rsatmaslik uchun

def safe_get_db():
    """Database connection olish, xatolikni boshqarish"""
    try:
        ensure_db()
        return get_db()
    except Exception as e:
        error_msg = str(e)
        if "SQLite" in error_msg or "read-only" in error_msg.lower():
            raise Exception("SQLite Vercel'da ishlamaydi. Iltimos, cloud database (Vercel Postgres, Supabase, va hokazo) sozlang.")
        raise

def generate_test_id():
    """6 xonali test ID yaratish"""
    return ''.join(random.choices(string.digits, k=6))

# ============ HTML PAGES ============

@app.route('/')
def index():
    """Asosiy sahifa"""
    return render_template('Index.html')

@app.route('/kirish.html')
def kirish():
    """Kirish sahifasi"""
    return render_template('kirish.html')

@app.route('/test_tanlov.html')
def test_tanlov():
    """Test tanlash sahifasi"""
    return render_template('test_tanlov.html')

@app.route('/test_yuklash.html')
def test_yuklash():
    """Test yuklash sahifasi"""
    return render_template('test_yuklash.html')

@app.route('/results.html')
def results():
    """Natijalar sahifasi"""
    return render_template('results.html')

@app.route('/ishlash.html')
def ishlash():
    """Test ishlash sahifasi"""
    return render_template('ishlash.html')

# ============ STATIC FILES ============
# Flask automatically serves files from static_folder via /static/ URL

# ============ USER ENDPOINTS ============

@app.route('/api/login', methods=['POST'])
def login():
    """Foydalanuvchi kirish"""
    ensure_db()  # Database ni tekshirish
    
    data = request.json
    name = data.get('name')
    user_id = data.get('id')
    
    if not name or not user_id:
        return jsonify({'error': 'Ism va ID kiritilishi shart'}), 400
    
    try:
        conn = safe_get_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    cursor = conn.cursor()
    
    # Foydalanuvchini topish
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    if not user:
        # Yangi foydalanuvchi yaratish
        cursor.execute('INSERT INTO users (id, name) VALUES (?, ?)', (user_id, name))
        conn.commit()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
    
    conn.close()
    
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'name': user['name']
        }
    })

# ============ TEST ENDPOINTS ============

@app.route('/api/tests', methods=['GET'])
def get_tests():
    """Barcha testlarni olish"""
    ensure_db()  # Database ni tekshirish
    
    try:
        conn = safe_get_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tests ORDER BY created_at DESC')
    tests = cursor.fetchall()
    conn.close()
    
    tests_list = []
    for test in tests:
        keys = test.keys()
        tests_list.append({
            'id': test['id'],
            'name': test['name'],
            'image': test['image'] if 'image' in keys else None,
            'class_level': test['class_level'] if 'class_level' in keys else None,
            'duration_minutes': test['duration_minutes'] if 'duration_minutes' in keys else None,
            'subject': test['subject'] if 'subject' in keys else None,
            'created_at': test['created_at']
        })
    return jsonify({'tests': tests_list})

@app.route('/api/tests/<test_id>', methods=['GET'])
def get_test(test_id):
    """Bitta testni barcha savollari bilan olish"""
    try:
        conn = safe_get_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    cursor = conn.cursor()
    
    # Testni topish
    cursor.execute('SELECT * FROM tests WHERE id = ?', (test_id,))
    test = cursor.fetchone()
    if not test:
        conn.close()
        return jsonify({'error': 'Test topilmadi'}), 404
    
    # Savollarni olish
    cursor.execute('SELECT * FROM questions WHERE test_id = ?', (test_id,))
    questions = cursor.fetchall()
    
    questions_list = []
    for q in questions:
        # Javob variantlarini olish
        cursor.execute('SELECT * FROM answers WHERE question_id = ?', (q['id'],))
        answers = cursor.fetchall()
        
        answers_list = []
        for ans in answers:
            answers_list.append({
                'id': ans['id'],
                'variant': ans['variant'],
                'text': ans['text']
            })
        
        questions_list.append({
            'id': q['id'],
            'question_text': q['question_text'],
            'answers': answers_list
        })
    
    conn.close()
    
    keys = test.keys()
    return jsonify({
        'test': {
            'id': test['id'],
            'name': test['name'],
            'class_level': test['class_level'] if 'class_level' in keys else None,
            'duration_minutes': test['duration_minutes'] if 'duration_minutes' in keys else None,
            'subject': test['subject'] if 'subject' in keys else None,
            'image': test['image'] if 'image' in keys else None,
            'questions': questions_list
        }
    })

@app.route('/api/tests/create', methods=['POST'])
def create_test():
    """Yangi test yaratish"""
    data = request.json
    test_name = data.get('name')
    questions = data.get('questions', [])
    test_image = data.get('image')  # Rasm base64 formatida
    class_level = data.get('class_level')
    duration_minutes = data.get('duration_minutes')
    subject = data.get('subject')
    
    if not test_name:
        return jsonify({'error': 'Test nomi kiritilishi shart'}), 400
    
    if not questions:
        return jsonify({'error': 'Kamida bitta savol bo\'lishi kerak'}), 400

    if duration_minutes is not None:
        try:
            duration_minutes = int(duration_minutes)
            if duration_minutes < 1:
                return jsonify({'error': 'Test vaqti kamida 1 daqiqa bo\'lishi kerak'}), 400
        except ValueError:
            return jsonify({'error': 'Test vaqti son bo\'lishi kerak'}), 400
    
    # Test ID yaratish
    test_id = generate_test_id()
    try:
        conn = safe_get_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    cursor = conn.cursor()
    
    # ID takrorlanmasligini tekshirish
    while True:
        cursor.execute('SELECT id FROM tests WHERE id = ?', (test_id,))
        if cursor.fetchone():
            test_id = generate_test_id()
        else:
            break
    
    # Test yaratish (rasm bilan yoki rasm siz)
    cursor.execute(
        '''
        INSERT INTO tests (id, name, image, class_level, duration_minutes, subject)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',
        (test_id, test_name, test_image, class_level, duration_minutes, subject)
    )
    
    # Savollar va javoblar yaratish
    for q_data in questions:
        question_text = q_data.get('question_text')
        answers = q_data.get('answers', [])
        correct_answer = q_data.get('correct_answer', 'A')
        
        if not question_text or not answers:
            continue
        
        # Savol yaratish
        cursor.execute(
            'INSERT INTO questions (test_id, question_text, correct_answer) VALUES (?, ?, ?)',
            (test_id, question_text, correct_answer)
        )
        question_id = cursor.lastrowid
        
        # Javob variantlarini yaratish
        for ans_data in answers:
            cursor.execute(
                'INSERT INTO answers (question_id, variant, text) VALUES (?, ?, ?)',
                (question_id, ans_data.get('variant'), ans_data.get('text'))
            )
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'test_id': test_id,
        'message': 'Test muvaffaqiyatli yaratildi'
    })

@app.route('/api/tests/<test_id>/delete', methods=['DELETE'])
def delete_test(test_id):
    """Testni o'chirish (faqat kod bilan)"""
    data = request.json or {}
    delete_code = data.get('code')
    
    # Kod tekshiruvi
    if delete_code != '2025':
        return jsonify({'error': 'Noto\'g\'ri kod'}), 403
    
    try:
        conn = safe_get_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    cursor = conn.cursor()
    
    # Testni topish
    cursor.execute('SELECT * FROM tests WHERE id = ?', (test_id,))
    test = cursor.fetchone()
    if not test:
        conn.close()
        return jsonify({'error': 'Test topilmadi'}), 404
    
    # Barcha savollarni olish
    cursor.execute('SELECT id FROM questions WHERE test_id = ?', (test_id,))
    question_ids = [row['id'] for row in cursor.fetchall()]
    
    # Barcha javoblarni o'chirish
    for question_id in question_ids:
        cursor.execute('DELETE FROM answers WHERE question_id = ?', (question_id,))
    
    # Barcha savollarni o'chirish
    cursor.execute('DELETE FROM questions WHERE test_id = ?', (test_id,))
    
    # Barcha natijalarni o'chirish
    cursor.execute('DELETE FROM test_results WHERE test_id = ?', (test_id,))
    
    # Testni o'chirish
    cursor.execute('DELETE FROM tests WHERE id = ?', (test_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'Test muvaffaqiyatli o\'chirildi'
    })

# ============ TEST TAKING ENDPOINTS ============

@app.route('/api/tests/<test_id>/submit', methods=['POST'])
def submit_test(test_id):
    """Test javoblarini yuborish va natijani hisoblash"""
    data = request.json
    user_id = data.get('user_id')
    answers = data.get('answers', [])
    
    if not user_id:
        return jsonify({'error': 'User ID kiritilishi shart'}), 400
    
    try:
        conn = safe_get_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    cursor = conn.cursor()
    
    # Testni topish
    cursor.execute('SELECT * FROM tests WHERE id = ?', (test_id,))
    test = cursor.fetchone()
    if not test:
        conn.close()
        return jsonify({'error': 'Test topilmadi'}), 404
    
    # Testni oldin ishlanganligini tekshirish
    cursor.execute(
        'SELECT * FROM test_results WHERE test_id = ? AND user_id = ?',
        (test_id, user_id)
    )
    existing_result = cursor.fetchone()
    
    if existing_result:
        conn.close()
        return jsonify({
            'error': 'Bu test allaqachon ishlangan',
            'result_id': existing_result['id']
        }), 400
    
    # Natijalarni hisoblash
    cursor.execute('SELECT * FROM questions WHERE test_id = ?', (test_id,))
    questions = cursor.fetchall()
    
    total_questions = len(questions)
    correct_answers = 0
    
    for q in questions:
        user_answer = next(
            (a['answer'] for a in answers if a['question_id'] == q['id']),
            None
        )
        if user_answer and user_answer.upper() == q['correct_answer'].upper():
            correct_answers += 1
    
    score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Natijani saqlash
    cursor.execute(
        '''INSERT INTO test_results (test_id, user_id, score, correct_answers, total_questions)
           VALUES (?, ?, ?, ?, ?)''',
        (test_id, user_id, score, correct_answers, total_questions)
    )
    result_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'result': {
            'id': result_id,
            'score': round(score, 2),
            'correct_answers': correct_answers,
            'total_questions': total_questions
        }
    })

# ============ RESULTS ENDPOINTS ============

@app.route('/api/results/<test_id>', methods=['GET'])
def get_test_results(test_id):
    """Test natijalarini olish"""
    try:
        conn = safe_get_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    cursor = conn.cursor()
    
    # Testni topish
    cursor.execute('SELECT * FROM tests WHERE id = ?', (test_id,))
    test = cursor.fetchone()
    if not test:
        conn.close()
        return jsonify({'error': 'Test topilmadi'}), 404
    
    # Natijalarni olish
    cursor.execute(
        'SELECT * FROM test_results WHERE test_id = ? ORDER BY completed_at DESC',
        (test_id,)
    )
    results = cursor.fetchall()
    
    results_list = []
    for result in results:
        # Foydalanuvchi ma'lumotlarini olish
        cursor.execute('SELECT * FROM users WHERE id = ?', (result['user_id'],))
        user = cursor.fetchone()
        
        results_list.append({
            'id': result['id'],
            'user_name': user['name'] if user else 'Noma\'lum',
            'user_id': result['user_id'],
            'score': round(result['score'], 2),
            'correct_answers': result['correct_answers'],
            'total_questions': result['total_questions'],
            'completed_at': result['completed_at']
        })
    
    conn.close()
    
    keys = test.keys()
    return jsonify({
        'test_name': test['name'],
        'class_level': test['class_level'] if 'class_level' in keys else None,
        'duration_minutes': test['duration_minutes'] if 'duration_minutes' in keys else None,
        'results': results_list
    })

@app.route('/api/results/user/<user_id>', methods=['GET'])
def get_user_results(user_id):
    """Foydalanuvchining barcha test natijalarini olish"""
    try:
        conn = safe_get_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT * FROM test_results WHERE user_id = ? ORDER BY completed_at DESC',
        (user_id,)
    )
    results = cursor.fetchall()
    
    results_list = []
    for result in results:
        cursor.execute('SELECT * FROM tests WHERE id = ?', (result['test_id'],))
        test = cursor.fetchone()
        
        results_list.append({
            'id': result['id'],
            'test_id': result['test_id'],
            'test_name': test['name'] if test else 'Noma\'lum test',
            'score': round(result['score'], 2),
            'correct_answers': result['correct_answers'],
            'total_questions': result['total_questions'],
            'completed_at': result['completed_at']
        })
    
    conn.close()
    
    return jsonify({'results': results_list})

@app.route('/api/results/<result_id>', methods=['GET'])
def get_result(result_id):
    """Bitta natijani olish"""
    try:
        conn = safe_get_db()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM test_results WHERE id = ?', (result_id,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return jsonify({'error': 'Natija topilmadi'}), 404
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (result['user_id'],))
    user = cursor.fetchone()
    
    cursor.execute('SELECT * FROM tests WHERE id = ?', (result['test_id'],))
    test = cursor.fetchone()
    
    conn.close()
    
    return jsonify({
        'result': {
            'id': result['id'],
            'user_name': user['name'] if user else 'Noma\'lum',
            'user_id': result['user_id'],
            'test_name': test['name'] if test else 'Noma\'lum test',
            'test_id': result['test_id'],
            'score': round(result['score'], 2),
            'correct_answers': result['correct_answers'],
            'total_questions': result['total_questions'],
            'completed_at': result['completed_at']
        }
    })

# Root route for health check
@app.route('/api', methods=['GET'])
def api_root():
    return jsonify({
        'message': 'Matematika Test API',
        'version': '1.0',
        'endpoints': {
            'login': '/api/login',
            'tests': '/api/tests',
            'create_test': '/api/tests/create',
            'submit_test': '/api/tests/<test_id>/submit',
            'results': '/api/results/<test_id>'
        }
    })

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint topilmadi'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Server xatoligi'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Matematika Test Backend Server")
    print("=" * 50)
    print("Server ishga tushmoqda...")
    print("URL: http://localhost:5000")
    print("API Base URL: http://localhost:5000/api")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)

