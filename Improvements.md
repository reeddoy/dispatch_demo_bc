# Improvements to Session Management and Email Sending

## What Was Changed

### 1. Session Management
- **Replaced Infinite Busy Loops with Periodic Cleanup:**
  - The original `clear_sessions` and `clear_reset_passwords` methods used infinite `while` loops that ran as fast as possible, causing high CPU usage.
  - These were replaced with `start_periodic_session_cleanup` and `start_periodic_reset_password_cleanup` methods, which run cleanup every 60 seconds using a background thread.
  - The cleanup logic was moved to `clear_sessions_once` and `clear_reset_passwords_once` methods, which are called periodically.
- **Updated Server Startup:**
  - In `lifespan`, the server now starts the periodic cleanup tasks instead of the old busy-loop thread.

### 2. Email Sending
- **Per-Email SMTP Connection:**
  - The mail sender now creates a new SMTP connection and logs in for each email sent, instead of keeping a long-lived SMTP connection open.
  - This avoids issues with stale or dropped connections in long-running server processes.
- **Background Thread for Sending:**
  - Each email is sent in a background thread, so the main request/response cycle is never blocked by slow SMTP servers or network issues.
- **Removed Persistent Mail Object:**
  - The `_Mail` class and persistent connection logic were removed. All email sending is now handled per-request in a thread.

## Impact

- **Greatly Reduced CPU Usage:**
  - The server no longer runs tight loops that consume 100% CPU. Cleanup now happens at regular intervals with minimal resource usage.
- **More Predictable and Scalable:**
  - Session and reset password cleanup are now predictable and can be tuned by changing the interval.
  - The approach is scalable and avoids spawning excessive threads.
- **No Change to Core Logic:**
  - The main session and client logic remains unchanged, so existing features and APIs are unaffected.
- **Easier Maintenance:**
  - The new structure is easier to understand and maintain, and can be further improved (e.g., by using async tasks or external stores) if needed.
- **Robust Email Delivery:**
  - Email sending is now more robust against connection issues and does not block user requests.
  - No risk of resource leaks from long-lived SMTP connections.

---

**Summary:**

Session management is now efficient, predictable, and no longer causes high CPU usage. Email sending is now robust, non-blocking, and safe for production use, while keeping the core structure and logic of the application intact.
