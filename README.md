<div align="center">

# 🚀 Django REST Framework API Project

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0%2B-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14%2B-red?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

*A comprehensive Django REST Framework implementation showcasing best practices for building modern, scalable RESTful APIs*

[Features](#-feature-breakdown) •
[Getting Started](#-getting-started) •
[Documentation](#-documentation) •
[Resources](#-resources)

</div>

---

## 📜 Table of Contents
* [🎯 Project Overview](#-project-overview)
* [🚀 Getting Started](#-getting-started)
* [👥 Team Roles and Responsibilities](#-team-roles-and-responsibilities)
* [🛠️ Technology Stack Overview](#️-technology-stack-overview)
* [💾 Database Design Overview](#-database-design-overview)
* [✨ Feature Breakdown](#-feature-breakdown)
* [🔒 API Security Overview](#-api-security-overview)
* [🔄 CI/CD Pipeline Overview](#-cicd-pipeline-overview)
* [📚 Resources](#-resources)
* [📝 License](#-license)
* [👨‍💻 Created By](#-created-by)

---

## 🎯 Project Overview

### 📖 Brief Description
This project is a comprehensive Django REST Framework (DRF) implementation designed to demonstrate best practices in building modern, scalable RESTful APIs. It provides a structured approach to API development, incorporating serialization, authentication, permissions, and automated testing. The project serves as both a learning resource and a production-ready template for building robust web APIs with Django.

DRF extends Django's capabilities to facilitate the development of RESTful APIs, providing features like data serialization, viewsets, routers, browsable API interface, and comprehensive authentication mechanisms. This project showcases how to leverage these features to create efficient, maintainable, and secure API endpoints.

### 🎯 Project Goals
* Build a scalable and maintainable RESTful API architecture using Django REST Framework
* Implement comprehensive data serialization for converting complex data structures to JSON/XML formats
* Demonstrate authentication and authorization mechanisms for secure API access
* Create reusable API endpoints with minimal boilerplate code using ViewSets and Routers
* Provide a browsable API interface for easy testing and documentation
* Implement CRUD (Create, Read, Update, Delete) operations for database models
* Showcase best practices in API design, including proper HTTP method usage and status codes
* Establish a foundation for scalable application development with proper separation of concerns

### 🔑 Key Tech Stack
* **Python 3.x** - Core programming language
* **Django** - High-level web framework for rapid development
* **Django REST Framework (DRF)** - Powerful toolkit for building Web APIs
* **SQLite/PostgreSQL** - Relational database management system
* **pip** - Python package manager

---

## 🚀 Getting Started

### 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **virtualenv** (recommended) - For creating isolated Python environments
- **Git** - For version control

### 🔧 Installation

Follow these steps to set up the project locally:

1. **Clone the repository**
   ```bash
   git clone https://github.com/MachariaP/django-drf.git
   cd django-drf
   ```

2. **Create a virtual environment**
   ```bash
   # Using venv (Python 3.3+)
   python -m venv venv
   
   # Or using virtualenv
   virtualenv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   # Create a .env file in the project root
   cp .env.example .env
   
   # Edit .env with your configuration
   # SECRET_KEY=your-secret-key-here
   # DEBUG=True
   # DATABASE_URL=sqlite:///db.sqlite3
   ```

6. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - API: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - Browsable API: http://127.0.0.1:8000/api/

### ⚡ Quick Start

Once the server is running, you can start exploring the API:

```bash
# List all API endpoints
curl http://127.0.0.1:8000/api/

# Create a new resource (example)
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{"title": "Django for Beginners", "author": "William Vincent"}'

# Retrieve a resource
curl http://127.0.0.1:8000/api/books/1/

# Update a resource
curl -X PUT http://127.0.0.1:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{"title": "Django for Professionals"}'

# Delete a resource
curl -X DELETE http://127.0.0.1:8000/api/books/1/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report

# Run specific test file
python manage.py test app_name.tests.test_models
```

### 📖 Documentation

This project includes comprehensive documentation to help you build production-ready APIs:

- **[guide.md](guide.md)** - Complete Django REST Framework API Guide (Part 1)
  - Project setup and configuration
  - Building models, serializers, and viewsets
  - Authentication and permissions
  - Testing, documentation, and deployment
  - Best practices and troubleshooting

- **[guide001.md](guide001.md)** - Advanced Django REST Framework Guide (Part 2)
  - E-commerce features (shopping cart, wishlist, orders)
  - Webhooks and event-driven architecture
  - Real-time features with Django Channels
  - Third-party integrations (Stripe, SendGrid, AWS S3)
  - Mobile app integration
  - Microservices architecture
  - GraphQL implementation
  - Advanced security features
  - Monitoring, logging, and performance optimization
  - API versioning strategies

---

## 👥 Team Roles and Responsibilities

| Role | Key Responsibility |
|------|-------------------|
| **Backend Developer** | Design and implement API endpoints, models, serializers, and business logic using Django and DRF |
| **Database Administrator** | Design database schema, optimize queries, manage migrations, and ensure data integrity |
| **DevOps Engineer** | Set up CI/CD pipelines, manage deployment infrastructure, and ensure application scalability |
| **QA Engineer** | Develop and execute test cases, perform API testing, and ensure code quality standards |
| **Frontend Developer** | Integrate with API endpoints, consume RESTful services, and build user interfaces |
| **Security Specialist** | Implement authentication mechanisms, conduct security audits, and ensure API security best practices |
| **Technical Writer** | Create comprehensive API documentation, maintain README files, and write usage guides |
| **Project Manager** | Coordinate team efforts, manage timelines, and ensure project goals are met |

---

## 🛠️ Technology Stack Overview

| Technology | Purpose in the Project |
|------------|----------------------|
| **Python** | Primary programming language providing the foundation for backend logic and API implementation |
| **Django** | Web framework providing ORM, admin interface, authentication, and URL routing capabilities |
| **Django REST Framework** | Toolkit for building RESTful APIs with serialization, viewsets, authentication, and permissions |
| **SQLite** | Default lightweight database for development and testing environments |
| **PostgreSQL** | Production-grade relational database for scalable data storage and complex queries |
| **pip** | Package manager for installing and managing Python dependencies |
| **djangorestframework** | Core DRF package providing serializers, viewsets, routers, and API views |
| **Git** | Version control system for tracking code changes and collaboration |
| **Gunicorn** | Python WSGI HTTP server for running Django applications in production |
| **nginx** | Reverse proxy server for handling HTTP requests and serving static files |
| **Docker** | Containerization platform for consistent development and deployment environments |
| **Redis** | In-memory data store for caching and session management |
| **Celery** | Distributed task queue for handling asynchronous operations |

---

## 💾 Database Design Overview

### Key Entities

* **Book** - Represents published books with title, author, and publication information
* **User** - Built-in Django user model for authentication and authorization
* **Author** - Represents book authors with biographical information
* **Category** - Categorizes books into different genres or topics
* **Review** - User-generated reviews and ratings for books
* **Order** - Tracks book orders and purchases
* **Publisher** - Represents publishing companies and their details

### Relationships

* **One-to-Many**: A single `Author` can have many `Books` (one author writes multiple books). This is implemented using a ForeignKey from Book to Author.
* **Many-to-Many**: A `Book` can belong to multiple `Categories`, and a `Category` can contain multiple `Books`. This relationship uses Django's ManyToManyField for flexible categorization.
* **One-to-Many**: A `User` can create many `Reviews`, but each `Review` belongs to one user. This ensures proper attribution of reviews while allowing users to review multiple books.

---

## ✨ Feature Breakdown

* **RESTful API Endpoints** - Provides standardized HTTP endpoints for performing CRUD operations on resources, following REST architectural principles with proper use of HTTP methods (GET, POST, PUT, PATCH, DELETE).

* **Model Serialization** - Converts complex Django model instances and querysets into JSON format for API responses, and deserializes JSON data for creating/updating model instances with built-in validation.

* **ViewSets and Routers** - Reduces boilerplate code by combining logic for multiple related views into a single ViewSet class, with automatic URL routing configuration for standard API patterns.

* **Browsable API Interface** - Offers an interactive, web-based interface for exploring API endpoints, testing requests, and viewing responses directly from a browser without additional tools.

* **Authentication Systems** - Implements multiple authentication mechanisms including token-based authentication for stateless API access and session-based authentication for browser-based clients.

* **Permission Controls** - Enforces fine-grained access control with customizable permission classes, ensuring users can only access resources they're authorized to view or modify.

* **Data Validation** - Provides comprehensive input validation through serializer fields, ensuring data integrity and returning meaningful error messages for invalid requests.

* **Filtering and Pagination** - Enables efficient data retrieval with query parameter filtering, search functionality, and paginated responses to handle large datasets.

* **API Documentation** - Auto-generates interactive API documentation with schema definitions, making it easy for developers to understand and integrate with the API.

* **Generic API Views** - Offers pre-built view classes for common patterns (ListCreateAPIView, RetrieveUpdateDestroyAPIView) to minimize code duplication and speed up development.

---

## 🔒 API Security Overview

### 🔐 Authentication
* Implements token-based authentication using Django REST Framework's TokenAuthentication, ensuring secure, stateless API access by requiring clients to include authentication tokens in request headers.
* Provides session-based authentication for browser-based clients, leveraging Django's built-in session framework for maintaining user state across requests.

### 🛡️ Authorization and Permissions
* Enforces permission controls using DRF's permission classes (IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly) to restrict access based on user roles and authentication status, preventing unauthorized access to sensitive resources.

### ✅ Input Validation and Sanitization
* Validates all incoming data through serializers with field-level and object-level validation, preventing injection attacks and ensuring data integrity by rejecting malformed or malicious input.

### ⏱️ Rate Limiting
* Protects against abuse and denial-of-service attacks by implementing throttling policies that limit the number of requests a client can make within a specified time period.

### 🔒 HTTPS/TLS Encryption
* Secures data in transit by enforcing HTTPS connections in production, protecting sensitive information like authentication credentials and personal data from interception.

### 🌐 CORS (Cross-Origin Resource Sharing)
* Configures proper CORS headers to control which domains can access the API, preventing unauthorized cross-origin requests while allowing legitimate client applications.

### 🛡️ SQL Injection Prevention
* Leverages Django's ORM parameterized queries to automatically escape user input, eliminating SQL injection vulnerabilities without requiring manual sanitization.

### 🚫 XSS Protection
* Implements proper content-type headers and escapes output data to prevent cross-site scripting attacks, especially important when the browsable API is enabled.

---

## 🔄 CI/CD Pipeline Overview

Continuous Integration and Continuous Deployment (CI/CD) is an automated software development practice that enables teams to deliver code changes more frequently and reliably. For this Django REST Framework project, CI/CD ensures that every code change is automatically tested, validated, and ready for deployment, reducing manual errors and accelerating the development cycle.

The CI/CD pipeline for this project utilizes **GitHub Actions** as the primary automation tool, triggering workflows on every push and pull request. The pipeline includes automated testing with pytest to validate functionality, code quality checks with flake8 or pylint to enforce coding standards, and security scanning to identify vulnerabilities. **Docker** containerization ensures consistent environments across development, testing, and production stages, eliminating the "works on my machine" problem.

For deployment, the pipeline automatically builds Docker images, pushes them to a container registry, and deploys to staging or production environments based on branch policies. This automated approach ensures that the Django application, along with its dependencies and configurations, is deployed consistently every time. Environment-specific configurations are managed through environment variables and secrets, keeping sensitive information secure while maintaining flexibility across different deployment targets.

---

## 📚 Resources

* [Django Documentation](https://docs.djangoproject.com/) - Official Django framework documentation
* [Django REST Framework Documentation](https://www.django-rest-framework.org/) - Comprehensive DRF documentation and guides
* [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/) - Official quickstart tutorial for building APIs with DRF
* [Creating REST APIs using Django REST API](https://www.django-rest-framework.org/tutorial/1-serialization/) - Step-by-step guide to API creation
* [Token Based Authentication in Django](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) - Implementation guide for token authentication
* [Session Based Authentication](https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication) - Guide for session-based auth
* [Django Authentication Explained (Video)](https://www.youtube.com/results?search_query=django+authentication+explained) - Video tutorials on Django authentication
* [REST API Best Practices](https://restfulapi.net/) - Guidelines for designing RESTful APIs
* [Python Type Hints](https://docs.python.org/3/library/typing.html) - Documentation for Python type annotations
* [PostgreSQL Documentation](https://www.postgresql.org/docs/) - Official PostgreSQL documentation
* [Docker Documentation](https://docs.docker.com/) - Containerization guide
* [Redis Documentation](https://redis.io/documentation) - In-memory data store guide

---

## 📝 License

This project is licensed under the **MIT License**.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 👨‍💻 Created By

**Phinehas Macharia**

<div align="center">

### 🌟 Star this repository if you find it helpful!

Made with ❤️ by Phinehas Macharia

</div>
