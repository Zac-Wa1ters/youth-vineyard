The Youth Vineyard

Project Overview
----------------
The Youth Vineyard is a community-based youth development organization dedicated to empowering young people through education, mentorship, and meaningful life opportunities.

The Youth Vineyard is a production-ready website built with Django and Wagtail CMS. It provides a modern content-managed platform for updating pages, events, galleries, products, and site content through an administrative dashboard.

This project was deployed from an initial Heroku test environment and migrated to a full AWS production stack using Elastic Beanstalk, RDS PostgreSQL, S3 media storage, Route 53 DNS, and SSL via AWS Certificate Manager.

Tech Stack
----------
Backend:
- Python
- Django
- Wagtail CMS
- Gunicorn

Frontend:
- HTML
- CSS
- JavaScript

Database:
- PostgreSQL (AWS RDS)

Storage:
- AWS S3 (media/image uploads)

Hosting / Infrastructure:
- AWS Elastic Beanstalk
- Application Load Balancer
- Route 53 DNS
- AWS Certificate Manager (HTTPS)

Security:
- HTTPS / SSL
- AWS WAF
- Environment variables for secrets

Core Features
-------------
- Editable CMS pages through Wagtail Admin
- Event management
- Gallery pages with images/video
- Product pages
- Contact / About pages
- Responsive front-end design
- Secure production deployment
- Custom domain support

Development Setup
-----------------
1. Clone repository

git clone <repo-url>
cd <project-folder>

2. Create virtual environment

python -m venv venv

3. Activate environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

4. Install dependencies

pip install -r requirements.txt

5. Configure environment variables

SECRET_KEY=
DEBUG=True
DATABASE_URL=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

6. Run migrations

python manage.py migrate

7. Create superuser

python manage.py createsuperuser

8. Run development server

python manage.py runserver

Production Deployment
---------------------
Hosted on AWS Elastic Beanstalk.

Key production services:
- Elastic Beanstalk app hosting
- RDS PostgreSQL database
- S3 media storage
- Route 53 DNS management
- SSL certificate
- AWS WAF protection

Useful Commands
---------------
Deploy changes:

eb deploy

Check environment:

eb status

SSH into server:

eb ssh

View logs:

eb logs

Collect static:

python manage.py collectstatic --noinput

Migrate database:

python manage.py migrate

Admin Access
------------
/admin/

Wagtail admin is used for:
- Editing pages
- Publishing content
- Managing media
- Managing navigation/content

Project Highlights
------------------
- Real-world AWS production migration
- Full-stack Django/Wagtail implementation
- Cloud deployment troubleshooting
- DNS + SSL setup
- Production debugging under live conditions
- Infrastructure + software ownership

Author
------
Evalyn Fondren
Zachary Walters
