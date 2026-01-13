"""
Email Incident Monitor
Automated monitoring system for Azion CDN incident notifications

Author: Diogo Alves Fragoso
Description: Monitors email inbox for incident notifications and processes status updates
"""

from email import message_from_bytes
from datetime import datetime, timedelta
from imaplib import IMAP4_SSL
from re import escape, DOTALL, findall, IGNORECASE, search


def connect_to_email(server, user, password):
    """
    Establish IMAP connection to email server
    
    Args:
        server (str): IMAP server address
        user (str): Email username
        password (str): Email password
    
    Returns:
        IMAP4_SSL: Connected mail object
    """
    mail = IMAP4_SSL(server)
    mail.login(user, password)
    mail.select('inbox')
    return mail


def search_emails(mail, days_back=10, sender='noreply@statuspage.io'):
    """
    Search for emails from specific sender within time window
    
    Args:
        mail: IMAP connection object
        days_back (int): Number of days to search back
        sender (str): Email sender to filter
    
    Returns:
        list: Email IDs matching criteria
    """
    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%d-%b-%Y')
    
    status, data = mail.search(
        None, 
        f'(SINCE "{start_date}")',
        f'(FROM "{sender}")'
    )
    
    return data[0].split()


def extract_incident_status(body):
    """
    Extract incident status from email body using regex patterns
    
    Args:
        body (str): Email body content (HTML or plain text)
    
    Returns:
        list: Matched incident status keywords
    """
    status_keywords = [
        'New incident',
        'An update has been posted',
        'Incident status: Identified',
        'Incident status: Monitoring',
        'Incident resolved'
    ]
    
    found_statuses = []
    for keyword in status_keywords:
        pattern = findall(
            r'\b{}\b'.format(escape(keyword)),
            body,
            flags=IGNORECASE
        )
        if pattern:
            found_statuses.append(keyword)
    
    return found_statuses


def process_email(mail, email_id):
    """
    Fetch and process individual email
    
    Args:
        mail: IMAP connection object
        email_id: Email ID to process
    
    Returns:
        list: Incident statuses found in email
    """
    status, data = mail.fetch(email_id, '(RFC822)')
    raw_email = data[0][1]
    
    msg = message_from_bytes(raw_email)
    statuses = []
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            
            if content_type in ['text/plain', 'text/html']:
                charset = part.get_content_charset() or 'utf-8'
                body = part.get_payload(decode=True).decode(charset, 'ignore')
                
                # Extract incident statuses
                statuses.extend(extract_incident_status(body))
                
                # Extract relevant section (between "You" and "notifications")
                pattern = search(r'You(.*?)notifications', body, DOTALL)
                if pattern:
                    relevant_content = pattern.group(1)
                    break
    
    return statuses


def main():
    """Main execution function"""
    
    # Configuration (use config file or environment variables in production)
    EMAIL_SERVER = 'imap.your-server.com'
    EMAIL_USER = 'monitoring@example.com'
    EMAIL_PASSWORD = 'your-password'  # Use secure credential management
    SENDER_FILTER = 'noreply@statuspage.io'
    TIME_WINDOW_DAYS = 10
    
    all_statuses = []
    
    try:
        # Connect to email server
        mail = connect_to_email(EMAIL_SERVER, EMAIL_USER, EMAIL_PASSWORD)
        
        # Search for relevant emails
        email_ids = search_emails(mail, TIME_WINDOW_DAYS, SENDER_FILTER)
        
        # Process each email
        for email_id in email_ids:
            statuses = process_email(mail, email_id)
            all_statuses.extend(statuses)
        
        # Close connection
        mail.close()
        mail.logout()
        
        # Output result
        if len(all_statuses) <= 0:
            print('No emails found today')
        else:
            # Get most recent status
            print(all_statuses[-1])
            
    except Exception as e:
        print(f'Error processing emails: {str(e)}')


if __name__ == "__main__":
    main()
```

4. Commit: "Add email monitoring script"

---

#### **1.2 - Criar requirements.txt:**

1. Add file → Create new file
2. Nome: `requirements.txt`
3. Conteúdo:
```
# Email Incident Monitor - Dependencies
# Uses Python standard library - no external packages required
python>=3.8
```
4. Commit: "Add requirements file"

---

#### **1.3 - Criar .gitignore:**

1. Add file → Create new file
2. Nome: `.gitignore`
3. Conteúdo:
```
# Credentials and sensitive data
config.py
*.env
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Testing
.pytest_cache/
.coverage
