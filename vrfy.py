import smtplib
import argparse
import dns.resolver
import socket
import time

def get_mx_record(domain):
    """
    Fetch the MX (Mail Exchange) record for the specified domain.

    Parameters:
    - domain (str): The domain to look up the MX record for.

    Returns:
    - str: The MX record host for the domain.
    """
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(sorted(mx_records, key=lambda rec: rec.preference)[0].exchange)
        return mx_record
    except Exception as e:
        print(f"Error fetching MX record for domain {domain}: {e}")
        exit()

def try_smtp_connection(server):
    """
    Attempt to connect to the server on common SMTP ports.
    """
    ports = [587, 465, 25]
    for port in ports:
        try:
            if port == 465:
                connection = smtplib.SMTP_SSL(server, port, timeout=10)
            else:
                connection = smtplib.SMTP(server, port, timeout=10)
                if port == 587:
                    connection.starttls()
            connection.close()
            print(f"Successfully connected to {server} on port {port}")
            return port
        except (smtplib.SMTPConnectError, socket.timeout, smtplib.SMTPServerDisconnected, ConnectionRefusedError) as e:
            print(f"Failed to connect to {server} on port {port}: {e}")
            time.sleep(2)  # Wait for 2 seconds before trying the next port
            continue
    print(f"Unable to connect to {server} on any common SMTP ports. Please check the server status or your network.")
    return None

def get_smtp_server(mx_record):
    """
    Determine the SMTP server and port.
    """
    port = try_smtp_connection(mx_record)
    if port:
        return mx_record, port
    else:
        print("Failed to connect to SMTP server on common ports.")
        exit()

def verify_email(email):
    """
    Verify the given email address by checking against the domain's SMTP server.
    """
    domain = email.split('@')[1]
    mx_record = get_mx_record(domain)
    smtp_server, port = get_smtp_server(mx_record)

    try:
        if port == 465:
            server = smtplib.SMTP_SSL(smtp_server, port)
        else:
            server = smtplib.SMTP(smtp_server, port)
            if port == 587:
                server.starttls()

        server.ehlo()
        code, message = server.verify(email)
        if code == 250 or code == 252:
            print(f"Verification result: Success, code {code}, {message.decode('utf-8')}")
        else:
            print(f"Verification result: Failure, code {code}, {message.decode('utf-8')}")
        server.quit()
    except Exception as e:
        print(f"Error verifying {email} with {smtp_server}: {e}")

def main():
    """
    Main function to parse arguments and verify email.
    """
    parser = argparse.ArgumentParser(description="Verify an email address via SMTP.")
    parser.add_argument("email", help="The email address to verify.")
    args = parser.parse_args()

    verify_email(args.email)

if __name__ == "__main__":
    main()
