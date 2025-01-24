from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from sqlalchemy import func
import base64
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define a blueprint for the admin section
admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

# Helper function to calculate balance, user count, and profit/loss
def calculate_metrics(db):
    from app import Account, Users
    try:
        total_balance = db.session.query(func.sum(Account.balance)).scalar() or 0.00
        user_count = db.session.query(func.count(Users.user_id)).scalar() or 0
        profit_loss_balance = total_balance - 10000 if total_balance > 10000 else -(10000 - total_balance)
        return total_balance, user_count, profit_loss_balance
    except Exception as e:
        logging.error(f"Error in calculating metrics: {e}")
        return 0.00, 0, 0.00

# Helper function to encode images to base64
def encode_documents(documents):
    encoded_docs = []
    for document in documents:
        try:
            if document.aadhar:
                document.aadhar = base64.b64encode(document.aadhar).decode('utf-8')
            if document.pan:
                document.pan = base64.b64encode(document.pan).decode('utf-8')
            if document.live_photo:
                document.live_photo = base64.b64encode(document.live_photo).decode('utf-8')

                  # Add IP address, MAC address, and entry date
            document.entry_ip = document.entry_ip if hasattr(document, 'entry_ip') else 'N/A'
            document.entry_mac = document.entry_mac if hasattr(document, 'entry_mac') else 'N/A'
            document.entry_date = document.entry_date if hasattr(document, 'entry_date') else 'N/A'
            encoded_docs.append(document)
        except Exception as e:
            logging.warning(f"Error encoding document ID {document.user_id}: {e}")
    return encoded_docs

# Admin dashboard route
@admin_bp.route('/Admin')
def Admin():
    from app import db, Account, Users, Document
    total_balance, user_count, profit_loss_balance = calculate_metrics(db)
    documents = encode_documents(Document.query.all())
    return render_template('Admin.html', balance=total_balance, User=user_count, profit_loss_balance=profit_loss_balance, documents=documents)

# Document verification route
@admin_bp.route('/admin_documents', methods=['GET', 'POST'])
def admin_documents():
    from app import db, Users, Document
    from flask import flash, redirect, url_for, render_template, request

    # Initialize variables for metrics
    total_balance, user_count, profit_loss_balance = calculate_metrics(db)

    if request.method == 'POST':
        # Get the list of user IDs from the checked checkboxes
        verified_documents = request.form.getlist('verified_documents')

        if verified_documents:
            for user_id in verified_documents:
                try:
                    # Fetch the user by user_id
                    user = Users.query.filter_by(user_id=user_id).first()
                    if user:
                        # Update the user's verification status
                        user.two_factor_enabled = 1
                        db.session.commit()
                        flash(f'Documents for User ID {user_id} have been verified.', 'success')
                except Exception as e:
                    logging.error(f"Error verifying user ID {user_id}: {e}")
                    flash(f'Error verifying documents for User ID {user_id}.', 'danger')

            flash(f'{len(verified_documents)} user(s) verified successfully!', 'success')
        else:
            flash('No documents were selected for verification.', 'warning')

        return redirect(url_for('admin.admin_documents'))

    # GET Request: Display documents with metrics
    documents = encode_documents(Document.query.all())
    return render_template('Admin.html', balance=total_balance, User=user_count, profit_loss_balance=profit_loss_balance, documents=documents)
