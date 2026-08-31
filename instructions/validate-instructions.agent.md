# Validate Transaction File Instructions

**Module:** 15 - Bulk File Processing  
**Tool:** Individual Transaction File Validator  
**Script:** `tools/validate-transaction-file.py`

---

## Overview

The **Transaction File Validator** is a Python tool that validates individual transaction files against checkout system validation rules. It processes one JSON file at a time and provides detailed error reporting for payment data including credit cards, expiration dates, and special character validation.

This tool is ideal for:
- Validating transaction batches one file at a time
- Testing individual transaction files before processing
- Identifying validation errors for correction
- Ensuring compliance with checkout rules

---

## When to Use This Tool

**Use this tool when you need to:**
- Validate a single transaction file before importing
- Check payment data for compliance before processing
- Generate detailed error reports for a specific file
- Verify that a transaction file meets all validation requirements
- Test file format and content validity

**Do NOT use this tool when you need to:**
- Process multiple files in parallel (use bulk validator instead)
- Perform non-blocking validation (errors halt processing)
- Transform or convert transaction files (validator only checks format)

---

## Script Metadata

| Property | Value |
|----------|-------|
| **Filename** | `validate-transaction-file.py` |
| **Language** | Python 3.8+ |
| **Type** | Command-line utility |
| **Input** | Single JSON file path |
| **Output** | Validation report to stdout |
| **Exit Codes** | 0 (success), 1 (validation failed) |

---

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- JSON-formatted transaction files

### Files Required

```
tools/validate-transaction-file.py    # Main validator script
```

### No External Dependencies

The validator uses only Python standard library modules:
- `json` - JSON parsing
- `re` - Regular expressions
- `sys` - System arguments
- `pathlib` - File path handling
- `datetime` - Date/time validation
- `typing` - Type hints

No pip install needed!

---

## Usage

### Basic Usage

```bash
python tools/validate-transaction-file.py <transaction-file.json>
```

### Full Command Format

```
python tools/validate-transaction-file.py <file-path>
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file-path` | string | Yes | Full or relative path to the JSON transaction file to validate |

### Examples

#### Example 1: Validate a single transaction file

```bash
python tools/validate-transaction-file.py transactions.json
```

#### Example 2: Validate with full path

```bash
python tools/validate-transaction-file.py c:\Workspace\hiAI\work\test-transactions-valid.json
```

#### Example 3: Windows PowerShell

```powershell
& "C:\Program Files\Python313\python.exe" "tools\validate-transaction-file.py" "work\transactions.json"
```

---

## Input File Format

### JSON Structure

The validator accepts two formats:

#### Single Transaction Record

```json
{
  "id": "txn_001",
  "cardholder_name": "John Doe",
  "card_number": "4532015112830366",
  "expiration": "12/25",
  "cvc": "123",
  "email": "john.doe@example.com",
  "phone": "(555) 123-4567"
}
```

#### Multiple Transaction Records (Array)

```json
[
  {
    "id": "txn_001",
    "cardholder_name": "John Doe",
    "card_number": "4532015112830366",
    "expiration": "12/25",
    "cvc": "123",
    "email": "john.doe@example.com",
    "phone": "(555) 123-4567"
  },
  {
    "id": "txn_002",
    "cardholder_name": "Jane Smith",
    "card_number": "5425233010103291",
    "expiration": "03/26",
    "cvc": "456",
    "email": "jane.smith@example.com",
    "phone": "555-987-6543"
  }
]
```

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `card_number` | string | Credit card number (13-19 digits) | "4532015112830366" |
| `expiration` | string | Card expiration in MM/YY or MM/YYYY format | "12/25" |
| `cvc` | string/int | CVV security code (3-4 digits) | "123" |

### Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Transaction identifier (for error reporting) | "txn_001" |
| `cardholder_name` | string | Full name on card | "John Doe" |
| `email` | string | Cardholder email address | "john@example.com" |
| `phone` | string | Cardholder phone number | "(555) 123-4567" |

---

## Validation Rules

### Credit Card Number

```
✓ Must be 13-19 numeric digits
✓ Must pass Luhn algorithm checksum validation
✓ Spaces and hyphens are allowed (will be stripped)
✗ Cannot contain letters or special characters
```

