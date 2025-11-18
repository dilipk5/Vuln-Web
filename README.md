# 🔓 Vuln-Web - Intentionally Vulnerable Web Application

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Educational-red.svg)

> ⚠️ **WARNING: This application is INTENTIONALLY VULNERABLE and should NEVER be deployed to production or any public-facing environment!**

## 📖 About

Vuln-Web is an intentionally vulnerable web application designed for **educational purposes** to help developers, security enthusiasts, and students learn about common web security vulnerabilities and how to exploit them.

This project demonstrates all **OWASP Top 10:2025** vulnerabilities in a hands-on, practical way.

### 🎓 Learning Objectives

- Understand common web vulnerabilities
- Learn how attackers exploit security flaws
- Practice identifying vulnerabilities in code
- Master secure coding practices
- Prepare for security certifications (CEH, OSCP, eWPT)

---

## 🎯 Features

### Core Functionality
- 👤 **User Authentication** - Register, login, logout (with vulnerabilities!)
- 📝 **Blog System** - Create posts, add comments
- 🛒 **E-Commerce** - Product catalog, shopping, checkout
- 👑 **Admin Panel** - User management, database backup
- 📁 **File Upload** - Profile picture upload
- 🔌 **REST API** - JSON endpoints for data access

### Security Vulnerabilities (OWASP Top 10:2025)

| # | Vulnerability | Examples in App |
|---|---------------|-----------------|
| **A01** | Broken Access Control | IDOR on user profiles, orders; Weak admin check |
| **A02** | Security Misconfiguration | DEBUG=True, default credentials, no security headers |
| **A03** | Software Supply Chain Failures | Vulnerable dependencies (Flask 2.0.1, Jinja2 2.11.0) |
| **A04** | Cryptographic Failures | Plain text passwords, weak SECRET_KEY='dev' |
| **A05** | Injection | SQL injection in login/search, XSS in posts/comments |
| **A06** | Insecure Design | No rate limiting, price manipulation, weak validation |
| **A07** | Authentication Failures | Predictable sessions, no account lockout, weak passwords |
| **A08** | Software & Data Integrity | No code signing, insecure deserialization potential |
| **A09** | Logging & Monitoring Failures | Insufficient logging, no security alerts |
| **A10** | Mishandling Exceptional Conditions | Verbose errors, full stack traces exposed |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/vuln-web.git
cd vuln-web

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

### Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Test Users:**
- alice / password123
- bob / qwerty
- charlie / 123456
- diana / letmein

---

## 🗂️ Project Structure

```
vuln-web/
├── app/
│   ├── __init__.py          # Flask app initialization & database setup
│   ├── routes.py            # All application routes (VULNERABLE!)
│   └── templates/           # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── blog_*.html
│       ├── shop.html
│       ├── upload.html
│       └── admin/
│           ├── dashboard.html
│           └── users.html
├── static/
│   ├── css/
│   │   └── style.css       # Application styling
│   ├── uploads/            # User uploaded files (VULNERABLE!)
│   └── backup/             # Database backups (EXPOSED!)
├── config.py               # Configuration (WEAK SECRET_KEY!)
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies (OLD VERSIONS!)
└── README.md
```

---

## 📚 Blog Series

Detailed write-ups for each vulnerability:

