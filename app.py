import sqlite3
import os
import random
import urllib.parse
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "sri_murugan_travels_secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'travels.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS main_packages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  place TEXT, price TEXT, days TEXT, km TEXT, img TEXT, 
                  type_flag TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS temple_places 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  category TEXT DEFAULT "aarupadai",
                  place TEXT, desc TEXT, price TEXT, img TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS vehicles 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              category TEXT, name TEXT, rate TEXT, seats TEXT, 
              type TEXT, img TEXT, bata TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS bookings 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  booking_id TEXT, name TEXT, phone TEXT, details TEXT, 
                  booking_date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()

    # =====================================================
    # AUTO SEED: Vehicles table kaaliyana default data po
    # =====================================================
    existing = conn.execute('SELECT COUNT(*) FROM vehicles').fetchone()[0]
    if existing == 0:
        default_vehicles = [
            ('car',   'Suzuki Swift Dezire',   '₹13/km', '4+1',  'Sedan',        'static/images/swiftdzire.jpg',   '₹400'),
            ('car',   'Innova',                '₹19/km', '6+1',  'MUV',          'static/images/innova2.jpg',       '₹300'),
            ('car',   'Innova Crysta',         '₹21/km', '7+1',  'Luxury MUV',   'static/images/innova crysta.jpg','₹300'),
            ('car',   'Indica',                '₹11/km', '4+1',  'Hatchback',    'static/images/indica2.jpg',       '₹300'),
            ('car',   'Lodgy',                 '₹16/km', '7+1',  'MPV',          'static/images/lodgy.jpg',         '₹450'),
            ('tempo', 'Force Tempo Traveller', '₹23/km', '16+1', 'Van',          'static/images/tempo1.jpg',        '₹550'),
            ('tempo', 'Urbania Luxury Van',    '₹38/km', '16+1', 'Luxury Van',   'static/images/urbania2.jpg',      '₹700'),
            ('bus',   'AC Sleeper Bus',        '₹25/km', '22+1', 'Coaching Bus', 'static/images/minibus.jpg',       '₹600'),
        ]
        conn.executemany(
            'INSERT INTO vehicles (category, name, rate, seats, type, img, bata) VALUES (?,?,?,?,?,?,?)',
            default_vehicles
        )
        conn.commit()

    conn.close()

# ==========================================
# HOME & TOUR ROUTES
# ==========================================

