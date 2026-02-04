from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ==================== DATABASE (PYTHON DICTIONARIES) ====================

# Users Database
users_db = {
    'user1@example.com': {
        'password': 'password123',
        'name': 'Sarah Johnson',
        'role': 'client',
        'phone': '+91-98765-43210'
    },
    'photographer1@example.com': {
        'password': 'photo123',
        'name': 'Alex Rivera',
        'role': 'photographer',
        'phone': '+91-98765-43211'
    }
}

# Photographers Database (Sync with signup)
photographers_db = {
    'PH001': {
        'id': 'PH001',
        'name': 'Alex Rivera',
        'email': 'photographer1@example.com',
        'specialization': 'Wedding',
        'price': 80000,
        'rating': 4.9,
        'reviews_count': 127,
        'experience': '8',
        'location': 'Mumbai',
        'bio': 'Passionate wedding photographer capturing love stories.',
        'portfolio': [
            'https://images.unsplash.com/photo-1519741497674-611481863552?w=800',
            'https://images.unsplash.com/photo-1606800052052-a08af7148866?w=800'
        ],
        'reviews': []
    },
    'PH002': {
        'id': 'PH002',
        'name': 'Maya Patel',
        'email': 'maya.patel@lumilens.com',
        'specialization': 'Portrait',
        'price': 15000,
        'rating': 4.8,
        'reviews_count': 95,
        'experience': '6',
        'location': 'Bangalore',
        'bio': 'Creating timeless portraits.',
        'portfolio': [
            'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=800'
        ],
        'reviews': []
    },
    'PH003': {
        'id': 'PH003',
        'name': 'James Mitchell',
        'email': 'james.mitchell@lumilens.com',
        'specialization': 'Event',
        'price': 25000,
        'rating': 4.7,
        'reviews_count': 83,
        'experience': '10',
        'location': 'Delhi',
        'bio': 'Documenting corporate events.',
        'portfolio': [
            'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800'
        ],
        'reviews': []
    }
}

# Bookings Database
bookings_db = {}
booking_counter = 1

# Chat Messages Database
chat_messages_db = {}

# Reviews Database
reviews_db = {}

# Gallery Database (Pinterest-style inspiration)
gallery_db = {
    'wedding': [
        'https://images.unsplash.com/photo-1519741497674-611481863552?w=600',
        'https://images.unsplash.com/photo-1606800052052-a08af7148866?w=600',
        'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=600',
        'https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=600'
    ],
    'portrait': [
        'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=600',
        'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600',
        'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=600',
        'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=600'
    ],
    'event': [
        'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=600',
        'https://images.unsplash.com/photo-1505236858219-8359eb29e329?w=600',
        'https://images.unsplash.com/photo-1511578314322-379afb476865?w=600',
        'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=600'
    ],
    'family': [
        'https://images.unsplash.com/photo-1511895426328-dc8714191300?w=600',
        'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=600',
        'https://images.unsplash.com/photo-1542037104857-ffbb0b9155fb?w=600',
        'https://images.unsplash.com/photo-1511895426328-dc8714191300?w=600'
    ]
}

# ==================== ROUTES ====================