1. **[SQL Injection Explained](#)** - How it works & how to prevent it
2. **[XSS: From Basic to Advanced](#)** - Stored, Reflected, and DOM-based XSS
3. **[IDOR Vulnerabilities](#)** - Access control failures
4. **[Session Security in Flask](#)** - Cookie signing, forging, and protection
5. **[Price Manipulation Attacks](#)** - Client-side validation failures
6. **[Command Injection 101](#)** - OS command exploitation
7. **[File Upload Security](#)** - Unrestricted file upload risks
8. **[Cryptographic Failures](#)** - Password storage and session management
9. **[API Security Best Practices](#)** - Securing REST endpoints
10. **[Complete Security Hardening Guide](#)** - Making Vuln-Web secure

> 📝 Blog posts coming soon! Each post includes:
> - Vulnerability explanation
> - Step-by-step exploitation
> - Code comparison (vulnerable vs secure)
> - Real-world impact
> - Remediation guide

---

## 🧪 Testing & Tools

### Recommended Tools

- **Burp Suite Community** - Web proxy for manual testing
- **OWASP ZAP** - Automated vulnerability scanner
- **SQLMap** - SQL injection automation
- **Nikto** - Web server scanner
- **Browser DevTools** - For client-side testing

### Running Security Scans

```bash
# SQL Injection testing
sqlmap -u "http://localhost:5000/login" --forms --batch

# XSS testing
# Use Burp Suite Intruder with XSS payloads

# Dependency scanning
pip-audit
safety check
```

---

## 📖 Educational Use

### Ideal For:

- 🎓 Cybersecurity students
- 👨‍💻 Developers learning secure coding
- 🔐 Security researchers and penetration testers
- 📚 Security training and workshops
- 🏆 CTF practice and preparation

### Learning Path:

1. **Beginner** - Start with SQL injection and XSS
2. **Intermediate** - Explore IDOR, session manipulation, file uploads
3. **Advanced** - Command injection, privilege escalation chains
4. **Expert** - Write automation scripts, create comprehensive reports

---

## ⚠️ Legal Disclaimer

**READ CAREFULLY:**

- ✅ This application is for **educational purposes only**
- ✅ Only use on systems you own or have permission to test
- ❌ **NEVER deploy to production environments**
- ❌ **NEVER use on systems without authorization**
- ❌ **NEVER store real/sensitive data**
- ❌ **DO NOT expose to the public internet**

**The authors are NOT responsible for any misuse of this application.**

Unauthorized access to computer systems is illegal under:
- Computer Fraud and Abuse Act (CFAA) in USA
- Computer Misuse Act in UK
- Similar laws in other countries

**Always obtain proper authorization before security testing!**

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-vulnerability`)
3. Commit your changes (`git commit -am 'Add new vulnerability'`)
4. Push to the branch (`git push origin feature/new-vulnerability`)
5. Open a Pull Request

### Contribution Ideas:

- Add new vulnerabilities (SSRF, XXE, etc.)
- Improve documentation
- Add more exploitation examples
- Create video tutorials
- Translate to other languages
- Add automated exploit scripts

---

## 📋 TODO / Roadmap

- [ ] Add SSRF (Server-Side Request Forgery) vulnerability
- [ ] Add XXE (XML External Entity) vulnerability
- [ ] Add CSRF (Cross-Site Request Forgery) vulnerability
- [ ] Implement Docker Compose for easy deployment
- [ ] Create video walkthrough series
- [ ] Add automated exploit scripts
- [ ] Create CTF-style challenges
- [ ] Add "secure mode" toggle to show fixes
- [ ] Implement WebSocket vulnerabilities
- [ ] Add GraphQL API with vulnerabilities

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software for educational purposes only...
```

---

## 🙏 Acknowledgments

- **OWASP Foundation** - For the OWASP Top 10 project
- **Flask Framework** - For the excellent web framework
- **Security Community** - For sharing knowledge and best practices

### Inspired By:

- [DVWA](https://github.com/digininja/DVWA) - Damn Vulnerable Web Application
- [WebGoat](https://github.com/WebGoat/WebGoat) - OWASP WebGoat
- [OWASP Juice Shop](https://github.com/juice-shop/juice-shop)
- [bWAPP](http://www.itsecgames.com/)

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/vuln-web/issues)
- **Discussions**: [Ask questions or share ideas](https://github.com/yourusername/vuln-web/discussions)
- **Blog**: [Read detailed exploitation guides](#)
- **Twitter**: [@yourusername](#)

---

## 🌟 Star History

If you find this project helpful for learning, please consider giving it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/vuln-web&type=Date)](https://star-history.com/#yourusername/vuln-web&Date)

---

## 📊 Statistics

![GitHub stars](https://img.shields.io/github/stars/yourusername/vuln-web?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/vuln-web?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/vuln-web?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/vuln-web)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/vuln-web)

---

<div align="center">

### 🎓 Learn. Practice. Secure.

**Remember: With great power comes great responsibility!**

Made with ❤️ for the security community

[⬆ Back to Top](#-vuln-web---intentionally-vulnerable-web-application)

</div>
