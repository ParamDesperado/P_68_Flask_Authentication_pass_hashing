# Flask Authentication & File Download Manager

A web application built with Flask that implements secure user authentication and protected file downloads. This project demonstrates backend security best practices including password hashing and route protection.

## Screenshots

### Home Page

*The landing page interface.*

### User Dashboard (After Login)

*The protected dashboard where users can download files.*

---

## Features

* **Secure User Registration:** Implements password hashing using `pbkdf2:sha256` with salt for enhanced security.
* **Authentication System:** Login required decorators to protect sensitive routes.
* **File Management:** Secure file serving using Flask's `send_from_directory`.
* **Tech Stack:** Python, Flask, Werkzeug Security, HTML/CSS.

## Key Code Implementation

### 1. Password Encryption
Passwords are never stored in plain text. We use `werkzeug.security` to hash passwords before storing them in the database.

# Hashing mechanism used during registration
hashed_password = generate_password_hash(
    password,
    method='pbkdf2:sha256',
    salt_length=8
)

### 2. Protected File Download
The download route is protected by the `@login_required` decorator, ensuring only authenticated users can access the file.

@app.route('/download')
@login_required
def download():
    return send_from_directory(
        directory="static/files",
        path="cheat_sheet.pdf",
        as_attachment=True
    )

## Installation & Usage

1.  **Clone the repository**
    git clone https://github.com/ParamDesperado/repository-name.git

2.  **Install dependencies**
    pip install flask werkzeug

3.  **Run the application**
    python main.py

## Author

**Param Sangani**
* GitHub: [@ParamDesperado](https://github.com/ParamDesperado)