@app.route('/')
def home():
    conn = get_db_connection()
    packages_db = conn.execute('SELECT * FROM main_packages').fetchall()
    conn.close()

    if not packages_db:
        conn = get_db_connection()
        initial_packages = [
            ('Temples in tamilnadu', 'best prize guranteed', 'customized pakages', 'All Major temples', 'static/images/tamilnadu.jpg', 'is_temple'),
            ('Navagraha Temples', 'best prize guranteed', 'customized packages', 'All Major Temples', '/static/images/navagraha.jpg', 'is_navagraha'),
            ('Divya Desam Temples', 'best prize guranteed', 'customized packages', 'All Major temples', '/static/images/divyadesam.jpg', 'is_divyadesam'),
            ('Kerala Tour', 'best prize guranteed', 'customized packages', 'All major places', 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80', 'is_kerala'),
            ('Karnataka Tour', 'best prize guranteed', 'customized packages', 'All major places', '/static/images/karnataka.jpg', 'is_karnataka'),
            ('Goa Tour', 'best prize guranteed', 'customized packages', 'All major places', 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80', 'is_goa')
        ]
        conn.executemany('INSERT INTO main_packages (place, price, days, km, img, type_flag) VALUES (?, ?, ?, ?, ?, ?)', initial_packages)
        conn.commit()
        packages_db = conn.execute('SELECT * FROM main_packages').fetchall()
        conn.close()

    return render_template('home.html', packages=packages_db)

@app.route('/temple-tour')
def temple_tour():
    conn = get_db_connection()
    aarupadai_db = conn.execute('SELECT * FROM temple_places WHERE category = "aarupadai"').fetchall()
    conn.close()
    if not aarupadai_db:
        conn = get_db_connection()
        initial_aarupadai = [
            ('aarupadai', 'Thirupparamkunram', 'Madurai - 1st Abode', 'Included', 'static/images/thiruparangundram.jpg'),
            ('aarupadai', 'Tiruchendur', 'Tuticorin - 2nd Abode', 'Included', 'static/images/thiruchednur.jpg'),
            ('aarupadai', 'Palani', 'Dhandayuthapani - 3rd Abode', 'Included', 'static/images/palani.jpg'),
            ('aarupadai', 'Swamimalai', 'Kumbakonam - 4th Abode', 'Included', 'static/images/swamimalai.jpg'),
            ('aarupadai', 'Thiruthani', 'Tiruvallur - 5th Abode', 'Included', 'static/images/thiruthani.jpg'),
            ('aarupadai', 'Pazhamudircholai', 'Madurai - 6th Abode', 'Included', 'static/images/pazhamuthircholai.jpg')
        ]
        conn.executemany('INSERT INTO temple_places (category, place, desc, price, img) VALUES (?,?,?,?,?)', initial_aarupadai)
        conn.commit()
        aarupadai_db = conn.execute('SELECT * FROM temple_places WHERE category = "aarupadai"').fetchall()
        conn.close()
    return render_template('home.html', modules=aarupadai_db, title="Aarupadai Veedu", temple_mode=True)

@app.route('/navagraha-tour')
def navagraha_tour():
    nav_list = [
        {'place': 'Suryanar Koil', 'desc': 'Sun (Suriyan)', 'price': 'Included', 'img': 'static/images/suriyanar.jpg'},
        {'place': 'Thingalur', 'desc': 'Moon (Chandran)', 'price': 'Included', 'img': 'static/images/thingalur.jpg'},
        {'place': 'Vaitheeswaran Koil', 'desc': 'Mars (Sevvai)', 'price': 'Included', 'img': 'static/images/vaitheeswaran.jpg'},
        {'place': 'Thiruvenkadu', 'desc': 'Mercury (Budhan)', 'price': 'Included', 'img': 'static/images/thiruvenkadu.jpg'},
        {'place': 'Alangudi', 'desc': 'Jupiter (Guru)', 'price': 'Included', 'img': 'static/images/alangudi.jpg'},
        {'place': 'Kanchanur', 'desc': 'Venus (Sukran)', 'price': 'Included', 'img': 'static/images/kanchanur.jpg'},
        {'place': 'Thirunallar', 'desc': 'Saturn (Sani)', 'price': 'Included', 'img': 'static/images/thirunallur.jpg'},
        {'place': 'Thirunageswaram', 'desc': 'Rahu', 'price': 'Included', 'img': 'static/images/thirunageswaram.jpg'},
        {'place': 'Keezhperumpallam', 'desc': 'Kethu', 'price': 'Included', 'img': 'static/images/keelaperumpallam.jpg'}
    ]
    conn = get_db_connection()
    db_navagraha = conn.execute('SELECT * FROM temple_places WHERE category = "navagraha"').fetchall()
    conn.close()
    for row in db_navagraha:
        nav_list.append({'place': row['place'], 'desc': row['desc'], 'price': row['price'], 'img': row['img']})
    return render_template('home.html', modules=nav_list, title="Navagraha Temples", temple_mode=True)

@app.route('/divyadesam-tour')
def divyadesam_tour():
    div_list = [
        {'place': 'Srirangam', 'desc': 'Sri Ranganathaswamy', 'price': 'Included', 'img': 'static/images/srirangam.jpg'},
        {'place': 'Tirupati', 'desc': 'Sri Venkateswara', 'price': 'Included', 'img': 'static/images/tirupathi.jpg'},
        {'place': 'Kanchipuram', 'desc': 'Varadharaja Perumal', 'price': 'Included', 'img': 'static/images/kanchipuram.jpg'},
        {'place': 'Srivilliputhur', 'desc': 'Andal Temple - Heritage Tower', 'price': 'Included', 'img': 'static/images/srivalliputhur.jpg'},
        {'place': 'Kumbakonam', 'desc': 'Sarangapani Perumal Temple', 'price': 'Included', 'img': 'static/images/kumbakonam.jpg'},
        {'place': 'Thiruvallur', 'desc': 'Veeraraghava Swamy Temple', 'price': 'Included', 'img': 'static/images/thiruvallur.jpg'},
    ]
    conn = get_db_connection()
    db_data = conn.execute('SELECT * FROM temple_places WHERE category = "divyadesam"').fetchall()
    conn.close()
    for row in db_data:
        div_list.append({'place': row['place'], 'desc': row['desc'], 'price': row['price'], 'img': row['img']})
    return render_template('home.html', modules=div_list, title="Divya Desam Temples", temple_mode=True)

@app.route('/kerala-tour')
def kerala_tour():
    kerala_list = [
        {'place': 'Munnar', 'desc': 'Tea Gardens & Waterfalls', 'price': 'Top 1', 'img': 'static/images/munnar.jpg'},
        {'place': 'Wayanad', 'desc': 'Edakkal Caves & Banasura Dam', 'price': 'Top 2', 'img': 'static/images/wayanad.jpg'},
        {'place': 'Alleppey', 'desc': 'Houseboat & Backwaters', 'price': 'Top 3', 'img': 'static/images/allepy.jpg'},
        {'place': 'Thekkady', 'desc': 'Wildlife Sanctuary & Boating', 'price': 'Top 4', 'img': 'static/images/thekkadi.jpg'},
        {'place': 'Vagamon', 'desc': 'Pine Forests & Meadows', 'price': 'Top 5', 'img': 'static/images/vagamon.jpg'},
        {'place': 'Varkala Beach', 'desc': 'Cliff Beach View', 'price': 'Top 6', 'img': 'static/images/varkala.jpg'},
        {'place': 'Athirappilly', 'desc': 'Grand Waterfalls (Bahubali)', 'price': 'Top 7', 'img': 'static/images/athirapally.jpg'},
        {'place': 'Kochi', 'desc': 'Fort Kochi & Marine Drive', 'price': 'Top 8', 'img': 'static/images/kochi.jpg'},
        {'place': 'Kovalam', 'desc': 'Lighthouse Beach', 'price': 'Top 9', 'img': 'static/images/kovalam.jpg'},
        {'place': 'Kumarakom', 'desc': 'Bird Sanctuary & Vembanad Lake', 'price': 'Top 10', 'img': 'static/images/kumarakom.jpg'}
    ]
    conn = get_db_connection()
    db_data = conn.execute('SELECT * FROM temple_places WHERE category = "kerala"').fetchall()
    conn.close()
    for row in db_data:
        kerala_list.append({'place': row['place'], 'desc': row['desc'], 'price': row['price'], 'img': row['img']})
    return render_template('home.html', modules=kerala_list, title="Places", temple_mode=True)

@app.route('/karnataka-tour')
def karnataka_tour():
    karnataka_list = [
        {'place': 'Coorg', 'desc': 'Scotland of India (Coffee Estates)', 'price': 'Top 1', 'img': 'static/images/coorg.jpg'},
        {'place': 'Mysore Palace', 'desc': 'Heritage & History', 'price': 'Top 2', 'img': 'static/images/mysore.jpg'},
        {'place': 'Hampi', 'desc': 'UNESCO World Heritage Ruins', 'price': 'Top 3', 'img': 'static/images/hambi.jpg'},
        {'place': 'Gokarna', 'desc': 'Om Beach & Temples', 'price': 'Top 4', 'img': 'static/images/gokarna.jpg'},
        {'place': 'Chikmagalur', 'desc': 'Mullayanagiri Peak & Coffee', 'price': 'Top 5', 'img': 'static/images/chikmagalur.jpg'},
        {'place': 'Jog Falls', 'desc': 'Famous High Waterfalls', 'price': 'Top 6', 'img': 'static/images/jog falls.jpg'},
        {'place': 'Badami', 'desc': 'Cave Temples & Rock Cut Architect', 'price': 'Top 7', 'img': 'static/images/badami.jpg'},
        {'place': 'Murudeshwar', 'desc': 'Shiva Statue & Beach', 'price': 'Top 8', 'img': 'static/images/murdeshwarar.jpg'},
        {'place': 'Bandipur', 'desc': 'Tiger Reserve Safari', 'price': 'Top 9', 'img': 'static/images/bandipur.jpg'},
        {'place': 'Belur & Halebidu', 'desc': 'Exquisite Hoysala Temples', 'price': 'Top 10', 'img': 'static/images/belur.jpg'}
    ]
    conn = get_db_connection()
    db_data = conn.execute('SELECT * FROM temple_places WHERE category = "karnataka"').fetchall()
    conn.close()
    for row in db_data:
        karnataka_list.append({'place': row['place'], 'desc': row['desc'], 'price': row['price'], 'img': row['img']})
    return render_template('home.html', modules=karnataka_list, title="Places", temple_mode=True)

@app.route('/goa-tour')
def goa_tour():
    goa_list = [
        {'place': 'Baga Beach', 'desc': 'Watersports & Nightlife', 'price': 'Top 1', 'img': 'static/images/bagabeach.jpg'},
        {'place': 'Calangute Beach', 'desc': 'Queen of Beaches', 'price': 'Top 2', 'img': 'static/images/calangute.jpg'},
        {'place': 'Dudhsagar Falls', 'desc': 'Giant Waterfall Safari', 'price': 'Top 3', 'img': 'static/images/dushsagar.jpg'},
        {'place': 'Old Goa', 'desc': 'Basilica of Bom Jesus', 'price': 'Top 4', 'img': 'static/images/old goa.jpg'},
        {'place': 'Anjuna Beach', 'desc': 'Rocky Coast & Flea Market', 'price': 'Top 5', 'img': 'static/images/anjuna beach.jpg'},
        {'place': 'Panjim', 'desc': 'Capital City & Churches', 'price': 'Top 6', 'img': 'static/images/panjim.jpg'},
        {'place': 'Fort Aguada', 'desc': 'Ocean View Lighthouse', 'price': 'Top 7', 'img': 'static/images/fort aguada.jpg'},
        {'place': 'Palolem Beach', 'desc': 'Silent Disco & Clean Water', 'price': 'Top 8', 'img': 'static/images/palolem.jpg'},
        {'place': 'Colva Beach', 'desc': 'White Sand & Peace', 'price': 'Top 9', 'img': 'static/images/colva.jpg'},
        {'place': 'River Cruise', 'desc': 'Mandovi River Luxury Cruise', 'price': 'Top 10', 'img': 'static/images/river cruise.jpg'}
    ]
    conn = get_db_connection()
    db_data = conn.execute('SELECT * FROM temple_places WHERE category = "goa"').fetchall()
    conn.close()
    for row in db_data:
        goa_list.append({'place': row['place'], 'desc': row['desc'], 'price': row['price'], 'img': row['img']})
    return render_template('home.html', modules=goa_list, title="Places", temple_mode=True)

# ==========================================
# RENTAL ROUTES
# ==========================================

@app.route('/rentals')
def rentals():
    return render_template('rentals.html')

@app.route('/cars')
def cars():
    conn = get_db_connection()
    db_cars = conn.execute('SELECT * FROM vehicles WHERE category="car"').fetchall()
    conn.close()
    car_list = [dict(row) for row in db_cars]
    return render_template('cars.html', cars=car_list, title="Car Rentals")

@app.route('/tempos')
def tempos():
    conn = get_db_connection()
    db_tempos = conn.execute('SELECT * FROM vehicles WHERE category="tempo"').fetchall()
    conn.close()
    tempo_list = [dict(row) for row in db_tempos]
    return render_template('tempos.html', vehicles=tempo_list, title="Van / Tempo Rentals")

@app.route('/buses')
def buses():
    conn = get_db_connection()
    db_buses = conn.execute('SELECT * FROM vehicles WHERE category="bus"').fetchall()
    conn.close()
    bus_list = [dict(row) for row in db_buses]
    return render_template('buses.html', vehicles=bus_list, title="Bus Bookings")

# ==========================================
# ADMIN ROUTES
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect('/admin')
    return '''
        <form method="post" style="text-align:center; margin-top:100px; font-family:Arial;">
            <h2>Sri Murugan Travels Admin</h2>
            <input type="password" name="password" placeholder="Password" style="padding:10px; margin:10px; border-radius:8px; border:1px solid #ccc;">
            <button type="submit" style="padding:10px 20px; background:#2563eb; color:white; border:none; border-radius:8px;">Login</button>
        </form>
    '''

@app.route('/admin')
def admin():
    if not session.get('admin'): return redirect('/login')
    conn = get_db_connection()
    all_bookings = conn.execute('SELECT * FROM bookings ORDER BY booking_date DESC').fetchall()
    all_vehicles  = conn.execute('SELECT * FROM vehicles ORDER BY category, id').fetchall()
    packages      = conn.execute('SELECT * FROM main_packages').fetchall()
    temple_packages = conn.execute('SELECT * FROM temple_places').fetchall()
    conn.close()
    return render_template('admin.html',
                           vehicles=all_vehicles,
                           packages=packages,
                           temple_packages=temple_packages,
                           bookings=all_bookings)

# ---------- Vehicle CRUD ----------

@app.route('/add-vehicle', methods=['POST'])
def add_vehicle():
    if not session.get('admin'): return redirect('/login')
    conn = get_db_connection()
    conn.execute('INSERT INTO vehicles (category, name, rate, seats, type, img, bata) VALUES (?,?,?,?,?,?,?)',
                 (request.form.get('category'), request.form.get('name'), request.form.get('rate'),
                  request.form.get('seats',''), request.form.get('type',''), request.form.get('img',''),
                  request.form.get('bata','')))
    conn.commit()
    conn.close()
    return redirect('/admin#vehicles-section')

@app.route('/update-vehicle', methods=['POST'])
def update_vehicle():
    if not session.get('admin'): return redirect('/login')
    conn = get_db_connection()
    conn.execute(
        'UPDATE vehicles SET name=?, category=?, rate=?, seats=?, type=?, img=?, bata=? WHERE id=?',
        (request.form.get('name'), request.form.get('category'), request.form.get('rate'),
         request.form.get('seats',''), request.form.get('type',''), request.form.get('img',''),
         request.form.get('bata',''), request.form.get('id'))
    )
    conn.commit()
    conn.close()
    return redirect('/admin#vehicles-section')

@app.route('/delete-vehicle/<int:id>')
def delete_vehicle(id):
    if not session.get('admin'): return redirect('/login')
    conn = get_db_connection()
    conn.execute('DELETE FROM vehicles WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin#vehicles-section')

# ---------- Main Package CRUD ----------

@app.route('/add', methods=['POST'])
def add_package():
    if not session.get('admin'): return redirect('/login')
    conn = get_db_connection()
    conn.execute('INSERT INTO main_packages (place, price, days, km, img, type_flag) VALUES (?, ?, ?, ?, ?, ?)',
                 (request.form.get('place'), request.form.get('price'), request.form.get('days'),
                  request.form.get('km'), request.form.get('img'), request.form.get('type')))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/delete-main-package/<int:id>')
def delete_main_package(id):
    if not session.get('admin'): return redirect('/login')
    conn = get_db_connection()
    conn.execute('DELETE FROM main_packages WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# ---------- Temple Place CRUD ----------

@app.route('/add-temple-place', methods=['POST'])
def add_temple_place():
    if not session.get('admin'): return redirect('/login')
    conn = get_db_connection()
    conn.execute('INSERT INTO temple_places (category, place, desc, price, img) VALUES (?,?,?,?,?)',
                 (request.form.get('category','aarupadai'), request.form['place'],
                  request.form['desc'], request.form['price'], request.form['img']))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/delete-temple/<int:id>')
def delete_temple(id):
    if not session.get('admin'): return redirect('/login')
    conn = get_db_connection()
    conn.execute('DELETE FROM temple_places WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# ---------- Booking CRUD ----------

@app.route('/delete-booking/<int:id>')
def delete_booking(id):
    if not session.get('admin'): return redirect('/login')
    conn = get_db_connection()
    conn.execute('DELETE FROM bookings WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/search-booking')
def search_booking():
    if not session.get('admin'): return redirect('/login')
    booking_id = request.args.get('booking_id','').strip()
    if not booking_id:
        return "Please enter a Booking ID."
    conn = get_db_connection()
    result = conn.execute('SELECT * FROM bookings WHERE booking_id = ?', (booking_id,)).fetchone()
    conn.close()
    if result:
        return f'''
        <div style="font-family:Arial;padding:30px;max-width:500px;margin:50px auto;border:2px solid #3182ce;border-radius:10px;">
            <h2 style="color:#3182ce;">Booking Found ✅</h2><hr>
            <p><b>Booking ID:</b> {result['booking_id']}</p>
            <p><b>Name:</b> {result['name']}</p>
            <p><b>Phone:</b> {result['phone']}</p>
            <p><b>Details:</b> {result['details']}</p>
            <p><b>Date:</b> {result['booking_date']}</p>
            <a href="/admin" style="padding:10px 20px;background:#333;color:white;text-decoration:none;border-radius:5px;">Back to Admin</a>
        </div>'''
    return f'''
        <div style="font-family:Arial;padding:30px;text-align:center;margin-top:50px;">
            <h2 style="color:#e53e3e;">No Booking Found for "{booking_id}" ❌</h2>
            <a href="/admin" style="padding:10px 20px;background:#333;color:white;text-decoration:none;border-radius:5px;">Back to Admin</a>
        </div>'''

# ==========================================
# BOOKING SAVE ROUTES
# ==========================================

@app.route('/book_package', methods=['POST'])
def book_package():
    data = request.json
    if not data:
        return {"status": "error", "message": "No data received"}, 400
    full_details = f"Package: {data.get('place')} | Vehicle: {data.get('vehicle')} | Pickup: {data.get('from_location')} | Date: {data.get('pickup_date')} | Duration: {data.get('days')} Days"
    booking_id = "SMT-PKG-" + str(random.randint(10000, 99999))
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO bookings (booking_id, name, phone, details) VALUES (?,?,?,?)',
                     (booking_id, data.get('name'), data.get('phone'), full_details))
        conn.commit()
        conn.close()
        return {"status": "success", "booking_id": booking_id}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route('/save-car-booking', methods=['POST'])
def save_car_booking():
    car_name = request.form.get('car_name')
    name     = request.form.get('name')
    phone    = request.form.get('phone')
    pickup   = request.form.get('pickup')
    date     = request.form.get('date')
    days     = request.form.get('days')
    full_details = f"Car: {car_name} | Pickup: {pickup} | Date: {date} | Duration: {days} Days"
    booking_id = "SMT-CAR-" + str(random.randint(10000, 99999))
    conn = get_db_connection()
    conn.execute('INSERT INTO bookings (booking_id, name, phone, details) VALUES (?,?,?,?)',
                 (booking_id, name, phone, full_details))
    conn.commit()
    conn.close()
    msg = f"*NEW CAR RENTAL BOOKING*\n\n*ID:* {booking_id}\n*Car:* {car_name}\n*Name:* {name}\n*Phone:* {phone}\n*From:* {pickup}\n*Date:* {date}\n*Days:* {days}"
    return redirect(f"https://wa.me/9345754315?text={urllib.parse.quote(msg)}")

@app.route('/save-tempo-booking', methods=['POST'])
def save_tempo_booking():
    vehicle_name = request.form.get('car_name')
    name  = request.form.get('name')
    phone = request.form.get('phone')
    pickup= request.form.get('pickup')
    date  = request.form.get('date')
    days  = request.form.get('days')
    full_details = f"Type: TEMPO | Vehicle: {vehicle_name} | Pickup: {pickup} | Date: {date} | Duration: {days} Days"
    booking_id = "SMT-TMP-" + str(random.randint(10000, 99999))
    conn = get_db_connection()
    conn.execute('INSERT INTO bookings (booking_id, name, phone, details) VALUES (?,?,?,?)',
                 (booking_id, name, phone, full_details))
    conn.commit()
    conn.close()
    msg = f"*NEW TEMPO RENTAL*\n\n*ID:* {booking_id}\n*Vehicle:* {vehicle_name}\n*Name:* {name}\n*Phone:* {phone}\n*From:* {pickup}\n*Date:* {date}\n*Days:* {days}"
    return redirect(f"https://wa.me/9345754315?text={urllib.parse.quote(msg)}")

@app.route('/save-bus-booking', methods=['POST'])
def save_bus_booking():
    vehicle_name = request.form.get('car_name')
    name  = request.form.get('name')
    phone = request.form.get('phone')
    pickup= request.form.get('pickup')
    date  = request.form.get('date')
    days  = request.form.get('days')
    full_details = f"Type: BUS | Vehicle: {vehicle_name} | Pickup: {pickup} | Date: {date} | Duration: {days} Days"
    booking_id = "SMT-BUS-" + str(random.randint(10000, 99999))
    conn = get_db_connection()
    conn.execute('INSERT INTO bookings (booking_id, name, phone, details) VALUES (?,?,?,?)',
                 (booking_id, name, phone, full_details))
    conn.commit()
    conn.close()
    msg = f"*NEW BUS BOOKING*\n\n*ID:* {booking_id}\n*Vehicle:* {vehicle_name}\n*Name:* {name}\n*Phone:* {phone}\n*From:* {pickup}\n*Date:* {date}\n*Days:* {days}"
    return redirect(f"https://wa.me/9345754315?text={urllib.parse.quote(msg)}")

# ==========================================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
