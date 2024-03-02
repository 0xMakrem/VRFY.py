# VRFY.py | SMTP Email Verification Tool

This tool verifies email addresses by querying the domain's mail server using the Simple Mail Transfer Protocol (SMTP). It checks if the mail server acknowledges the recipient's existence without sending an actual email.

This SMTP Email Verification Tool offers a reliable method to verify email addresses by interfacing with the domain's mail server, enhancing privacy and reducing unnecessary traffic.

## Usage:
The script is invoked from the command line with the email address you wish to verify:

```bash
python vrfy.py username@domain.com
```

## How It Works

### 1. Domain Extraction
Extracts the domain from the provided email address.

### 2. MX Record Lookup
Performs a DNS query to fetch the MX (Mail Exchange) record for the domain, indicating the responsible mail server.

### 3. SMTP Server Connection
Attempts to connect to the SMTP server using common SMTP ports:

- **Port 587**: Preferred for email submission, supports STARTTLS.
- **Port 465**: Used for SMTP over SSL (SMTPS), deprecated but still used.
- **Port 25**: Standard SMTP port, used for SMTP relay and mail delivery, often restricted.

The tool tries to connect using these ports, upgrading to a secure connection when possible.

### 4. Email Verification
Once connected, it sends a `VRFY` command with the email address to verify. The server's response indicates the email's validity.

### 5. Results Interpretation
- A positive response (250 or 252 SMTP code) suggests the email is valid.
- A negative response or error implies the email is invalid or unverifiable.

## Limitations:
### SMTP Server Protections: 
Many SMTP servers implement security measures that limit or completely disable the response to VRFY commands to prevent unauthorized enumeration of email addresses. This tool respects such configurations and does not attempt to bypass these protections.
### Variable Server Responses: 
SMTP servers can be configured to respond to VRFY commands in various ways, including providing generic responses that do not indicate whether an email address is valid.

## Security and Compliance
- Does not send emails, ensuring spam regulation compliance.
- Respects server policies and includes error handling for server rejections.

## Disclaimer
This project is intended for educational purposes only and must be used with strict adherence to ethical guidelines and legal regulations. Unauthorized use of this tool to probe, scan, or test the vulnerability of any system or network without explicit permission from the owner is strictly prohibited. Users are solely responsible for ensuring that their use of the tool complies with all applicable laws and regulations.
