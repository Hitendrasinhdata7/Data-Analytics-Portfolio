from datetime import datetime 
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from sqlalchemy import func 
import os
import pymysql
pymysql.install_as_MySQLdb()
# Import and register the admin routes
from Admin import admin_bp  # Import blueprint from Admin.py



app = Flask(__name__)

# Register the blueprint
app.register_blueprint(admin_bp)



# Set a secret key for session management
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

# MySQL database configuration (make sure mysqlclient or pymysql is installed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:121093@localhost/automatedtradingapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'Zalamayursinh45@gmail.com')  # Replace with your email
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'weok wqvw sfrg ljkv')        # Replace with your email password

db = SQLAlchemy()
db.init_app(app)  # Make sure to call init_app to link db with the app
bcrypt = Bcrypt(app)
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


# Database Models
class Users(db.Model):
    __table_args__ = {'extend_existing': True}  # Add this line to extend the existing table if defined
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)


# Routes
@app.route('/')
def home():
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)

    # Store the sum in the session
    session['captcha_sum'] = num1 + num2

    return render_template('index.html', num1=num1, num2=num2)

@app.route('/Home')
def Home():
    email = session.get('email')
    balance = 0.00
    transaction_balance = 0.00
    profit_loss_balance = 0.00

    if email:
        user = Users.query.filter_by(email=email).first()
        if user:
            account = Account.query.filter_by(user_id=user.user_id).first()

            # Sum transactions and profit/loss
            transaction_balance = Trade.query.with_entities(func.sum(Trade.trade_price)).filter_by(user_id=user.user_id).scalar() or 0.00
            profit_loss_balance = Trade.query.with_entities(func.sum(Trade.profit_loss)).filter_by(user_id=user.user_id).scalar() or 0.00

            balance = account.balance if account else 0.00

            user = Users.query.filter_by(email=email).first()

    return render_template('home.html', balance=balance, transaction_balance=transaction_balance, profit_loss_balance=profit_loss_balance, user=user)


import random

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password_hash')
        captcha_response = request.form.get('captcha')

        # Get the correct captcha sum from the session
        correct_captcha_sum = session.get('captcha_sum')

        # Validate the CAPTCHA
        if not captcha_response.isdigit() or int(captcha_response) != correct_captcha_sum:
            flash('Invalid CAPTCHA. Please try again.', 'danger')
            return redirect(url_for('login'))

        user = Users.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            # Set session for the logged-in user's email
            session['email'] = user.email
            session['user_id'] = user.user_id
            
            # Redirect to the Home page after login
            return redirect(url_for('Home'))

        flash('Login failed. Check your email and password.', 'danger')
        return redirect(url_for('login'))

    # Generate two random numbers for the CAPTCHA on GET request
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)

    # Store the sum in the session
    session['captcha_sum'] = num1 + num2

    return render_template('index.html', num1=num1, num2=num2)


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove the user from the session
    return redirect(url_for('home'))  # Redirect to the login page

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    existing_user = Users.query.filter_by(email=email).first()

    if existing_user:
        # Check if the user is already verified
        if existing_user.is_verified == 0:
            # User exists but is not verified, send confirmation link again
            token = s.dumps(email, salt='email-confirm')

            # Send the email with the token link
            msg = Message('Confirm Your Email', sender='noreply@demo.com', recipients=[email])
            link = url_for('confirm_email', token=token, _external=True)
            msg.body = f'Your link to set the password: {link}'
            mail.send(msg)

            flash('A new confirmation email has been sent. Please check your inbox.', 'info')
            return redirect(url_for('home'))

        flash('Email already registered and verified. Please log in.', 'danger')
        return redirect(url_for('home'))

    # If the user does not exist, create a new one
    new_user = Users(email=email, is_verified=0)  # Assuming is_verified is initialized to 0
    db.session.add(new_user)
    db.session.commit()

    token = s.dumps(email, salt='email-confirm')

    # Send the email with the token link
    msg = Message('Confirm Your Email', sender='noreply@demo.com', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = f'Your link to set the password: {link}'
    mail.send(msg)

    flash('A confirmation email has been sent. Please check your inbox.', 'info')
    return redirect(url_for('home'))



@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        # Load the token, set to expire in 7 days (604800 seconds)
        email = s.loads(token, salt='email-confirm', max_age=604800)  # Token expires in 7 days

    except SignatureExpired:
        flash('The confirmation link has expired.', 'danger')
        return redirect(url_for('home'))

    user = Users.query.filter_by(email=email).first()

    if user.is_verified:
        flash('Your email is already verified. Please log in.', 'info')
        return redirect(url_for('home'))

    user.is_verified = True
    db.session.commit()
    
    # Redirect to password setting page
    return redirect(url_for('set_password', email=email))


@app.route('/set_password/<email>', methods=['GET', 'POST'])
def set_password(email):
    user = Users.query.filter_by(email=email).first()

    if request.method == 'POST':
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password_hash = hashed_password
        db.session.commit()

        flash('Your password has been set. Please log in.', 'success')
        return redirect(url_for('home'))

    return render_template('set_password.html', email=email)



from flask import session

@app.route('/save_profile', methods=['POST'])
def save_profile():
    # Get the logged-in user's email from the session
    email = session.get('email')  # Assuming you store email in session upon login

    if not email:
        flash('You must be logged in to update your profile.', 'danger')
        return redirect(url_for('home'))

    # Get form data
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    address = request.form.get('address')
    city = request.form.get('city')
    country = request.form.get('country')
    postal_code = request.form.get('postal_code')
    date_of_birth = request.form.get('date_of_birth')
    phone_number = request.form.get('phone_number')

    # Convert date_of_birth to a proper date format
    try:
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
    except ValueError:
        flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
        return redirect(url_for('Home'))

    # Find the user by email and update their profile
    user = Users.query.filter_by(email=email).first()

    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.address = address
        user.city = city
        user.country = country
        user.postal_code = postal_code
        user.date_of_birth = date_of_birth
        user.phone_number = phone_number

        # Commit the changes to the database
        db.session.commit()

        flash('Profile updated successfully!', 'success')
    else:
        flash('User not found. Please log in again.', 'danger')

    return redirect(url_for('Home'))


class Account(db.Model):
    __table_args__ = {'extend_existing': True}  # Add this line to extend the existing table if defined
    __tablename__ = 'accounts'  # Explicitly define the table name
    account_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    
    Card_Name = db.Column(db.String(100), nullable=False)
    Card_Number = db.Column(db.String(100), nullable=False)
    Expiry_Date = db.Column(db.String(10), nullable=False)
    # New fields for billing address
    address1 = db.Column(db.String(255), nullable=False)
    address2 = db.Column(db.String(255), nullable=True)
    address3 = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(100), nullable=False)

    user = db.relationship('Users', backref=db.backref('account', uselist=False))



