# Leader-CMS-Mapper
Professional CMS mapper
# Leader-CMS-Mapper 🚀

A highly efficient, multi-threaded Directory Fuzzing and CMS Fingerprinting tool written in Python. Designed for penetration testers and security researchers to map web structures, discover hidden installation files, core directories, and restricted paths without cluttering the terminal.

It utilizes a thread-safe queue mechanism to handle high-speed concurrent requests and dumps clean, organized results into a local text report.

---

## 🧠 Architecture & Logic

Unlike primitive fuzzers that cause file corruption (Race Conditions) when multiple threads attempt to write to a report simultaneously, **Leader-CMS-Mapper** implements a dynamic **Thread-Safe Queue System**:
1. **Targeted Fuzzing:** Threads process paths concurrently from an input queue.
2. **Real-time Terminal Cleanliness:** Live tracking uses `\r` to overwrite `404 Not Found` statuses on a single line, keeping the terminal readable while immediately printing `200 OK` or `403 Forbidden` hits.
3. **Memory-to-Disk Dumping:** Valid hits are buffered safely in a secondary results queue in memory. Once all threads complete (`t.join()`), the data is structured and flushed into the output file in a single I/O operation.

---

## ✨ Features

- **Multi-Threaded Performance:** Spawn up to 20 attacking threads (customizable) for rapid directory scanning.
- **Dynamic 403 Detection:** Automatically identifies and highlights restricted directories (`403 Forbidden`) that indicate a folder exists but directory browsing is disabled.
- **Clean Terminal Output:** No more endless scrolling of 404 errors.
- **Automated Report Generation:** Generates a professional, structured `.txt` report containing metadata (Target URL, total hits) followed by discovered endpoints.
- **Custom User-Agent:** Evades basic signature-based blocking by mimicking a standard Linux Firefox client.

---

## 🛠️ Installation

1. **Clone the Repository:**
```bash
   git clone [https://github.com/YOUR_USERNAME/Leader-CMS-Mapper.git](https://github.com/YOUR_USERNAME/Leader-CMS-Mapper.git)
   cd Leader-CMS-Mapper


Set up a Virtual Environment (Recommended):

python3 -m venv venv
   source venv/bin/activate

Install Dependencies:
The script relies on the built-in standard libraries (threading, queue, sys) and requires requests for HTTP handling.

pip install requests

🚀 Usage
Run the script with root privileges if accessing protected system wordlists:

sudo python3 leader-cms_mapping_v2.py

Interactive Prompts:
Target Link: Enter the base URL (e.g., https://wordpress.org/showcase).

Wordlist Path: Path to your wordlist (e.g., /usr/share/seclists/Discovery/Web-Content/CMS/wordpress.fuzz.txt).

Output Report: The desired filename for your report (e.g., target_report.txt).


Sample Output Report (target_report.txt):

=== CMS Mapping Report for [https://wordpress.org/showcase](https://wordpress.org/showcase) ===
[*] Total valid paths found: 3
==================================================

[+] Found (200 OK): [https://wordpress.org/showcase/wp-config.php](https://wordpress.org/showcase/wp-config.php)
[!] Restricted (403 Forbidden): [https://wordpress.org/showcase/wp-admin/includes/](https://wordpress.org/showcase/wp-admin/includes/) -> (Target folder exists!)
[+] Found (200 OK): [https://wordpress.org/showcase/wp-cron.php](https://wordpress.org/showcase/wp-cron.php)


⚠️ Legal Disclaimer
This tool is developed strictly for educational purposes and authorized security auditing (Penetration Testing). Running this tool against targets without prior explicit written consent is illegal. The author accepts no liability and is not responsible for any misuse or damage caused by this program.

🧑‍💻 Author
Mohamed (Leader)
Cybersecurity Enthusiast & Tool Developer
