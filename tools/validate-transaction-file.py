#!/usr/bin/env python3
"""
Individual Transaction File Validator

Validates a single transaction file against checkout validation rules.
Processes one file at a time with detailed error reporting.

Author: AI-Assisted Development
Module: 15 - Bulk File Processing
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class IndividualFileValidator:
    """Validates a single transaction file."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.valid_count = 0
        self.invalid_count = 0
    
    def luhn_check(self, card_number: str) -> bool:
        """Validate credit card number using Luhn algorithm."""
        if not card_number.isdigit() or not (13 <= len(card_number) <= 19):
            return False
        
        digits = [int(d) for d in card_number]
        checksum = 0
        parity = len(digits) % 2
        
        for i, d in enumerate(digits):
            if i % 2 == parity:
                d *= 2
                if d > 9:
                    d -= 9
            checksum += d
        
        return checksum % 10 == 0
    
    def validate_card_number(self, card_number: str) -> Tuple[bool, str]:
        """Validate credit card number format and checksum."""
        if not card_number:
            return False, "Card number is required"
        
        card_number = card_number.replace(' ', '').replace('-', '')
        
        if not card_number.isdigit():
            return False, "Card number must be numeric only"
        
        if not (13 <= len(card_number) <= 19):
            return False, f"Card number length must be 13-19 digits (got {len(card_number)})"
        
        if not self.luhn_check(card_number):
            return False, "Card number failed Luhn algorithm check (invalid checksum)"
        
        return True, "Valid"
    
    def validate_expiration(self, expiry: str) -> Tuple[bool, str]:
        """Validate expiration date format and value."""
        if not expiry:
            return False, "Expiration date is required"
        
        match = re.match(r'^(\d{2})/(\d{2,4})$', expiry.strip())
        
        if not match:
            return False, "Expiration date must be MM/YY or MM/YYYY format (e.g., 12/25)"
        
        month, year = match.groups()
        month = int(month)
        year = int(year)
        
        if month < 1 or month > 12:
            return False, f"Month must be 01-12 (got {month})"
        
        # Normalize year to 4-digit format
        if year < 100:
            year += 2000
        
        # Check if expiration is in the future
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year
        
        if year < current_year or (year == current_year and month < current_month):
            return False, f"Expiration date is in the past ({month}/{year})"
        
        return True, "Valid"
    
    def validate_cvc(self, cvc: str) -> Tuple[bool, str]:
        """Validate CVC/CVV code."""
        if not cvc:
            return False, "CVC is required"
        
        cvc = str(cvc).strip()
        
        if not cvc.isdigit():
            return False, "CVC must be numeric only"
        
        if not (3 <= len(cvc) <= 4):
            return False, f"CVC must be 3-4 digits (got {len(cvc)})"
        
        return True, "Valid"
    
    def validate_name(self, field_name: str, value: str) -> Tuple[bool, str]:
        """Validate name field."""
        if not value:
            return False, f"{field_name} is required"
        
        value = value.strip()
        
        # Check for disallowed special characters
        if re.search(r'[<>{}[\];:`~|$()\\"\']', value):
            return False, f"{field_name} contains disallowed special characters"
        
        # Name can contain letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-\']+$", value):
            return False, f"{field_name} must contain only letters, spaces, hyphens, or apostrophes"
        
        if len(value) < 2:
            return False, f"{field_name} must be at least 2 characters"
        
        if len(value) > 50:
            return False, f"{field_name} must not exceed 50 characters"
        
        return True, "Valid"
    
    def validate_email(self, email: str) -> Tuple[bool, str]:
        """Validate email address."""
        if not email:
            return False, "Email is required"
        
        email = email.strip()
        
        # Check for disallowed special characters
        if re.search(r'[<>{}[\];:`~|$()\\"\']', email):
            return False, "Email contains disallowed special characters"
        
        # Basic email validation
        if not re.match(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, "Email is not in valid format (must be name@domain.com)"
        
        if len(email) > 254:
            return False, "Email must not exceed 254 characters"
        
        return True, "Valid"
    
    def validate_phone(self, phone: str) -> Tuple[bool, str]:
        """Validate phone number."""
        if not phone:
            return False, "Phone is required"
        
        phone = str(phone).strip()
        
        # Check for disallowed special characters
        if re.search(r'[<>{}[\];:`~|$\\"\']', phone):
            return False, "Phone contains disallowed special characters"
        
        # Phone can contain digits, spaces, hyphens, and parentheses
        if not re.match(r'^[\d\-\(\)\s]{10,15}$', phone):
            return False, "Phone must be 10-15 digits with optional formatting like (555) 123-4567"
        
        # Count actual digits
        digit_count = len(re.sub(r'\D', '', phone))
        if not (10 <= digit_count <= 15):
            return False, f"Phone must contain 10-15 digits (got {digit_count})"
        
        return True, "Valid"
    
    def validate_record(self, record: Dict, record_index: int) -> bool:
        """Validate a single transaction record. Returns True if valid."""
        record_id = record.get('id', f'record_{record_index}')
        record_errors = []
        
        print(f"\n  Record: {record_id}")
        print("  " + "-" * 60)
        
        # Validate card number
        if 'card_number' in record:
            valid, msg = self.validate_card_number(record['card_number'])
            if valid:
                print(f"    ✓ card_number: {msg}")
            else:
                print(f"    ✗ card_number: {msg}")
                record_errors.append(f"card_number: {msg}")
        else:
            print(f"    ✗ card_number: Card number is required")
            record_errors.append("card_number: Card number is required")
        
        # Validate expiration date
        if 'expiration' in record:
            valid, msg = self.validate_expiration(record['expiration'])
            if valid:
                print(f"    ✓ expiration: {msg}")
            else:
                print(f"    ✗ expiration: {msg}")
                record_errors.append(f"expiration: {msg}")
        else:
            print(f"    ✗ expiration: Expiration date is required")
            record_errors.append("expiration: Expiration date is required")
        
        # Validate CVC
        if 'cvc' in record:
            valid, msg = self.validate_cvc(record['cvc'])
            if valid:
                print(f"    ✓ cvc: {msg}")
            else:
                print(f"    ✗ cvc: {msg}")
                record_errors.append(f"cvc: {msg}")
        else:
            print(f"    ✗ cvc: CVC is required")
            record_errors.append("cvc: CVC is required")
        
        # Validate cardholder name
        if 'cardholder_name' in record:
            valid, msg = self.validate_name('cardholder_name', record['cardholder_name'])
            if valid:
                print(f"    ✓ cardholder_name: {msg}")
            else:
                print(f"    ✗ cardholder_name: {msg}")
                record_errors.append(f"cardholder_name: {msg}")
        
        # Validate email
        if 'email' in record:
            valid, msg = self.validate_email(record['email'])
            if valid:
                print(f"    ✓ email: {msg}")
            else:
                print(f"    ✗ email: {msg}")
                record_errors.append(f"email: {msg}")
        
        # Validate phone
        if 'phone' in record:
            valid, msg = self.validate_phone(record['phone'])
            if valid:
                print(f"    ✓ phone: {msg}")
            else:
                print(f"    ✗ phone: {msg}")
                record_errors.append(f"phone: {msg}")
        
        if record_errors:
            self.errors.extend(record_errors)
            self.invalid_count += 1
            return False
        else:
            self.valid_count += 1
            return True
    
    def validate_file(self, filepath: Path) -> bool:
        """Validate a single JSON file. Returns True if all records are valid."""
        print(f"\nValidating: {filepath.name}")
        print("=" * 70)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"✗ JSON parsing error: {str(e)}")
            self.errors.append(f"File {filepath.name}: JSON parsing error: {str(e)}")
            return False
        except Exception as e:
            print(f"✗ Error reading file: {str(e)}")
            self.errors.append(f"File {filepath.name}: Error reading file: {str(e)}")
            return False
        
        # Handle both single record and array of records
        records = data if isinstance(data, list) else [data]
        
        print(f"Found {len(records)} record(s)")
        
        all_valid = True
        for i, record in enumerate(records):
            if not self.validate_record(record, i):
                all_valid = False
        
        return all_valid
    
    def print_summary(self, filepath: Path) -> None:
        """Print validation summary."""
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print(f"File: {filepath.name}")
        print(f"Valid Records: {self.valid_count}")
        print(f"Invalid Records: {self.invalid_count}")
        
        if self.invalid_count > 0:
            total = self.valid_count + self.invalid_count
            success_rate = (self.valid_count / total * 100) if total > 0 else 0
            print(f"Success Rate: {success_rate:.1f}%")
            print(f"\nErrors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("Status: ✓ ALL RECORDS VALID")
        
        print("=" * 70 + "\n")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python bulk-transaction-validator-individual.py <file.json>")
        print("\nExample:")
        print("  python bulk-transaction-validator-individual.py transactions.json")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    
    if not filepath.exists():
        print(f"Error: File '{filepath}' not found")
        sys.exit(1)
    
    if not filepath.suffix.lower() == '.json':
        print(f"Warning: File does not have .json extension")
    
    validator = IndividualFileValidator()
    is_valid = validator.validate_file(filepath)
    validator.print_summary(filepath)
    
    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