from flask import jsonify

@app.route('/add_balance', methods=['POST'])
def add_balance():
    email = session.get('email')

    if not email:
        return jsonify({'message': 'You must be logged in to update your profile.'}), 403

    user_id = session.get('user_id')
    balance_amount = request.form.get('amount')

    try:
        balance_amount = Decimal(balance_amount)
    except (ValueError, InvalidOperation):
        return jsonify({'message': 'Invalid amount. Please enter a numeric value.'}), 400

    Card_Name = request.form.get('cardName')
    Card_Number = request.form.get('cardNumber')
    Expiry_Date = request.form.get('expiryDate')
    address1 = request.form.get('address1')
    address2 = request.form.get('address2', '')
    address3 = request.form.get('address3', '')
    country = request.form.get('country')

    if not address1 or not country:
        return jsonify({'message': 'Please fill in all required address fields.'}), 400

    account = Account.query.filter_by(user_id=user_id).first()

    if account:
        account.balance += balance_amount
        account.Card_Name = Card_Name
        account.Card_Number = Card_Number
        account.Expiry_Date = Expiry_Date
        account.address1 = address1
        account.address2 = address2
        account.address3 = address3
        account.country = country
        message = 'Balance and billing address updated successfully!'
    else:
        new_account = Account(
            user_id=user_id, 
            balance=balance_amount,
            Card_Name = Card_Name,
            Card_Number = Card_Number,
            Expiry_Date = Expiry_Date,
            address1=address1,
            address2=address2,
            address3=address3,
            country=country
        )
        db.session.add(new_account)
        message = 'Account created and balance set with billing address successfully!'

    db.session.commit()
    return jsonify({'message': message}), 200



class Trade(db.Model):
    __tablename__ = 'trades' 
    trade_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), nullable=False)
    asset_id = db.Column(db.Integer, nullable=False)
    trade_type = db.Column(db.String(10), nullable=False)  # 'buy' or 'sell'
    order_type = db.Column(db.String(10), nullable=False)
    trade_amount = db.Column(db.Numeric(10, 2), nullable=False)
    trade_price = db.Column(db.Numeric(10, 2), nullable=False)
    stop_loss = db.Column(db.Numeric(10, 2), nullable=True)
    take_profit = db.Column(db.Numeric(10, 2), nullable=True)
    leverage = db.Column(db.Numeric(10, 2), nullable=True)
    trade_status = db.Column(db.String(10), nullable=False)  # 'Open', 'Auto', 'Closed'
    open_time = db.Column(db.DateTime, nullable=True)
    close_time = db.Column(db.DateTime, nullable=True)
    profit_loss = db.Column(db.Numeric(10, 2), nullable=True)


