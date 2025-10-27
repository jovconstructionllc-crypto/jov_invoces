
JOV Invoices - Ready-to-deploy Flask app
======================================

This package contains a simple Flask application to create Invoices and Estimates,
and generate PDF documents with your company branding.

How to run locally (optional):
-----------------------------
1. Create a Python virtual environment and activate it.
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt
   Note: WeasyPrint may require system packages (cairo, pango) if used.
   As a fallback, install wkhtmltopdf and pdfkit.

3. Run the app:
   python app.py
4. Open http://127.0.0.1:5000 in your browser.

Deploy to Render.com (FREE) - quick guide:
------------------------------------------
1. Create a free account on https://render.com and login.
2. Create a new repository in GitHub and push the contents of this folder to that repo.
   (You can unzip the package locally and then 'git init' and push to GitHub.)
3. In Render dashboard, click "New" -> "Web Service".
   - Connect your GitHub account and choose the repo.
   - Runtime: Python 3
   - Build command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
4. Click "Create Web Service" and Render will build and deploy. Your site will be available at a Render subdomain like https://your-repo.onrender.com
5. (Optional) Add a custom domain if you later buy jovinvoices.com

Admin / first login:
--------------------
- After deployment, open the site and create an admin user via the app UI (Clients -> Create client -> then create document).
- The app does not include authentication in this simple package; for production you should add user accounts and restrict access.

If you want, I can prepare a GitHub-ready zip and instructions to push to GitHub step-by-step.
