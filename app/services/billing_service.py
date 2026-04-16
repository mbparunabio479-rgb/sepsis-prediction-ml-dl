"""
Billing Service for Patient Dashboard
Handles mock billing data, bill generation, and payment tracking
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json


class BillingService:
    """Service for handling patient billing information"""

    def __init__(self):
        """Initialize billing service with mock data generators"""
        self.healthcare_charges = {
            'ICU Room Charges': {'base': 25000, 'per_day': 2500},
            'Medications & IV Fluids': {'base': 8500, 'per_day': 1200},
            'Laboratory Tests': {'base': 5200, 'items': ['Blood Culture', 'Sensitivity Test', 'WBC Count']},
            'Doctor Consultation': {'base': 3000, 'per_visit': 1500},
            'Nursing Care & Monitoring': {'base': 6000, 'per_day': 2000},
            'CT Scan & Imaging': {'base': 12000, 'type': 'procedure'},
            'Surgeon Fees': {'base': 15000, 'type': 'procedure'},
            'Ventilator Support': {'base': 8000, 'per_day': 3000},
            'Critical Care Monitoring': {'base': 4000, 'per_day': 1500},
        }

    def get_patient_bills(self, patient_id: str, days_admitted: int = 5) -> List[Dict]:
        """
        Generate mock bills for a patient

        Args:
            patient_id: Patient ID
            days_admitted: Number of days in hospital

        Returns:
            List of bills with dates, descriptions, amounts, and statuses
        """
        bills = []
        admission_date = datetime.now() - timedelta(days=days_admitted)

        bill_items = [
            {
                'date': (admission_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                'description': 'ICU Room Charges',
                'amount': 25000,
                'status': 'Paid'
            },
            {
                'date': (admission_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                'description': 'Medications & IV Fluids',
                'amount': 8500,
                'status': 'Paid'
            },
            {
                'date': (admission_date + timedelta(days=2)).strftime('%Y-%m-%d'),
                'description': 'Laboratory Tests',
                'amount': 5200,
                'status': 'Paid'
            },
            {
                'date': (admission_date + timedelta(days=2)).strftime('%Y-%m-%d'),
                'description': 'Doctor Consultation',
                'amount': 3000,
                'status': 'Paid'
            },
            {
                'date': (admission_date + timedelta(days=3)).strftime('%Y-%m-%d'),
                'description': 'Nursing Care & Monitoring',
                'amount': 6000,
                'status': 'Paid'
            },
            {
                'date': (admission_date + timedelta(days=4)).strftime('%Y-%m-%d'),
                'description': 'CT Scan & Imaging',
                'amount': 12000,
                'status': 'Pending'
            },
            {
                'date': (admission_date + timedelta(days=5)).strftime('%Y-%m-%d'),
                'description': 'Surgeon Fees',
                'amount': 15000,
                'status': 'Pending'
            }
        ]

        return bill_items

    def calculate_pending_balance(self, patient_id: str, days_admitted: int = 5) -> Dict:
        """
        Calculate total pending balance and amount paid

        Args:
            patient_id: Patient ID
            days_admitted: Number of days in hospital

        Returns:
            Dictionary with total_paid, total_pending, and total_amount
        """
        bills = self.get_patient_bills(patient_id, days_admitted)

        total_paid = sum(bill['amount'] for bill in bills if bill['status'] == 'Paid')
        total_pending = sum(bill['amount'] for bill in bills if bill['status'] == 'Pending')

        return {
            'total_paid': total_paid,
            'total_pending': total_pending,
            'total_amount': total_paid + total_pending,
            'payment_percentage': (total_paid / (total_paid + total_pending) * 100) if (total_paid + total_pending) > 0 else 0
        }

    def get_payment_history(self, patient_id: str, days_admitted: int = 5) -> List[Dict]:
        """
        Get payment history timeline

        Args:
            patient_id: Patient ID
            days_admitted: Number of days in hospital

        Returns:
            List of payment transactions
        """
        admission_date = datetime.now() - timedelta(days=days_admitted)

        history = [
            {
                'date': (admission_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                'description': 'ICU Room Charges',
                'amount': 25000,
                'method': 'Insurance Claim',
                'status': 'Successful'
            },
            {
                'date': (admission_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                'description': 'Medications & IV Fluids',
                'amount': 8500,
                'method': 'Insurance Claim',
                'status': 'Successful'
            },
            {
                'date': (admission_date + timedelta(days=2)).strftime('%Y-%m-%d'),
                'description': 'Laboratory Tests',
                'amount': 5200,
                'method': 'Insurance Claim',
                'status': 'Successful'
            },
            {
                'date': (admission_date + timedelta(days=2)).strftime('%Y-%m-%d'),
                'description': 'Doctor Consultation',
                'amount': 3000,
                'method': 'Credit Card',
                'status': 'Successful'
            },
            {
                'date': (admission_date + timedelta(days=3)).strftime('%Y-%m-%d'),
                'description': 'Nursing Care & Monitoring',
                'amount': 6000,
                'method': 'Insurance Claim',
                'status': 'Successful'
            }
        ]

        return history

    def generate_bill_receipt_html(self, patient_id: str, bill_description: str, amount: float,
                                  date: str, patient_name: str = 'Patient') -> str:
        """
        Generate HTML receipt for bill

        Args:
            patient_id: Patient ID
            bill_description: Description of the bill
            amount: Bill amount in currency
            date: Date of the bill
            patient_name: Name of the patient

        Returns:
            HTML string of the receipt
        """
        receipt_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 20px auto; }}
                .receipt {{ border: 1px solid #ddd; padding: 20px; background: #f9f9f9; }}
                .header {{ text-align: center; border-bottom: 2px solid #1E5BA8; padding-bottom: 15px; margin-bottom: 15px; }}
                .hospital-name {{ font-size: 24px; font-weight: bold; color: #1E5BA8; }}
                .receipt-info {{ font-size: 12px; color: #666; margin: 5px 0; }}
                .section {{ margin: 20px 0; }}
                .section-title {{ font-weight: bold; font-size: 14px; margin: 10px 0; border-bottom: 1px solid #ddd; }}
                .info-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }}
                .label {{ font-weight: bold; }}
                .total {{ font-size: 18px; font-weight: bold; color: #1E5BA8; padding: 15px 0; text-align: right; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; border-top: 1px solid #ddd; padding-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="receipt">
                <div class="header">
                    <div class="hospital-name">🏥 HOSPITAL CARE</div>
                    <div class="receipt-info">Receipt Date: {date}</div>
                    <div class="receipt-info">Receipt ID: RCP-{patient_id}-{date.replace('-', '')}</div>
                </div>

                <div class="section">
                    <div class="section-title">Patient Information</div>
                    <div class="info-row">
                        <span class="label">Patient Name:</span>
                        <span>{patient_name}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Patient ID:</span>
                        <span>{patient_id}</span>
                    </div>
                </div>

                <div class="section">
                    <div class="section-title">Billing Details</div>
                    <div class="info-row">
                        <span class="label">Description:</span>
                        <span>{bill_description}</span>
                    </div>
                    <div class="info-row">
                        <span class="label">Amount:</span>
                        <span>₹{amount:,.2f}</span>
                    </div>
                </div>

                <div class="total">
                    Total Amount Due: ₹{amount:,.2f}
                </div>

                <div class="footer">
                    <p><strong>Thank you for choosing our hospital</strong></p>
                    <p>For any billing inquiries, please contact our Billing Department</p>
                    <p>Contact: billing@hospital.com | Phone: +91-8888-888-888</p>
                    <p style="margin-top: 10px; font-size: 11px;">This is an automatically generated receipt. No signature required.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return receipt_html

    def generate_bill_receipt_json(self, patient_id: str, bill_description: str, amount: float,
                                  date: str, patient_name: str = 'Patient') -> Dict:
        """
        Generate bill receipt data in JSON format

        Args:
            patient_id: Patient ID
            bill_description: Description of the bill
            amount: Bill amount in currency
            date: Date of the bill
            patient_name: Name of the patient

        Returns:
            Dictionary with receipt data
        """
        return {
            'receipt_id': f'RCP-{patient_id}-{date.replace("-", "")}',
            'date': date,
            'patient': {
                'id': patient_id,
                'name': patient_name
            },
            'billing': {
                'description': bill_description,
                'amount': amount,
                'currency': 'INR'
            },
            'total': amount,
            'generated_at': datetime.now().isoformat()
        }


# Singleton instance
_billing_service = None


def get_billing_service() -> BillingService:
    """Get or create billing service instance"""
    global _billing_service
    if _billing_service is None:
        _billing_service = BillingService()
    return _billing_service
