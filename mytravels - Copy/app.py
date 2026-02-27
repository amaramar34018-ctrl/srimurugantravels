import sqlite3
import os
import random          # PUDHUSA ADD PANNATHU
import urllib.parse    # PUDHUSA ADD PANNATHU
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__, template_folder='templates', static_folder='static')
DB_PATH = os.path.join(os.path.dirname(__file__), 'travels.db')
app.secret_key = "sri_murugan_travels_secret" # Admin login-kaga

# ==========================================
# STEP 1: DATABASE CONNECTION SETUP
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'travels.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_db_connection()
    # Pathaya table (Main Packages)
    conn.execute('''CREATE TABLE IF NOT EXISTS main_packages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  place TEXT, price TEXT, days TEXT, km TEXT, img TEXT, 
                  type_flag TEXT)''')
    
    # PUDHU TABLE: Ippo 'category' column sethurukkom
    conn.execute('''CREATE TABLE IF NOT EXISTS temple_places 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  category TEXT DEFAULT "aarupadai",
                  place TEXT, desc TEXT, price TEXT, img TEXT)''')
    # Vehicles table (Cars, Tempos, Buses ellathukkum)
    conn.execute('''CREATE TABLE IF NOT EXISTS vehicles 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              category TEXT, name TEXT, rate TEXT, seats TEXT, 
              type TEXT, img TEXT, bata TEXT)''')
              
    # PUDHUSA ADD PANNATHU: Bookings save panna table
    conn.execute('''CREATE TABLE IF NOT EXISTS bookings 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  booking_id TEXT, name TEXT, phone TEXT, details TEXT, 
                  booking_date DATETIME DEFAULT CURRENT_TIMESTAMP)''')
                  
    conn.commit()
    conn.close()

# ==========================================
# ROUTES
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
    # CHANGE 1: Aarupadai category mattum edukrom
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
    # Pazhaya Hardcoded List
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

    # CHANGE 2: Database-la irundhu Navagraha category data edukrom
    conn = get_db_connection()
    db_navagraha = conn.execute('SELECT * FROM temple_places WHERE category = "navagraha"').fetchall()
    conn.close()

    # Database data-vai pazhaya list kooda serkirom
    for row in db_navagraha:
        nav_list.append({
            'place': row['place'],
            'desc': row['desc'],
            'price': row['price'],
            'img': row['img']
        })

    return render_template('home.html', modules=nav_list, title="Navagraha Temples", temple_mode=True)

# ... (Mela irukkura code ellam apdiye irukkattum) ...

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
    # FIX: Database-la irundhu divyadesam data-vai edukrom
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
    # FIX: Database-la irundhu kerala data-vai edukrom
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
    # FIX: Database-la irundhu karnataka data-vai edukrom
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
    # FIX: Database-la irundhu goa data-vai edukrom
    conn = get_db_connection()
    db_data = conn.execute('SELECT * FROM temple_places WHERE category = "goa"').fetchall()
    conn.close()
    for row in db_data:
        goa_list.append({'place': row['place'], 'desc': row['desc'], 'price': row['price'], 'img': row['img']})

    return render_template('home.html', modules=goa_list, title="Places", temple_mode=True)

# ... (Keezha irukkura Rental, Admin, Delete routes ellam apdiye irukkattum) ...
@app.route('/rentals')
def rentals():
    return render_template('rentals.html')

@app.route('/cars')
def cars():
    # 1. Unga pazhaya hardcoded list (Ethuvum maathala, apdiye irukku)
    car_list = [
        {'name': 'Suzuki Swift Dezire', 'rate': '₹13/km', 'seats': '4+1', 'type': 'Sedan', 'img':'static/images/swiftdzire.jpg', 'bata': '₹400'},
        {'name': 'Innova', 'rate': '₹19/km', 'seats': '6+1', 'type': 'MUV','img':'static/images/innova2.jpg', 'bata': '₹300'},
        {'name': 'Innova Crysta', 'rate': '₹21/km', 'seats': '7+1', 'type': 'MUV','img':'static/images/innova crysta.jpg', 'bata': '₹300'},
        {'name': 'Indica', 'rate': '₹11/km', 'seats': '4+1', 'type': 'Hatchback','img':'static/images/indica2.jpg', 'bata': '₹300'},
        {'name': 'Lodgy', 'rate': '₹16/km', 'seats': '7+1', 'type': 'MPV','img':'static/images/lodgy.jpg', 'bata': '₹450'}
    ]

    # 2. Database-la irundhu pudhusa add panna cars-ai edukrom
    conn = get_db_connection()
    # 'vehicles' table create panni irukkom la, adhula irundhu 'car' category mattum edukrom
    db_cars = conn.execute('SELECT * FROM vehicles WHERE category="car"').fetchall()
    conn.close()

    # 3. Database data-vai pazhaya list kooda serkirom
    for row in db_cars:
        car_list.append({
            'name': row['name'],
            'rate': row['rate'],
            'seats': row['seats'],
            'type': row['type'],
            'img': row['img'],
            'bata': row['bata']
        })

    return render_template('cars.html', cars=car_list, title="Car Rentals")

