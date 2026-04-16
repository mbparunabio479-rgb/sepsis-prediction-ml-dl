from flask import Blueprint, render_template, request, jsonify, current_app, session, redirect, url_for
import json
from datetime import datetime
from app.services.billing_service import get_billing_service
from app.services.wellness_service import get_wellness_service

bp = Blueprint('main', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and endpoint"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        name = data.get('name', '').strip()
        role = data.get('role', '').strip()

        # Simple validation - in production, validate against a database
        if not all([username, name, role]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        if role not in ['clinician', 'nurse', 'patient']:
            return jsonify({'success': False, 'error': 'Invalid role'}), 400

        # Set session
        session['user_id'] = username
        session['user_name'] = name
        session['user_role'] = role
        session.permanent = False

        return jsonify({
            'success': True,
            'redirect': get_dashboard_for_role(role)
        }), 200

    # GET request - show login page only if not authenticated
    if 'user_id' in session:
        return redirect(url_for('main.' + get_dashboard_endpoint_for_role(session.get('user_role', 'nurse'))))

    return render_template('login.html')


@bp.route('/logout')
def logout():
    """Logout endpoint - clears session"""
    session.clear()
    return redirect(url_for('main.login'))


def get_dashboard_for_role(role):
    """Get dashboard URL for role"""
    routes = {
        'clinician': '/clinician-dashboard',
        'nurse': '/nurse-dashboard',
        'patient': '/patient-dashboard'
    }
    return routes.get(role, '/dashboard')


def get_dashboard_endpoint_for_role(role):
    """Get dashboard endpoint name for role"""
    routes = {
        'clinician': 'clinician_dashboard',
        'nurse': 'nurse_dashboard',
        'patient': 'patient_dashboard'
    }
    return routes.get(role, 'dashboard')


@bp.route('/clinician-dashboard')
def clinician_dashboard():
    """Clinician-specific dashboard"""
    return render_template('clinician_dashboard.html')


@bp.route('/nurse-dashboard')
def nurse_dashboard():
    """Nurse dashboard - same as main dashboard"""
    return render_template('dashboard.html')


@bp.route('/patient-dashboard')
def patient_dashboard():
    """Patient dashboard - dedicated patient experience"""
    # Get patient data from session if available
    patient_id = session.get('user_id', 'P001')
    patient_name = session.get('user_name', 'Patient')

    # Get patient details from store if patient ID exists
    store = current_app.config.get('STORE')
    patient_data = {}
    if store:
        # Try to get first admitted patient for demo purposes
        admitted_patients = store.get_admitted_patients()
        if admitted_patients:
            # Use the first admitted patient for demo
            patient_data = admitted_patients[0] if isinstance(admitted_patients, list) else admitted_patients

        # If no admitted patients, create default patient data
        if not patient_data:
            patient_data = {
                'id': 1,
                'name': patient_name,
                'age': '45',
                'doctor': 'Dr. Smith',
                'doctorPhone': '+91-9999-999-999',
                'admitted': '2024-03-15',
                'sepsisRisk': 0.65,
                'vitals': {
                    'HR': 92,
                    'Temp': 37.2,
                    'SBP': 128,
                    'DBP': 82,
                    'O2Sat': 96
                }
            }

    return render_template('patient_dashboard.html',
                         patient_id=patient_data.get('id', patient_id),
                         patient_name=patient_data.get('name', patient_name),
                         patient_age=patient_data.get('age', '45'),
                         doctor_name=patient_data.get('doctor', 'Dr. Smith'),
                         doctor_phone=patient_data.get('doctorPhone', '+91-9999-999-999'),
                         admission_date=patient_data.get('admitted', '2024-03-15'),
                         sepsis_risk=patient_data.get('sepsisRisk', 0.65),
                         vitals_hr=patient_data.get('vitals', {}).get('HR', 92),
                         vitals_temp=patient_data.get('vitals', {}).get('Temp', 37.2),
                         vitals_sbp=patient_data.get('vitals', {}).get('SBP', 128),
                         vitals_dbp=patient_data.get('vitals', {}).get('DBP', 82),
                         vitals_o2=patient_data.get('vitals', {}).get('O2Sat', 96))


@bp.route('/unified-dashboard')
def unified_dashboard():
    """Unified dashboard"""
    return render_template('unified_dashboard.html')


@bp.route('/')
def home():
    """Home/landing page - redirect to login"""
    return redirect(url_for('main.login'))


@bp.route('/dashboard')
def dashboard():
    """ICU monitoring dashboard"""
    return render_template('dashboard.html')


@bp.route('/hitl-feedback')
def hitl_feedback_history():
    """HITL feedback history and review page"""
    return render_template('hitl_feedback.html')


@bp.route('/review')
def review_queue():
    """Legacy clinical review queue - for backwards compatibility"""
    return render_template('review_queue.html')


@bp.route('/review-queue')
def review_queue_alias():
    """Clinical review queue page"""
    return render_template('review_queue.html')


@bp.route('/patient-report/<int:patient_id>')
def patient_report_alias(patient_id):
    """Friendly URL for patient report page"""
    return render_template('patient_report.html', patient_id=patient_id)


@bp.route('/medical-certificate/<int:patient_id>')
def medical_certificate_alias(patient_id):
    """Friendly URL for medical certificate page"""
    return render_template('medical_certificate.html', patient_id=patient_id)


@bp.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all admitted patients"""
    try:
        store = current_app.config.get('STORE')
        if not store:
            return jsonify({'success': False, 'patients': [], 'error': 'Store not initialized'}), 200

        patients = store.get_admitted_patients()

        # Ensure patients is a list
        if not isinstance(patients, list):
            patients = list(patients) if hasattr(patients, '__iter__') else [patients] if patients else []

        return jsonify({'success': True, 'patients': patients}), 200
    except Exception as e:
        print(f"Error in get_patients: {str(e)}")
        return jsonify({'success': False, 'patients': [], 'error': str(e)}), 200


@bp.route('/api/patient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get specific patient details"""
    store = current_app.config['STORE']
    patient = store.get_patient(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    return jsonify(patient)


@bp.route('/api/patient/live/<int:patient_id>', methods=['GET'])
def get_patient_live(patient_id):
    """Get live patient data with real-time updates"""
    store = current_app.config['STORE']
    patient = store.get_patient(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Return patient data directly (will be merged into local patient object)
    return jsonify(patient)


@bp.route('/api/patient/admit', methods=['POST'])
def admit_patient():
    """Admit a new patient"""
    store = current_app.config['STORE']
    data = request.json
    patient = store.admit_patient(data)

    # Log admission
    print(f"[ADMISSION] New patient admitted:")
    print(f"  - ID: {patient['id']}")
    print(f"  - Name: {patient['name']}")
    print(f"  - Ward: {patient['ward']}")
    print(f"  - Doctor: {patient['doctor']}")

    return jsonify(patient), 201


@bp.route('/api/patient/<int:patient_id>/discharge', methods=['POST'])
def discharge_patient(patient_id):
    """Discharge a patient"""
    store = current_app.config['STORE']
    success = store.discharge_patient(patient_id)
    if success:
        return jsonify({'status': 'discharged'}), 200
    return jsonify({'error': 'Patient not found'}), 404


@bp.route('/api/patient/<int:patient_id>/predict', methods=['POST'])
def predict_sepsis(patient_id):
    """Run sepsis prediction on patient vitals/labs"""
    engine = current_app.config['ENGINE']
    store = current_app.config['STORE']
    patient = store.get_patient(patient_id)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    print(f"\n[PREDICTION REQUEST] Patient ID: {patient_id} ({patient.get('name', 'Unknown')})")
    result = engine.predict(patient)
    print(f"[PREDICTION RESULT] Score: {result['risk_score']}, Level: {result['risk_level']}")

    # Update patient risk score
    store.update_patient_risk(patient_id, result['risk_score'], result['top_features'])

    return jsonify(result)


@bp.route('/api/patient/<int:patient_id>/alert', methods=['POST'])
def send_alert(patient_id):
    """Send SMS alert to doctor"""
    engine = current_app.config['ENGINE']
    store = current_app.config['STORE']
    patient = store.get_patient(patient_id)
    
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    result = engine.send_alert(patient)
    
    # Log alert
    store.log_alert(patient_id, result['message'])
    
    return jsonify(result)


@bp.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get all sent alerts"""
    store = current_app.config['STORE']
    alerts = store.get_alerts()
    return jsonify(alerts)


@bp.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


# ============ HITL FEEDBACK ENDPOINTS ============
@bp.route('/api/hitl/submit', methods=['POST'])
def submit_hitl_feedback():
    """Submit HITL feedback for patient training"""
    store = current_app.config['STORE']
    data = request.json
    
    feedback = store.submit_hitl_feedback(
        clinician_id=data.get('clinician_id'),
        patient_id=data.get('patient_id'),
        feedback_data=data
    )
    
    # Check if we can retrain
    can_retrain = store.can_retrain()
    
    return jsonify({
        'success': True,
        'feedback': feedback,
        'can_retrain': can_retrain,
        'feedback_count': store.get_hitl_feedback_count()
    }), 201


@bp.route('/api/hitl/list', methods=['GET'])
def get_hitl_feedback():
    """Get HITL feedback list for clinician"""
    store = current_app.config['STORE']
    clinician_id = request.args.get('clinician_id')
    
    feedback_list = store.get_hitl_feedback_list(clinician_id)
    feedback_count = store.get_hitl_feedback_count(clinician_id)
    
    return jsonify({
        'success': True,
        'feedback': feedback_list,
        'count': feedback_count,
        'can_retrain': store.can_retrain()
    }), 200


@bp.route('/api/patient/<int:patient_id>/summary', methods=['GET'])
def get_patient_summary(patient_id):
    """Get patient summary for download"""
    store = current_app.config['STORE']
    summary = store.get_patient_summary(patient_id)
    
    if not summary:
        return jsonify({'error': 'Patient not found'}), 404
    
    return jsonify(summary), 200


@bp.route('/api/hitl/status', methods=['GET'])
def check_retrain_status():
    """Check if model retraining is available"""
    store = current_app.config['STORE']
    count = store.get_hitl_feedback_count()
    
    return jsonify({
        'feedback_count': count,
        'can_retrain': store.can_retrain(),
        'forms_needed': max(0, 10 - count)
    }), 200


# ============ MODEL RETRAINING ENDPOINTS ============
@bp.route('/api/retrain/trigger', methods=['POST'])
def trigger_retrain():
    """Trigger model retraining from collected feedback"""
    store = current_app.config['STORE']
    count = store.get_hitl_feedback_count()
    
    if count < 10:
        return jsonify({
            'success': False,
            'error': f'Insufficient feedback: {count}/10 required',
            'feedback_count': count
        }), 400
    
    # Log retraining  
    print(f"\n[RETRAINING TRIGGERED]")
    print(f"  - Feedback count: {count}")
    print(f"  - Timestamp: {datetime.now().isoformat()}")
    print(f"  - Source: {request.remote_addr}")
    
    return jsonify({
        'success': True,
        'message': f'Model retraining triggered with {count} feedback samples',
        'feedback_count': count,
        'retrain_status': 'started',
        'timestamp': datetime.now().isoformat()
    }), 200


@bp.route('/api/retrain/status', methods=['GET'])
def get_retrain_status():
    """Get current retraining status"""
    store = current_app.config['STORE']
    count = store.get_hitl_feedback_count()
    
    return jsonify({
        'feedback_count': count,
        'ready_to_retrain': count >= 10,
        'forms_needed': max(0, 10 - count),
        'last_retrain': None  # Can be updated to track last retraining time
    }), 200


# ============ MEDICAL REPORT & CERTIFICATE ENDPOINTS ============
@bp.route('/api/patient/<int:patient_id>/report', methods=['GET'])
def get_patient_report(patient_id):
    """Generate medical report for patient"""
    store = current_app.config['STORE']
    patient = store.get_patient(patient_id)
    
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    summary = store.get_patient_summary(patient_id)
    
    return jsonify({
        'success': True,
        'report': {
            'patient_info': summary['patient_info'],
            'current_risk': summary['current_risk'],
            'current_vitals': summary['current_vitals'],
            'current_labs': summary['current_labs'],
            'top_features': patient.get('topFeatures', []),
            'clinical_feedback': summary['clinical_feedback'],
            'feedback_count': summary['feedback_count'],
            'generated_at': datetime.now().isoformat()
        }
    }), 200


@bp.route('/api/patient/<int:patient_id>/certificate', methods=['GET'])
def get_medical_certificate(patient_id):
    """Generate medical discharge certificate for patient"""
    store = current_app.config['STORE']
    patient = store.get_patient(patient_id)
    
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    # Check if patient is discharged or ready for discharge
    return jsonify({
        'success': True,
        'certificate': {
            'patient_id': patient['id'],
            'patient_name': patient['name'],
            'age': patient['age'],
            'gender': patient['gender'],
            'ward': patient['ward'],
            'admitted_date': patient['admitted'],
            'discharge_date': datetime.now().strftime('%Y-%m-%d'),
            'final_sepsis_risk': patient.get('sepsisRisk', 'N/A'),
            'final_risk_status': patient.get('riskLevel', 'Stable'),
            'doctors_name': patient.get('doctor', 'Medical Team'),
            'hospital_name': 'Sepsis ICU Management System',
            'certificate_number': f"MED-{patient_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'generated_at': datetime.now().isoformat()
        }
    }), 200


@bp.route('/patient/report/<int:patient_id>')
def view_patient_report(patient_id):
    """HTML view for patient medical report"""
    return render_template('patient_report.html', patient_id=patient_id)


@bp.route('/patient/certificate/<int:patient_id>')
def view_medical_certificate(patient_id):
    """HTML view for medical certificate"""
    return render_template('medical_certificate.html', patient_id=patient_id)


# ============ PATIENT BILLING & FINANCIAL ENDPOINTS ============
@bp.route('/api/patient/<int:patient_id>/bills', methods=['GET'])
def get_patient_bills(patient_id):
    """Get patient bills list"""
    try:
        store = current_app.config['STORE']
        patient = store.get_patient(patient_id)

        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404

        # Calculate days admitted
        from datetime import datetime as dt
        admitted_date = dt.strptime(patient.get('admitted', '2024-03-15'), '%Y-%m-%d')
        days_admitted = (dt.now() - admitted_date).days

        billing_service = get_billing_service()
        bills = billing_service.get_patient_bills(str(patient_id), days_admitted)

        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'bills': bills
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/patient/<int:patient_id>/payment-history', methods=['GET'])
def get_patient_payment_history(patient_id):
    """Get patient payment history"""
    try:
        store = current_app.config['STORE']
        patient = store.get_patient(patient_id)

        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404

        # Calculate days admitted
        from datetime import datetime as dt
        admitted_date = dt.strptime(patient.get('admitted', '2024-03-15'), '%Y-%m-%d')
        days_admitted = (dt.now() - admitted_date).days

        billing_service = get_billing_service()
        payment_history = billing_service.get_payment_history(str(patient_id), days_admitted)
        balance = billing_service.calculate_pending_balance(str(patient_id), days_admitted)

        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'payment_history': payment_history,
            'balance': balance
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/patient/<int:patient_id>/bills/summary', methods=['GET'])
def get_patient_bills_summary(patient_id):
    """Get patient bills summary"""
    try:
        store = current_app.config['STORE']
        patient = store.get_patient(patient_id)

        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404

        # Calculate days admitted
        from datetime import datetime as dt
        admitted_date = dt.strptime(patient.get('admitted', '2024-03-15'), '%Y-%m-%d')
        days_admitted = (dt.now() - admitted_date).days

        billing_service = get_billing_service()
        balance = billing_service.calculate_pending_balance(str(patient_id), days_admitted)

        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'summary': balance
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/patient/<int:patient_id>/bills/<bill_id>/receipt-html', methods=['GET'])
def get_bill_receipt_html(patient_id, bill_id):
    """Get HTML receipt for a bill"""
    try:
        store = current_app.config['STORE']
        patient = store.get_patient(patient_id)

        if not patient:
            return jsonify({'error': 'Patient not found'}), 404

        billing_service = get_billing_service()
        # For demo purposes, create a sample receipt
        receipt_html = billing_service.generate_bill_receipt_html(
            str(patient_id),
            f"Bill {bill_id}",
            10000,
            '2024-03-26',
            patient.get('name', 'Patient')
        )

        return receipt_html, 200, {'Content-Type': 'text/html; charset=utf-8'}
    except Exception as e:
        return str(e), 500


@bp.route('/api/patient/<int:patient_id>/bills/<bill_id>/receipt-json', methods=['GET'])
def get_bill_receipt_json(patient_id, bill_id):
    """Get JSON receipt for a bill"""
    try:
        store = current_app.config['STORE']
        patient = store.get_patient(patient_id)

        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404

        billing_service = get_billing_service()
        receipt_data = billing_service.generate_bill_receipt_json(
            str(patient_id),
            f"Bill {bill_id}",
            10000,
            '2024-03-26',
            patient.get('name', 'Patient')
        )

        return jsonify({
            'success': True,
            'receipt': receipt_data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ WELLNESS & MENTAL HEALTH ENDPOINTS ============
@bp.route('/api/wellness/quotes', methods=['GET'])
def get_wellness_quote():
    """Get a random wellness quote"""
    try:
        wellness_service = get_wellness_service()
        quote = wellness_service.get_wellness_quote()

        return jsonify({
            'success': True,
            'quote': quote
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/wellness/tips', methods=['GET'])
def get_wellness_tips():
    """Get daily wellness tips"""
    try:
        wellness_service = get_wellness_service()
        tips = wellness_service.get_combined_wellness_tips(5)

        return jsonify({
            'success': True,
            'tips': tips
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/wellness/dashboard', methods=['GET'])
def get_wellness_dashboard():
    """Get complete wellness dashboard data"""
    try:
        wellness_service = get_wellness_service()
        data = wellness_service.get_wellness_dashboard_data()

        return jsonify({
            'success': True,
            'wellness': data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/wellness/coping-strategies', methods=['GET'])
def get_coping_strategies():
    """Get list of coping strategies"""
    try:
        wellness_service = get_wellness_service()
        strategies = wellness_service.get_coping_strategies()

        return jsonify({
            'success': True,
            'strategies': strategies
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ MEDICAL HISTORY ENDPOINTS ============
@bp.route('/api/patient/<int:patient_id>/medical-history-detailed', methods=['GET'])
def get_detailed_medical_history(patient_id):
    """Get detailed medical history for patient"""
    try:
        from datetime import datetime as dt
        store = current_app.config['STORE']
        patient = store.get_patient(patient_id)

        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404

        # Return patient's medical records
        medical_history = {
            'current_admission': {
                'admitted_date': patient.get('admitted', 'N/A'),
                'ward': patient.get('ward', 'N/A'),
                'doctor': patient.get('doctor', 'N/A'),
                'current_risk': patient.get('sepsisRisk', 0),
                'risk_level': patient.get('riskLevel', 'N/A'),
                'days_admitted': (dt.now() - dt.strptime(patient.get('admitted', '2024-03-15'), '%Y-%m-%d')).days
            },
            'vitals': patient.get('vitals', {}),
            'labs': patient.get('labs', {}),
            'top_features': patient.get('topFeatures', []),
            'alerts': patient.get('alerts', [])
        }

        return jsonify({
            'success': True,
            'patient_id': patient_id,
            'medical_history': medical_history
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500