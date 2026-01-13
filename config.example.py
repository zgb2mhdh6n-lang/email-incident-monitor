"""
Configuration template for Email Incident Monitor
Copy this file to config.py and fill in your credentials
"""

# Email Server Configuration
EMAIL_SERVER = 'imap.your-server.com'
EMAIL_USER = 'your-email@domain.com'
EMAIL_PASSWORD = 'your-secure-password'

# Monitoring Configuration
SENDER_FILTER = 'noreply@statuspage.io'
TIME_WINDOW_DAYS = 10

# Zabbix Configuration (if integrating)
ZABBIX_SERVER = 'your-zabbix-server.com'
ZABBIX_PORT = 10051