@app.route('/tempos')
def tempos():
    # 1. Unga pazhaya tempo list (mela irukkum)
    tempo_list = [
        {'name': 'Force Tempo Traveller', 'rate': '₹23/km', 'seats': '16+1', 'img': '/static/images/tempo1.jpg', 'bata': '₹550'},
        {'name': 'Urbania Luxury Van', 'rate': '₹38/km', 'seats': '16+1', 'img': '/static/images/urbania2.jpg', 'bata': '₹700'}
    ]

    # 2. Database-la irundhu 'tempo' category edukrom
    conn = get_db_connection()
    db_tempos = conn.execute('SELECT * FROM vehicles WHERE category="tempo"').fetchall()
    conn.close()

    # 3. Database data-vai append pandrom
    for row in db_tempos:
        tempo_list.append({
            'name': row['name'],
            'rate': row['rate'],
            'seats': row['seats'],
            'type': row['type'],
            'img': row['img'],
            'bata': row['bata']
        })

    return render_template('tempos.html', vehicles=tempo_list, title="Van / Tempo Rentals")

@app.route('/buses')
def buses():
    # 1. Pazhaya bus list
    bus_list = [
        {'name': 'AC Sleeper Bus', 'rate': '₹25/km', 'seats': '22+1', 'img': 'static/images/minibus.jpg'}
    ]

    # 2. Database-la irundhu 'bus' category edukrom
    conn = get_db_connection()
    db_buses = conn.execute('SELECT * FROM vehicles WHERE category="bus"').fetchall()
    conn.close()

    # 3. Database data-vai sethukrom
    for row in db_buses:
        bus_list.append({
            'name': row['name'],
            'rate': row['rate'],
            'seats': row['seats'],
            'type': row['type'],
            'img': row['img']
        })

    return render_template('buses.html', vehicles=bus_list, title="Bus Bookings")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect('/admin')
    return '''
        <form method="post" style="text-align:center; margin-top:100px;">
            <h2>Sri Murugan Travels Admin</h2>
            <input type="password" name="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/admin')
def admin():
    if not session.get('admin'): return redirect('/login')
    
    conn = get_db_connection()
    
    # 1. PUDHUSA ADD PANNATHU: Bookings table-la irundhu details edukrom
    # Latest bookings mela vara maari 'DESC' (Descending) order-la edukrom
    all_bookings = conn.execute('SELECT * FROM bookings ORDER BY booking_date DESC').fetchall()
    
    # 2. Vehicles fetch panrom
    db_vehicles = conn.execute('SELECT * FROM vehicles').fetchall()
    
    vehicles_to_show = []
    if not db_vehicles:
        defaults = [
            {'id': 'old', 'category': 'car', 'name': 'Suzuki Swift Dezire', 'type': 'Sedan', 'rate': '₹13/km', 'bata': '₹400'},
            {'id': 'old', 'category': 'car', 'name': 'Toyota Etios', 'type': 'Executive Sedan', 'rate': '₹14/km', 'bata': '₹400'},
            {'id': 'old', 'category': 'car', 'name': 'Innova Crysta', 'type': 'Luxury MUV', 'rate': '₹21/km', 'bata': '₹300'},
            {'id': 'old', 'category': 'tempo', 'name': 'Force Tempo Traveller', 'type': 'Van', 'rate': '₹23/km', 'bata': '₹550'},
            {'id': 'old', 'category': 'tempo', 'name': 'Urbania', 'type': 'Luxury Van', 'rate': '₹38/km', 'bata': '₹700'},
            {'id': 'old', 'category': 'bus', 'name': 'AC Sleeper Bus', 'type': 'Coaching Bus', 'rate': '₹25/km', 'bata': '-'}
        ]
        vehicles_to_show = defaults
    else:
        for row in db_vehicles:
            vehicles_to_show.append({
                'id': row['id'],
                'category': row['category'],
                'name': row['name'],
                'type': row['type'],
                'rate': row['rate'],
                'bata': row['bata']
            })

    # 3. Packages fetch panrom
    packages = conn.execute('SELECT * FROM main_packages').fetchall()
    temple_packages = conn.execute('SELECT * FROM temple_places').fetchall()
    conn.close()

    # 4. Final step: 'bookings=all_bookings' nu sethu anupunga
    return render_template('admin.html', 
                           vehicles=vehicles_to_show, 
                           packages=packages, 
                           temple_packages=temple_packages, 
                           bookings=all_bookings)

@app.route('/add-temple-place', methods=['POST'])
def add_temple_place():
    if not session.get('admin'): return redirect('/login')
    
    # CHANGE 3: Admin form-la irundhu vara 'category'-ai (navagraha / aarupadai) database-la add panrom
    category = request.form.get('category', 'aarupadai')
    p = (category, request.form['place'], request.form['desc'], request.form['price'], request.form['img'])
    
    conn = get_db_connection()
    conn.execute('INSERT INTO temple_places (category, place, desc, price, img) VALUES (?,?,?,?,?)', p)
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/add-vehicle', methods=['POST'])
def add_vehicle():
    if not session.get('admin'): return redirect('/login')
    
    # .get() use panna error varaathu
    category = request.form.get('category')
    name = request.form.get('name')
    rate = request.form.get('rate')
    seats = request.form.get('seats', '')
    v_type = request.form.get('type', '') # 'type' illanaalum empty-ah edukkum
    img = request.form.get('img', '')
    bata = request.form.get('bata', '')
    
    conn = get_db_connection()
    conn.execute('INSERT INTO vehicles (category, name, rate, seats, type, img, bata) VALUES (?,?,?,?,?,?,?)', 
                 (category, name, rate, seats, v_type, img, bata))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/delete-vehicle/<int:id>')
def delete_vehicle(id):
    if not session.get('admin'): return redirect('/login')
    conn = get_db_connection()
    conn.execute('DELETE FROM vehicles WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

@app.route('/update-vehicle', methods=['POST'])
def update_vehicle():
    if not session.get('admin'): return redirect('/login')
    
    v_id = request.form.get('id')
    rate = request.form.get('rate')
    bata = request.form.get('bata')
    name = request.form.get('name')
    category = request.form.get('category')

    conn = get_db_connection()
    if v_id == 'old':
        # Pazhaya car-ai database-kku move pandrom pudhu rate-oda
        conn.execute('INSERT INTO vehicles (category, name, rate, bata) VALUES (?,?,?,?)', 
                     (category, name, rate, bata))
    else:
        # Already database-la irukkura car-ai update pandrom
        conn.execute('UPDATE vehicles SET rate = ?, bata = ? WHERE id = ?', (rate, bata, v_id))
    
    conn.commit()
    conn.close()
    return redirect('/admin')

# ==========================================
# MAIN PACKAGES - ADD & DELETE (Missing Routes)
# ==========================================

@app.route('/add', methods=['POST'])
def add_package():
    if not session.get('admin'): return redirect('/login')
    
    # Admin form-la irundhu data-vai edukrom
    place = request.form.get('place')
    price = request.form.get('price')
    days = request.form.get('days')
    km = request.form.get('km')
    img = request.form.get('img')
    type_flag = request.form.get('type') # is_kerala, is_goa, etc.

    conn = get_db_connection()
    conn.execute('INSERT INTO main_packages (place, price, days, km, img, type_flag) VALUES (?, ?, ?, ?, ?, ?)',
                 (place, price, days, km, img, type_flag))
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

@app.route('/delete-temple/<int:id>')
def delete_temple(id):
    if not session.get('admin'): return redirect('/login')
    conn = get_db_connection()
    conn.execute('DELETE FROM temple_places WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/admin')

# ==========================================
# WHATSAPP & BOOKING ROUTES (PUDHUSA ADD PANNATHU)
# ==========================================

# ... (Mela ulla unga import and db connection code ellam apdiye irukkattum) ...

# ==========================================
# WHATSAPP & BOOKING ROUTES (UPDATED)
# ==========================================

# ITHU UNGA PAZHAYA PACKAGE BOOKING ROUTE (Ethuvum maathala)
@app.route('/save-booking', methods=['POST'])
def save_booking():
    name = request.form.get('name', 'Customer')
    phone = request.form.get('phone', 'No Phone')
    details = request.form.get('details', 'Website Enquiry')
    
    booking_id = "SMT-" + str(random.randint(10000, 99999))
    
    conn = get_db_connection()
    conn.execute('INSERT INTO bookings (booking_id, name, phone, details) VALUES (?,?,?,?)', 
                  (booking_id, name, phone, details))
    conn.commit()
    conn.close()
    
    whatsapp_number = "9345754315" # UNGA NUMBER MATHI IRUKAEN
    msg = f"Hello Sri Murugan Travels!\n\nName: {name}\nPhone: {phone}\nEnquiry: {details}\n*My Booking ID: {booking_id}*"
    safe_msg = urllib.parse.quote(msg)
    
    return redirect(f"https://wa.me/{'9345754315'}?text={safe_msg}")

# PUDHUSA ADD PANNATHU: Car Rental-ai Database-la save panna
@app.route('/search-booking')
def search_booking():
    if not session.get('admin'): return redirect('/login')
    
    booking_id = request.args.get('booking_id', '').strip() # Space iruntha remove pannidum
    
    if not booking_id:
        return "Please enter a Booking ID."

    conn = get_db_connection()
    # Query-ah check pannunga
    result = conn.execute('SELECT * FROM bookings WHERE booking_id = ?', (booking_id,)).fetchone()
    conn.close()
    
    if result:
        # result oru dictionary maari behave pannum (Row factory irukira nala)
        return f'''
        <div style="font-family: Arial; padding: 30px; max-width: 500px; margin: auto; border: 2px solid #3182ce; border-radius: 10px; margin-top: 50px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h2 style="color: #3182ce;">Booking Found! ✅</h2>
            <hr>
            <p><b>Booking ID:</b> {result['booking_id']}</p>
            <p><b>Name:</b> {result['name']}</p>
            <p><b>Phone:</b> {result['phone']}</p>
            <p><b>Details:</b> {result['details']}</p>
            <p><b>Date & Time:</b> {result['booking_date']}</p>
            <br>
            <a href="/admin" style="padding: 10px 20px; background: #333; color: white; text-decoration: none; border-radius: 5px;">Back to Admin</a>
        </div>
        '''
    else:
        return f'''
        <div style="font-family: Arial; padding: 30px; text-align: center; margin-top: 50px;">
            <h2 style="color: #e53e3e;">No Booking Found for "{booking_id}" ❌</h2>
            <p>Check if the ID is correct (Example: SMT-CAR-5806)</p>
            <br>
            <a href="/admin" style="padding: 10px 20px; background: #333; color: white; text-decoration: none; border-radius: 5px;">Back to Admin</a>
        </div>
        '''
@app.route('/save-car-booking', methods=['POST']) # Intha spell check pannunga
def save_car_booking():
    car_name = request.form.get('car_name')
    name = request.form.get('name')
    phone = request.form.get('phone')
    pickup = request.form.get('pickup')
    date = request.form.get('date')
    days = request.form.get('days')

    full_details = f"Car: {car_name} | Pickup: {pickup} | Date: {date} | Duration: {days} Days"
    booking_id = "SMT-CAR-" + str(random.randint(10000, 99999))

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO bookings (booking_id, name, phone, details) VALUES (?,?,?,?)', 
                      (booking_id, name, phone, full_details))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")
        return "Database-la save panna mudiyala, details check pannunga!"

    whatsapp_number = "9345754315"
    msg = f"*NEW CAR RENTAL BOOKING*\n\n*ID:* {booking_id}\n*Car:* {car_name}\n*Name:* {name}\n*Phone:* {phone}\n*From:* {pickup}\n*Date:* {date}\n*Days:* {days}"
    safe_msg = urllib.parse.quote(msg)

    return redirect(f"https://wa.me/{whatsapp_number}?text={safe_msg}")
    

    # WhatsApp-kku message ready panrom
    whatsapp_number = "9345754315"
    msg = f"*NEW CAR RENTAL BOOKING*\n\n*ID:* {booking_id}\n*Car:* {car_name}\n*Name:* {name}\n*Phone:* {phone}\n*From:* {pickup}\n*Date:* {date}\n*Days:* {days}"
    safe_msg = urllib.parse.quote(msg)

    return redirect(f"https://wa.me/9345754315?text={safe_msg}")

# ... (Keezha ulla unga search-booking route and main block apdiye irukkattum) ...
@app.route('/save-tempo-booking', methods=['POST'])
def save_tempo_booking():
    vehicle_name = request.form.get('car_name') # Modal-la irundhu varra name
    name = request.form.get('name')
    phone = request.form.get('phone')
    pickup = request.form.get('pickup')
    date = request.form.get('date')
    days = request.form.get('days')

    # Inga 'TEMPO' nu mention panrom, details-la store aagum pothu clear-ah irukkum
    full_details = f"Type: TEMPO | Vehicle: {vehicle_name} | Pickup: {pickup} | Date: {date} | Duration: {days} Days"
    booking_id = "SMT-TMP-" + str(random.randint(10000, 99999)) # TMP nu start aagum

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO bookings (booking_id, name, phone, details) VALUES (?,?,?,?)', 
                      (booking_id, name, phone, full_details))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")
        return "Database error! Please try again."

    # WhatsApp-ku anupura message
    whatsapp_number = "9345754315"
    msg = f"*NEW TEMPO RENTAL*\n\n*ID:* {booking_id}\n*Vehicle:* {vehicle_name}\n*Name:* {name}\n*Phone:* {phone}\n*From:* {pickup}\n*Date:* {date}\n*Days:* {days}"
    safe_msg = urllib.parse.quote(msg)

    return redirect(f"https://wa.me/{whatsapp_number}?text={safe_msg}")
@app.route('/save-bus-booking', methods=['POST'])
def save_bus_booking():
    vehicle_name = request.form.get('car_name') 
    name = request.form.get('name')
    phone = request.form.get('phone')
    pickup = request.form.get('pickup')
    date = request.form.get('date')
    days = request.form.get('days')

    # Booking details-la 'BUS' nu mention panrom
    full_details = f"Type: BUS | Vehicle: {vehicle_name} | Pickup: {pickup} | Date: {date} | Duration: {days} Days"
    booking_id = "SMT-BUS-" + str(random.randint(10000, 99999)) # SMT-BUS nu start aagum

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO bookings (booking_id, name, phone, details) VALUES (?,?,?,?)', 
                      (booking_id, name, phone, full_details))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")
        return "Database error! Please try again."

    # WhatsApp message for Bus
    whatsapp_number = "9345754315"
    msg = f"*NEW BUS BOOKING*\n\n*ID:* {booking_id}\n*Vehicle:* {vehicle_name}\n*Name:* {name}\n*Phone:* {phone}\n*From:* {pickup}\n*Date:* {date}\n*Days:* {days}"
    safe_msg = urllib.parse.quote(msg)

    return redirect(f"https://wa.me/{whatsapp_number}?text={safe_msg}")

@app.route('/delete-booking/<int:id>')
def delete_booking(id):
    if not session.get('admin'): return redirect('/login')
    
    try:
        conn = get_db_connection()
        # Row ID-ah vechu delete panrom
        conn.execute('DELETE FROM bookings WHERE id = ?', (id,))
        conn.commit() # Ithu thaan romba mukkiyam! Appo thaan save aagum.
        conn.close()
    except Exception as e:
        print(f"Delete Error: {e}")
    return redirect('/admin') 
# ==========================================
# TOUR PACKAGE BOOKING ROUTE (PUDHUSA ADD PANNATHU)
# ==========================================

@app.route('/book_package', methods=['POST'])
def book_package():
    # AJAX moolama data varum pothu request.json use pannanum
    data = request.json
    
    if not data:
        return {"status": "error", "message": "No data received"}, 400

    place = data.get('place')
    vehicle = data.get('vehicle')
    name = data.get('name')
    phone = data.get('phone')
    from_loc = data.get('from_location')
    date = data.get('pickup_date')
    days = data.get('days')

    # Booking details-ah formatted string-ah mathikurom
    full_details = f"Package: {place} | Vehicle: {vehicle} | Pickup: {from_loc} | Date: {date} | Duration: {days} Days"
    
    # Unique ID generate panrom
    booking_id = "SMT-PKG-" + str(random.randint(10000, 99999))

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO bookings (booking_id, name, phone, details) VALUES (?,?,?,?)', 
                     (booking_id, name, phone, full_details))
        conn.commit()
        conn.close()
        return {"status": "success", "booking_id": booking_id}, 200
    except Exception as e:
        print(f"Database Error: {e}")
        return {"status": "error", "message": str(e)}, 500

# ==========================================
# END OF NEW ROUTE
# ==========================================
if __name__ == '__main__':
    init_db()  # Database update
    # Inga mathavum:
    app.run(host='0.0.0.0', port=10000)


