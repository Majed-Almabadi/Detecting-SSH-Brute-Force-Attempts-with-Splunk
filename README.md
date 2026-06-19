# SSH Authentication Log Analysis & Threat Hunting Using Splunk

## Project Overview
This project documents an SSH log investigation performed in a local instance of Splunk Enterprise on Ubuntu 26.04 LTS. The primary objective is to identify abnormal login behavior, detect potential brute-force activity, and construct reusable detection logic from JSON-based Zeek-style SSH logs.

## Project Metadata
- **Analyst:** Majed Almabadi
- **Date:** June 19, 2026
- **SIEM Tool:** Splunk Enterprise (Local Instance)
- **Dataset:** `ssh_logs.json` (From 30-Days SOC Challenge Beginner - Day #18)
- **Total Events Analyzed:** 2,400

## Executive Summary
| Metric | Value |
| :--- | :--- |
| Total Events | 2,400 |
| Failed Authentication Events | 1,216 |
| Successful Authentication Events | 612 |
| Top Suspicious Source IP | 10.0.0.25 |

### Main Finding
Source IP `10.0.0.25` exhibited highly suspicious, automated behavior, generating multiple failed authentication attempts with a maximum `auth_attempts` value of 8, alongside 16 successful logins.