Examples:
- Valid: `4532015112830366` (Visa)
- Valid: `5425233010103291` (MasterCard)
- Invalid: `1234567890123456` (fails Luhn check)

### Expiration Date

```
✓ Must be in MM/YY or MM/YYYY format
✓ Month must be 01-12
✓ Year cannot be in the past
✓ Year < 100 is normalized to 20xx
✗ Invalid month (13+) or past date
```

Examples:
- Valid: `12/25` (December 2025)
- Valid: `03/2026` (March 2026)
- Invalid: `13/25` (month out of range)
- Invalid: `12/20` (if current year > 2020)

### CVC/CVV Code

```
✓ Must be 3 or 4 numeric digits
✓ Can be string or integer
✗ Cannot contain letters or spaces
```

Examples:
- Valid: `123`
- Valid: `1234` (American Express has 4-digit CVC)
- Invalid: `12` (too short)

### Cardholder Name

```
✓ Letters (A-Z, a-z) only
✓ Spaces, hyphens (-), and apostrophes (') allowed
✓ Must be 2-50 characters
✗ No special characters: < > { } [ ] ; : ` ~ | $ ( ) \ " '
✗ No digits
```

Examples:
- Valid: `John Doe`
- Valid: `Mary-Jane Smith`
- Valid: `O'Connor`
- Invalid: `John123Doe` (contains digits)
- Invalid: `John<script>` (contains special characters)

### Email Address

```
✓ Must contain exactly one @ symbol
✓ Must have domain with at least one dot (.)
✓ Format: localpart@domain.tld
✓ Max 254 characters
✗ No angle brackets, quotes, or injection characters
```

Examples:
- Valid: `john.doe@example.com`
- Valid: `user+tag@domain.co.uk`
- Invalid: `john@example` (missing TLD)
- Invalid: `john@.com` (missing domain name)

### Phone Number

```
✓ Must contain 10-15 digits (with optional formatting)
✓ Can include spaces, hyphens (-), and parentheses ()
✓ Valid formats: (555) 123-4567, 555-123-4567, 5551234567
✗ No letters, special characters, or injection characters
```

Examples:
- Valid: `(555) 123-4567`
- Valid: `555-123-4567`
- Valid: `5551234567`
- Invalid: `555 123 4567` (spaces, must use hyphens/parens)

---

## Output Format

### Validation Report

The validator produces a detailed report with per-record validation results:

