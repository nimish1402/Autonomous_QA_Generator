# E-Commerce Checkout System Requirements

## Overview
This document outlines the functional requirements for the e-commerce checkout system, including payment processing, discount code functionality, and order validation.

## Discount Code Feature

### Business Rules
- Valid discount codes: SAVE10, DISCOUNT20, WELCOME15, FIRST10
- SAVE10 provides $10.00 off the total order
- DISCOUNT20 provides $20.00 off the total order  
- WELCOME15 provides $15.00 off the total order
- FIRST10 provides $10.00 off the total order
- Discount codes are case-insensitive
- Only one discount code can be applied per order
- Discount is applied to the subtotal before tax calculation

### Validation Rules
- Discount code field accepts alphanumeric characters
- Maximum length: 20 characters
- Invalid codes should display error message: "Invalid discount code"
- Valid codes should display success message: "Discount applied successfully!"
- Apply button should be disabled after successful application

### Error Handling
- Empty discount code should show: "Please enter a discount code"
- Invalid discount codes should show: "Invalid discount code" 
- Network errors should show: "Unable to apply discount code. Please try again."

## Form Validation Requirements

### Required Fields
All fields marked with asterisk (*) are mandatory:
- First Name: Required, minimum 2 characters
- Last Name: Required, minimum 2 characters  
- Email Address: Required, valid email format
- Street Address: Required, minimum 5 characters
- City: Required, minimum 2 characters
- State: Required, must select from dropdown
- ZIP Code: Required, 5-digit numeric format
- Payment Method: Required selection
- Terms and Conditions: Must be checked

### Field Validation Rules
- Email: Must contain @ symbol and valid domain
- ZIP Code: Must be exactly 5 digits
- Phone: Optional field, no validation required
- Card Number: 16 digits, formatted with spaces
- CVV: 3-4 digits depending on card type
- Expiry Date: Month and year must be future date

### Error Messages
Each field should display specific error messages:
- "First name is required"
- "Last name is required" 
- "Valid email address is required"
- "Street address is required"
- "City is required"
- "State selection is required"
- "Valid ZIP code is required"
- "Payment method is required"
- "You must agree to the terms and conditions"

## Payment Processing

### Supported Payment Methods
- Credit Card (Visa, MasterCard, American Express)
- Debit Card
- PayPal

### Card Validation
- Card number must be 16 digits
- CVV must be 3-4 digits
- Expiry date must be future date
- Cardholder name is required for card payments

### Payment Security
- All card details are validated client-side first
- SSL encryption required for transmission
- No card details stored locally
- PCI compliance required

## Order Summary Calculation

### Price Components
- Subtotal: Sum of all item prices
- Shipping: $9.99 flat rate
- Tax: 8.25% of subtotal
- Discount: Applied after subtotal, before tax
- Total: Subtotal + Shipping + Tax - Discount

### Display Format
- All prices displayed with $ symbol
- Two decimal places required
- Discount shown as negative value
- Total highlighted with bold formatting