@app.route('/get_user_trades', methods=['GET'])
def get_user_trades():
    # Get the user ID from the session
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    try:
        # Fetch all 'buy' trades for the specific user_id
        buy_trades = Trade.query.filter_by(user_id=user_id, trade_type='Buy', trade_status='Open').all()

        # Prepare the trade data for JSON response
        trades_data = [
            {
                'trade_id': trade.trade_id,
                'asset_id': trade.asset_id,
                'trade_status': trade.trade_status,
                'trade_type': trade.trade_type,
                'trade_amount': trade.trade_amount,
                'trade_price': trade.trade_price
            } for trade in buy_trades
        ]
        return jsonify({'trades': trades_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
   

@app.route('/trade_history', methods=['GET'])
def trade_history():
    # Get the user ID from the session
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    try:
        # Fetch all 'buy' trades for the specific user_id
        buy_trades = Trade.query.filter_by(user_id=user_id, trade_type='Buy', trade_status='Open').all()

        # Render the template and pass the trade data
        return render_template('TradeHistory.html', trades=buy_trades)

    except Exception as e:
        print(f"Error fetching buy trades: {e}")
        return jsonify({'error': 'Failed to fetch trades'}), 500



from flask import Flask, request, jsonify, session
from datetime import datetime
from decimal import Decimal, InvalidOperation

@app.route('/place_trade', methods=['POST'])
def place_trade():
    data = request.get_json()

    # Extract user and account from the session
    user_id = session.get('user_id')  # Ensure user_id is stored in the session

    if not user_id:
        return jsonify(message="User not authenticated."), 401

    # Extract and validate trade details from the request
    trade_type = data.get('trade_type')
    asset_id = data.get('asset_id')
    trade_status = data.get('trade_status')

    if trade_type not in ['buy', 'sell'] or not asset_id:
        return jsonify(message="Invalid trade type or asset ID."), 400

    # Validate and ensure the presence of numeric values
    try:
        if not data.get('trade_amount') or not data.get('trade_price'):
            return jsonify(message="Trade amount and price are required."), 400

        trade_amount = Decimal(data.get('trade_amount'))
        trade_price = Decimal(data.get('trade_price'))

        stop_loss = Decimal(data.get('stop_loss')) if data.get('stop_loss') else None
        take_profit = Decimal(data.get('take_profit')) if data.get('take_profit') else None
        leverage = Decimal(data.get('leverage')) if data.get('leverage') else None
    except (ValueError, InvalidOperation):
        return jsonify(message="Invalid numeric value provided."), 400

    if trade_type == 'buy':
        # Create a new trade entry for a buy action
        new_trade = Trade(
            user_id=user_id,
            asset_id=asset_id,
            trade_type=trade_type,
            order_type='market',
            trade_amount=trade_amount,
            trade_price=trade_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            leverage=leverage,
            trade_status='Open',
            close_time=None,
        )

        try:
            db.session.add(new_trade)
            db.session.commit()
            return jsonify(message="Trade placed successfully!"), 201
        except Exception as e:
            db.session.rollback()
            print(f"Error while saving trade: {str(e)}")
            return jsonify(message="Error placing trade, please try again later."), 500

    elif trade_type == 'sell':
        trade_id = data.get('trade_id')
        if not trade_id:
            return jsonify(message="Trade ID is required for selling."), 400

        # Find the trade that needs to be closed
        trade = Trade.query.filter_by(trade_id=trade_id, user_id=user_id).first()
        if trade is None:
            return jsonify(message="Trade not found."), 404
        if trade.trade_status != 'Open':
            return jsonify(message="Trade is not open, cannot close it."), 400

        # Close the trade
        trade.trade_status = 'Closed'
        trade.trade_type = 'Sell'
        trade.close_time = datetime.utcnow()
        
        # Calculate profit/loss
        buy_price = trade.trade_price
        sell_price = trade_price
        trade.profit_loss = Decimal(sell_price) - Decimal(buy_price)

        try:
            db.session.commit()
            return jsonify(message="Trade closed successfully!", profit_loss=float(trade.profit_loss)), 200
        except Exception as e:
            db.session.rollback()
            print(f"Error while closing trade for trade_id {trade_id}: {str(e)}")
            return jsonify(message="Error closing trade, please try again later."), 500
        
    return jsonify(message="Invalid trade type provided."), 400


# Define the route for LivePhoto
@app.route('/live_photo')
def live_photo():
    return render_template('LivePhoto.html')


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    aadhar = db.Column(db.LargeBinary, nullable=True)
    pan = db.Column(db.LargeBinary, nullable=True)
    live_photo = db.Column(db.LargeBinary, nullable=True)
    entry_ip = db.Column(db.String(45), nullable=True)  # IPv6 compatible
    entry_mac = db.Column(db.String(17), nullable=True)  # MAC address format XX:XX:XX:XX:XX:XX
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, aadhar=None, pan=None, live_photo=None, entry_ip=None, entry_mac=None):
        self.user_id = user_id
        self.aadhar = aadhar
        self.pan = pan
        self.live_photo = live_photo
        self.entry_ip = entry_ip
        self.entry_mac = entry_mac
        self.entry_date = datetime.utcnow()

from flask import request
import re
import os
import uuid

def get_user_ip_mac():
    # Get IP address from the request
    user_ip = request.remote_addr

    # Attempt to get the MAC address (Note: Not available over the internet)
    # Here we're using a placeholder because MAC can't be obtained via HTTP requests
    user_mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    return user_ip, user_mac
   
from flask import request, jsonify, session
import base64
from datetime import datetime


# Route to save live image
@app.route('/save_live_image', methods=['POST'])
def save_live_image():
    # Ensure user is authenticated
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 403

    data = request.json

    # Extract images from the request
    aadhar_image = data.get('aadhar')
    pan_image = data.get('pan')
    live_photo = data.get('live')

    # Validate that required images are provided
    if not aadhar_image or not pan_image or not live_photo:
        return jsonify({'status': 'error', 'message': 'Missing required images'}), 400

    # Decode the base64-encoded images
    try:
        aadhar_binary = base64.b64decode(aadhar_image.split(',')[1])
        pan_binary = base64.b64decode(pan_image.split(',')[1])
        live_binary = base64.b64decode(live_photo.split(',')[1])
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error decoding images: {str(e)}'}), 400

    # Capture Entry_IP and Entry_MAC
    entry_ip, entry_mac = get_user_ip_mac()

    # Check if the user already has uploaded documents
    existing_record = Document.query.filter_by(user_id=user_id).first()

    try:
        if existing_record:
            # Update the existing record
            existing_record.aadhar = aadhar_binary
            existing_record.pan = pan_binary
            existing_record.live_photo = live_binary
            existing_record.entry_ip = entry_ip
            existing_record.entry_mac = entry_mac
            existing_record.entry_date = datetime.utcnow()  # Update entry date
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Documents updated successfully'}), 200
        else:
            # Insert a new record
            new_document = Document(
                user_id=user_id,
                aadhar=aadhar_binary,
                pan=pan_binary,
                live_photo=live_binary,
                entry_ip=entry_ip,
                entry_mac=entry_mac
            )
            db.session.add(new_document)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Documents saved successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error while saving documents: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Error saving documents, please try again later.'}), 500

# Route to show a preview of uploaded documents in HTML for the logged-in user
@app.route('/show_preview', methods=['GET'])
def show_preview():
    if 'user_id' not in session:
        return "User not logged in", 403

    user_id = session['user_id']

    doc = Document.query.filter_by(user_id=user_id).first()

    if doc:
        # Convert binary data to base64 for display in the HTML
        aadhar_img = base64.b64encode(doc.aadhar).decode('utf-8')
        pan_img = base64.b64encode(doc.pan).decode('utf-8')
        live_img = base64.b64encode(doc.live_photo).decode('utf-8')

        return render_template('LivePhoto.html', aadhar_img=aadhar_img, pan_img=pan_img, live_img=live_img)
    else:
        return "No documents found for this user", 404

# Route to retrieve a specific image as a direct GET request (for the session user)
@app.route('/get_existing_images', methods=['GET'])
def get_existing_images():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 403

    user_id = session['user_id']
    doc = Document.query.filter_by(user_id=user_id).first()

    if doc:
        aadhar_img = base64.b64encode(doc.aadhar).decode('utf-8') if doc.aadhar else None
        pan_img = base64.b64encode(doc.pan).decode('utf-8') if doc.pan else None
        live_img = base64.b64encode(doc.live_photo).decode('utf-8') if doc.live_photo else None

        return jsonify({
            'status': 'success',
            'aadhar_image': aadhar_img,
            'pan_image': pan_img,
            'live_image': live_img
        })
    else:
        return jsonify({'status': 'error', 'message': 'No images found'}), 404



@app.route('/filter_trades', methods=['POST'])
def filter_trades():
    # Get form data
    trade_type = request.form.get('balance')
    start_date = request.form.get('from')
    end_date = request.form.get('to')

    # Initialize the query
    query = Trade.query

    # Filter by trade type if specified
    if trade_type:
        query = query.filter_by(trade_type=trade_type)

    # Filter by date range if both dates are provided
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        query = query.filter(Trade.open_time >= start_date, Trade.open_time <= end_date)

    # Fetch the filtered trades
    trades = query.all()

      # Render the template with trades data and selected trade type
    return render_template('TradeHistory.html', trades=trades, selected_trade_type=trade_type)


if __name__ == '__main__':
    app.run(debug=True)