```
Validating: test-transactions.json
======================================================================
Found 3 record(s)

  Record: txn_001
  ────────────────────────────────────────────────────────────────
    ✓ card_number: Valid
    ✓ expiration: Valid
    ✓ cvc: Valid
    ✓ cardholder_name: Valid
    ✓ email: Valid
    ✓ phone: Valid

  Record: txn_002
  ────────────────────────────────────────────────────────────────
    ✓ card_number: Valid
    ✓ expiration: Valid
    ✓ cvc: Valid
    ✓ cardholder_name: Valid
    ✓ email: Valid
    ✓ phone: Valid

  Record: txn_003
  ────────────────────────────────────────────────────────────────
    ✗ card_number: Card number failed Luhn algorithm check (invalid checksum)
    ✗ expiration: Expiration date is in the past (01/20)
    ✓ cvc: Valid
    ✓ cardholder_name: Valid
    ✓ email: Valid
    ✓ phone: Valid

======================================================================
VALIDATION SUMMARY
======================================================================
File: test-transactions.json
Valid Records: 2
Invalid Records: 1
Success Rate: 66.7%

Errors (2):
  - card_number: Card number failed Luhn algorithm check (invalid checksum)
  - expiration: Expiration date is in the past (01/20)
======================================================================
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success - All records are valid |
| `1` | Failure - One or more records failed validation |

---

## Common Issues & Troubleshooting

### Issue: "File not found"

**Error:**
```
Error: File 'transactions.json' not found
```

**Solution:** 
- Verify the file path is correct
- Use full absolute path if relative path fails
- Check file name spelling and case sensitivity

### Issue: "JSON parsing error"

**Error:**
```
✗ JSON parsing error: Expecting value: line 1 column 1
```

**Solution:**
- Ensure file contains valid JSON
- Check for trailing commas in JSON arrays/objects
- Use online JSON validator (jsonlint.com)
- Ensure UTF-8 encoding (not ANSI/ASCII)

### Issue: "Card number failed Luhn check"

**Error:**
```
✗ card_number: Card number failed Luhn algorithm check
```

**Solution:**
- Double-check card number is typed correctly
- Verify card number length is 13-19 digits
- Use known test card numbers (see examples below)

### Issue: "Expiration date is in the past"

**Error:**
```
✗ expiration: Expiration date is in the past (12/23)
```

**Solution:**
- Use a future expiration date
- Two-digit years are normalized to 20xx (25 → 2025)
- Remember expiration is valid through the last day of the month

### Issue: "Email is not in valid format"

**Error:**
```
✗ email: Email is not in valid format
```

**Solution:**
- Ensure email has format: name@domain.tld
- Must have exactly one @ symbol
- Must have at least one dot in domain portion

---

## Test Data & Examples

### Valid Test Transaction

```json
{
  "id": "test_001",
  "cardholder_name": "John Doe",
  "card_number": "4532015112830366",
  "expiration": "12/25",
  "cvc": "123",
  "email": "john.doe@example.com",
  "phone": "(555) 123-4567"
}
```

**Expected Result:** ✓ All fields valid

### Valid Test Cards (by type)

| Card Type | Test Number | Exp | CVC |
|-----------|-------------|-----|-----|
| Visa | 4532015112830366 | 12/25 | 123 |
| MasterCard | 5425233010103291 | 03/26 | 456 |
| American Express | 378282246310005 | 06/27 | 1234 |
| Discover | 6011111111111117 | 09/25 | 789 |

### Invalid Test Transaction

```json
{
  "id": "test_invalid",
  "cardholder_name": "Bob<script>",
  "card_number": "1234567890123456",
  "expiration": "13/25",
  "cvc": "99",
  "email": "invalid@",
  "phone": "555"
}
```

**Expected Result:** ✗ Multiple validation errors

---

## Batch Processing Workflow

For processing multiple files:

**Iterative Reread Approach** (process one file at a time):

```bash
# File 1
python tools/validate-transaction-file.py batch1.json

# Check output, fix issues if needed

# File 2
python tools/validate-transaction-file.py batch2.json

# Continue...
```

**Or use bulk validator** (for processing many files automatically):

```bash
python tools/bulk-transaction-validator.py .
```

---

## Integration with Project

This validator is part of the checkout system's payment validation layer. Use it to:

1. **Pre-import validation** - Validate files before loading to database
2. **Data quality checks** - Ensure payment data meets security standards
3. **Compliance audits** - Verify PCI-DSS compliance for stored data
4. **Testing** - Validate test transaction files in CI/CD pipelines

---

## Security Considerations

⚠️ **Warning: Never log or store actual credit card numbers**

This validator:
- ✓ Validates card format (not in cleartext logs)
- ✓ Checks card validity without storing numbers
- ✓ Should run in isolated environments
- ✓ Output should not include full card numbers in production

For production use:
- Use tokenized cards, not raw numbers
- Run validator in PCI-DSS compliant environment
- Redact card numbers from logs
- Implement proper access controls

---

## Module Context

**Module 15: Bulk File Processing**
- Topic: Processing multiple files or data items in batch
- Skill: Individual file validation as part of iterative workflow
- Related tool: `bulk-transaction-validator.py` (for multi-file processing)

---

## Quick Reference

```bash
# Validate a transaction file
python tools/validate-transaction-file.py transactions.json

# View detailed output
python tools/validate-transaction-file.py -v transactions.json

# Process multiple files sequentially
for file in *.json; do
  python tools/validate-transaction-file.py "$file"
  if [ $? -ne 0 ]; then
    echo "Validation failed for $file"
  fi
done
```

---

## Related Documentation

- [Validation Rules](../work/validation-rules.md) - Comprehensive validation specification
- [Bulk Validator](./bulk-transaction-validator-instructions.md) - Bulk file processing guide
- [Project Spec](../specs/project_spec.md) - Checkout system requirements

---

**Last Updated:** 2026-08-25  
**Author:** AI-Assisted Development  
**Status:** Approved