@app.route('/')
def home():
    """Home page"""
    if 'user' in session:
        if session.get('role') == 'photographer':
            return redirect(url_for('photographer_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User signup"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        role = request.form.get('role', 'client')
        
        if email in users_db:
            flash('Email already registered. Please login.', 'error')
            return redirect(url_for('signup'))
        
        # Base user data
        user_data = {
            'password': password,
            'name': name,
            'role': role,
            'phone': phone
        }
        
        users_db[email] = user_data
        
        # If photographer, add to photographers_db with extra fields
        if role == 'photographer':
            ph_id = f'PH{str(len(photographers_db) + 1).zfill(3)}'
            photographers_db[ph_id] = {
                'id': ph_id,
                'name': name,
                'email': email,
                'location': request.form.get('location', 'Not Specified'),
                'specialization': request.form.get('specialization', 'General'),
                'experience': request.form.get('experience', '0'),
                'price': int(request.form.get('price', 0)),
                'bio': request.form.get('bio', ''),
                'rating': 5.0,
                'reviews_count': 0,
                'portfolio': [
                    request.form.get('portfolio1', 'https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=800'),
                    request.form.get('portfolio2', 'https://images.unsplash.com/photo-1511895426328-dc8714191300?w=800'),
                    request.form.get('portfolio3', 'https://images.unsplash.com/photo-1522673607200-164d1b6ce486?w=800')
                ],
                'reviews': []
            }
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users_db and users_db[email]['password'] == password:
            session['user'] = email
            session['name'] = users_db[email]['name']
            session['role'] = users_db[email]['role']
            
            flash(f'Welcome back, {users_db[email]["name"]}!', 'success')
            
            if users_db[email]['role'] == 'photographer':
                return redirect(url_for('photographer_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/user-dashboard')
def user_dashboard():
    """Client dashboard"""
    if 'user' not in session or session.get('role') != 'client':
        flash('Please login as a client to access this page.', 'error')
        return redirect(url_for('login'))
    
    # Get user's bookings
    user_bookings = {k: v for k, v in bookings_db.items() if v['client_email'] == session['user']}
    
    return render_template('user_dashboard.html', bookings=user_bookings)

@app.route('/photographer-dashboard')
def photographer_dashboard():
    """Photographer dashboard"""
    if 'user' not in session or session.get('role') != 'photographer':
        flash('Please login as a photographer to access this page.', 'error')
        return redirect(url_for('login'))
    
    # Get photographer's bookings
    photographer_bookings = {k: v for k, v in bookings_db.items() if v['photographer_email'] == session['user']}
    
    # Calculate earnings
    earnings = sum(v['price'] for v in photographer_bookings.values() if v['status'] == 'Delivered')
    pending_bookings = [v for v in photographer_bookings.values() if v['status'] == 'Requested']
    active_bookings = [v for v in photographer_bookings.values() if v['status'] in ['Accepted', 'Shoot Started', 'Editing']]
    
    # Get photographer profile
    photographer = None
    for ph_id, ph_data in photographers_db.items():
        if ph_data['email'] == session['user']:
            photographer = ph_data
            break
    
    return render_template('photographer_dashboard.html', 
                           bookings=photographer_bookings, 
                           photographer=photographer,
                           earnings=earnings,
                           pending_count=len(pending_bookings),
                           active_count=len(active_bookings))

@app.route('/photographers')
def photographers():
    """Browse all photographers"""
    if 'user' not in session:
        flash('Please login to browse photographers.', 'error')
        return redirect(url_for('login'))
    
    return render_template('photographers.html', photographers=photographers_db)

@app.route('/profile/<photographer_id>')
def profile(photographer_id):
    """Photographer profile page"""
    if 'user' not in session:
        flash('Please login to view photographer profiles.', 'error')
        return redirect(url_for('login'))
    
    if photographer_id not in photographers_db:
        flash('Photographer not found.', 'error')
        return redirect(url_for('photographers'))
    
    photographer = photographers_db[photographer_id]
    return render_template('profile.html', photographer=photographer)

@app.route('/booking/<photographer_id>', methods=['GET', 'POST'])
def booking(photographer_id):
    """Booking page"""
    if 'user' not in session or session.get('role') != 'client':
        flash('Please login as a client to book a photographer.', 'error')
        return redirect(url_for('login'))
    
    if photographer_id not in photographers_db:
        flash('Photographer not found.', 'error')
        return redirect(url_for('photographers'))
    
    photographer = photographers_db[photographer_id]
    
    if request.method == 'POST':
        global booking_counter
        
        booking_id = f'BK{str(booking_counter).zfill(4)}'
        booking_counter += 1
        
        bookings_db[booking_id] = {
            'id': booking_id,
            'client_email': session['user'],
            'client_name': session['name'],
            'photographer_id': photographer_id,
            'photographer_name': photographer['name'],
            'photographer_email': photographer['email'],
            'event_type': request.form.get('event_type'),
            'event_date': request.form.get('event_date'),
            'location': request.form.get('location'),
            'duration': request.form.get('duration'),
            'price': photographer['price'],
            'status': 'Requested',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        flash('Booking request submitted successfully!', 'success')
        return redirect(url_for('payment', booking_id=booking_id))
    
    return render_template('booking.html', photographer=photographer)

@app.route('/payment/<booking_id>', methods=['GET', 'POST'])
def payment(booking_id):
    """Payment page (UI simulation)"""
    if 'user' not in session:
        flash('Please login to continue.', 'error')
        return redirect(url_for('login'))
    
    if booking_id not in bookings_db:
        flash('Booking not found.', 'error')
        return redirect(url_for('user_dashboard'))
    
    booking = bookings_db[booking_id]
    
    if request.method == 'POST':
        # Simulate payment success
        booking['payment_status'] = 'Paid'
        booking['payment_method'] = request.form.get('payment_method')
        booking['transaction_id'] = f'TXN{secrets.token_hex(8).upper()}'
        
        flash('Payment successful! Your booking is confirmed.', 'success')
        return redirect(url_for('tracker', booking_id=booking_id))
    
    return render_template('payment.html', booking=booking)

@app.route('/tracker/<booking_id>')
def tracker(booking_id):
    """Booking progress tracker"""
    if 'user' not in session:
        flash('Please login to view booking tracker.', 'error')
        return redirect(url_for('login'))
    
    if booking_id not in bookings_db:
        flash('Booking not found.', 'error')
        return redirect(url_for('user_dashboard'))
    
    booking = bookings_db[booking_id]
    
    # Define status progression
    statuses = ['Requested', 'Accepted', 'Shoot Started', 'Editing', 'Delivered']
    current_index = statuses.index(booking['status']) if booking['status'] in statuses else 0
    
    return render_template('tracker.html', booking=booking, statuses=statuses, current_index=current_index)

@app.route('/update-status/<booking_id>', methods=['POST'])
def update_status(booking_id):
    """Update booking status (photographer only)"""
    if 'user' not in session or session.get('role') != 'photographer':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    if booking_id not in bookings_db:
        return jsonify({'success': False, 'message': 'Booking not found'}), 404
    
    new_status = request.form.get('status')
    bookings_db[booking_id]['status'] = new_status
    
    return jsonify({'success': True, 'message': 'Status updated successfully'})

@app.route('/gallery')
def gallery():
    """Pinterest-style gallery"""
    if 'user' not in session:
        flash('Please login to view gallery.', 'error')
        return redirect(url_for('login'))
    
    return render_template('gallery.html', gallery=gallery_db)

@app.route('/review/<booking_id>', methods=['GET', 'POST'])
def review(booking_id):
    """Submit review after booking completion"""
    if 'user' not in session or session.get('role') != 'client':
        flash('Please login as a client to submit a review.', 'error')
        return redirect(url_for('login'))
    
    if booking_id not in bookings_db:
        flash('Booking not found.', 'error')
        return redirect(url_for('user_dashboard'))
    
    booking = bookings_db[booking_id]
    
    if request.method == 'POST':
        review_id = f'RV{len(reviews_db) + 1}'
        
        reviews_db[review_id] = {
            'booking_id': booking_id,
            'photographer_id': booking['photographer_id'],
            'client_name': session['name'],
            'rating': int(request.form.get('rating')),
            'comment': request.form.get('comment'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        flash('Thank you for your review!', 'success')
        return redirect(url_for('user_dashboard'))
    
    return render_template('review.html', booking=booking)

# ==================== CHAT & CHATBOT API ====================

@app.route('/chat/<booking_id>')
def chat(booking_id):
    """Chat page"""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    if booking_id not in bookings_db:
        return jsonify({'success': False, 'message': 'Booking not found'}), 404
    
    # Initialize chat if not exists
    if booking_id not in chat_messages_db:
        chat_messages_db[booking_id] = []
    
    return jsonify({'success': True, 'messages': chat_messages_db[booking_id]})

@app.route('/send-message/<booking_id>', methods=['POST'])
def send_message(booking_id):
    """Send chat message"""
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    if booking_id not in bookings_db:
        return jsonify({'success': False, 'message': 'Booking not found'}), 404
    
    message = request.form.get('message')
    
    if booking_id not in chat_messages_db:
        chat_messages_db[booking_id] = []
    
    chat_messages_db[booking_id].append({
        'sender': session['name'],
        'message': message,
        'timestamp': datetime.now().strftime('%H:%M')
    })
    
    return jsonify({'success': True})

@app.route('/chatbot', methods=['POST'])
def chatbot():
    """Rule-based chatbot API"""
    user_message = request.json.get('message', '').lower()
    
    # Rule-based responses
    if 'book' in user_message or 'booking' in user_message:
        response = "To book a photographer, browse our photographers page, select your preferred photographer, and click 'Book Now'. You'll be guided through the booking process step by step!"
    elif 'price' in user_message or 'cost' in user_message or 'pricing' in user_message:
        response = "Our photographers offer competitive pricing starting from ₹10,000. Prices vary based on specialization and experience. Check individual photographer profiles for exact pricing."
    elif 'contact' in user_message or 'support' in user_message or 'help' in user_message:
        response = "You can reach us at support@lumilens.com or call +91-1800-LUMILENS. We're here to help 24/7!"
    elif 'payment' in user_message or 'pay' in user_message:
        response = "We accept all major payment methods including Credit/Debit Cards, UPI, and Digital Wallets. Payment is secure and processed after booking confirmation."
    elif 'track' in user_message or 'status' in user_message:
        response = "You can track your booking status in your dashboard. We provide real-time updates: Requested → Accepted → Shooting → Editing → Delivered."
    elif 'hello' in user_message or 'hi' in user_message or 'hey' in user_message:
        response = "Hello! Welcome to LumiLens. How can I assist you today? Ask me about bookings, pricing, or anything else!"
    else:
        response = "I'm here to help! You can ask me about bookings, pricing, payment methods, tracking your order, or contact information."
    
    return jsonify({'response': response})

# ==================== RUN APP ====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


