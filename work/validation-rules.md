# Validation Rules

## Credit Card Validation

### Luhn Algorithm Check
- **Purpose:** Validate credit card number format and checksum
- **Format:** 13-19 digit numeric strings
- **Algorithm:**
  1. Starting from the rightmost digit (check digit), double every second digit
  2. If doubling results in a number > 9, subtract 9
  3. Sum all the digits
  4. Total sum must be divisible by 10

### Supported Card Types
- **Visa:** Starts with 4, length 13 or 16 digits
- **MasterCard:** Starts with 51-55 or 2221-2720, length 16 digits
- **American Express:** Starts with 34 or 37, length 15 digits
- **Discover:** Starts with 6011, 622126-622925, 644, 645, 646, 647, or 648, length 16 digits
- **Diners Club:** Starts with 300-305, 36, or 38, length 14 digits

### Validation Rules
```
Rule 1: Card number must be numeric only
Rule 2: Card number length must be 13-19 digits
Rule 3: Card number must pass Luhn algorithm check
Rule 4: Card type must match card number prefix and length
Rule 5: No leading or trailing whitespace allowed
```

---

## Expiration Date Validation

### Format Requirements
- **Format:** MM/YY (2-digit month / 2-digit year)
- **Alternative:** MM/YYYY (2-digit month / 4-digit year)

### Validation Rules
```
Rule 1: Month must be between 01 and 12
Rule 2: Year cannot be in the past
Rule 3: If current month is equal to expiration month, year must be current year or later
Rule 4: Date format must strictly match MM/YY or MM/YYYY
Rule 5: No spaces or special characters other than forward slash allowed
Rule 6: Leading zeros required (e.g., "02/25" not "2/25")
Rule 7: Expiration date is valid through the last day of the expiration month
```

### Examples
- **Valid:** 12/25, 03/27, 12/2025
- **Invalid:** 13/25 (month > 12), 00/25 (month < 01), 12/20 (if current year is 2026), 2/25 (missing leading zero)

---

## Special Characters Validation

### Allowed Characters (Standard)
- **Alphanumeric:** A-Z, a-z, 0-9
- **Whitespace:** Space, Tab, Newline (context-dependent)
- **Common Punctuation:** . , ! ? - ' "
- **Symbols:** @ # $ % & * + = / \ | ~ ^ ( )

### Disallowed Characters (High-Risk for Injection Attacks)
```
< > { } [ ] ; : ` ~ | $ ( ) ` \ " '
```

### Field-Specific Rules

#### For Name Fields (First Name, Last Name, Full Name)
```
Rule 1: Only letters (A-Z, a-z) allowed
Rule 2: Hyphens (-) and apostrophes (') allowed between letters
Rule 3: No leading or trailing hyphens or apostrophes
Rule 4: No consecutive hyphens or apostrophes
Rule 5: No special characters (@, #, $, %, etc.)
Rule 6: No digits allowed
Rule 7: Length: 2-50 characters
```

#### For Email Address
```
Rule 1: Must contain exactly one @ symbol
Rule 2: Must contain a domain with at least one dot (.)
Rule 3: Local part (before @): letters, digits, . - _
Rule 4: No consecutive dots allowed
Rule 5: Must not start or end with dot or hyphen
Rule 6: Length: 5-254 characters
Rule 7: No spaces allowed
```

#### For Shipping Address
```
Rule 1: Alphanumeric characters allowed
Rule 2: Allowed special characters: . , - # & / ( )
Rule 3: No angle brackets < > or quotes allowed
Rule 4: No single or double quotes for injection prevention
Rule 5: No backslashes or forward slashes in certain positions
Rule 6: Length: 5-100 characters
Rule 7: No leading/trailing whitespace
```

#### For Phone Number
```
Rule 1: Digits only (0-9)
Rule 2: Hyphens (-) and parentheses () allowed for formatting
Rule 3: Valid format: (XXX) XXX-XXXX, XXX-XXX-XXXX, XXXXXXXXXX
Rule 4: Length: 10-15 digits (excluding formatting characters)
Rule 5: Must start with valid country/area code
Rule 6: No spaces between digits (optional spacing after closing paren)
```

#### For Postal Code / ZIP Code
```
Rule 1: Alphanumeric characters (A-Z, 0-9)
Rule 2: Hyphens (-) allowed for formatted codes (e.g., USA ZIP+4)
Rule 3: No spaces allowed (use hyphens for formatting)
Rule 4: Length: 3-10 characters
Rule 5: Cannot start with leading zeros (context-dependent)
```

---

## Input Sanitization & Prevention

### SQL Injection Prevention
```
Rule 1: Use parameterized queries/prepared statements
Rule 2: Validate against whitelist of allowed characters
Rule 3: Escape special characters: ' " \ ; --
Rule 4: Do not concatenate user input into SQL strings
```

### XSS (Cross-Site Scripting) Prevention
```
Rule 1: HTML-encode output: < > " ' & to &lt; &gt; &quot; &#39; &amp;
Rule 2: Do not allow script tags: <script>, <iframe>, <object>
Rule 3: Sanitize event handlers: onclick, onload, etc.
Rule 4: Content Security Policy (CSP) headers recommended
```

### Command Injection Prevention
```
Rule 1: Avoid executing shell commands with user input
Rule 2: Use allowlists for command parameters
Rule 3: Use subprocess with argument lists, not shell strings
Rule 4: Disable shell interpretation of special characters
```

---

## Validation Function Pseudocode

```
function validateCreditCard(cardNumber, expirationDate, cvc) {
  // Remove spaces and hyphens
  sanitized = cardNumber.replace(/[\s-]/g, '')
  
  // Check numeric only
  if (!sanitized.match(/^\d{13,19}$/)) return false
  
  // Check Luhn algorithm
  if (!luhnCheck(sanitized)) return false
  
  // Check expiration date
  if (!validateExpiration(expirationDate)) return false
  
  // Validate CVC (3-4 digits)
  if (!cvc.match(/^\d{3,4}$/)) return false
  
  return true
}

function validateExpiration(expDate) {
  // Parse MM/YY or MM/YYYY
  match = expDate.match(/^(\d{2})\/(\d{2,4})$/)
  if (!match) return false
  
  month = parseInt(match[1])
  year = parseInt(match[2])
  
  // Validate month
  if (month < 1 || month > 12) return false
  
  // Normalize year to 4-digit format
  if (year < 100) year += 2000
  
  // Check if expiration is in the future
  currentDate = now()
  expirationDate = lastDayOfMonth(month, year)
  
  return expirationDate >= currentDate
}

function hasInvalidSpecialChars(input, allowedChars) {
  for (char in input) {
    if (!allowedChars.contains(char)) {
      return true
    }
  }
  return false
}
```

---

## Compliance Notes

- **PCI-DSS:** Never store full credit card numbers. Use tokenization.
- **GDPR:** Validate consent before collecting personal data.
- **CCPA:** Provide privacy notice for data collection.
- **Rate Limiting:** Implement rate limiting on validation endpoints to prevent brute-force attacks.
