# Mass Email Sender

A professional, Python-based application for automating bulk email campaigns. This tool features dynamic HTML templating, automatic PDF attachment handling, sender account rotation for optimal deliverability, and persistent state management to prevent duplicate emails across sessions.

## Core Features
* **Sender Rotation:** Automatically cycles through multiple SMTP accounts to balance load and gracefully bypass authentication failures or rate limits.
* **Dynamic Templating:** Injects generated invoice numbers, formatted dates, and dynamic pricing directly into HTML email templates.
* **State Management:** Safely tracks processed contacts and removes them from the active queue. If the application crashes or loses power, it resumes exactly where it left off.
* **Automated Attachments:** Automatically locates and attaches the most recently generated PDF in the designated directory.
* **Comprehensive Logging:** Dual-stream logging records real-time terminal output and detailed `.log` files for post-campaign debugging.

## Setup & Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/mass-email-sender.git](https://github.com/yourusername/mass-email-sender.git)
   cd mass-email-sender
