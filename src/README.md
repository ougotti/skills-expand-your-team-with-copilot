# Mergington High School Activities

A comprehensive web application for managing extracurricular activities at Mergington High School. This full-stack application allows teachers to manage student registrations and enables students to explore available activities with advanced filtering and search capabilities.

## Features

### For Students
- View all available extracurricular activities with detailed schedules
- Search activities by name or description
- Filter activities by day of the week (Monday through Friday)
- Filter activities by time slots (morning or afternoon)
- Browse activities by category (Sports, Arts, Academic, Community, Technology)
- View participant counts and availability

### For Teachers
- Secure login system for teacher authentication
- Register students for activities
- Remove students from activities
- Access to all student management features

### Technical Features
- Real-time filtering and search functionality
- Responsive web design that works on all devices
- MongoDB database for persistent data storage
- REST API with comprehensive endpoints
- Modal dialogs for user interactions
- Color-coded activity categories for easy navigation

## Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: MongoDB with pymongo driver
- **Frontend**: HTML, CSS, and JavaScript
- **Authentication**: Secure password hashing
- **Server**: Uvicorn ASGI server

## Prerequisites

- Python 3.7+ 
- MongoDB server (local or remote)

## Quick Start

1. **Start MongoDB** (if running locally):
   ```bash
   # On Ubuntu/Debian:
   sudo service mongod start
   
   # On macOS with Homebrew:
   brew services start mongodb-community
   
   # Or use Docker:
   docker run -d -p 27017:27017 mongo:latest
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application**:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

4. **Open your browser** to:
   - Main application: http://localhost:8000
   - API documentation: http://localhost:8000/docs

> **Note**: The application requires a MongoDB connection to function. On first startup, it will automatically create the database and populate it with sample activities and teacher accounts.

## API Endpoints

The application provides a REST API with the following main endpoints:

- `GET /activities` - Get all activities (with optional day/time filtering)
- `GET /activities/days` - Get available days with activities
- `POST /activities/{name}/signup` - Register a student (requires teacher auth)
- `POST /activities/{name}/unregister` - Remove a student (requires teacher auth)
- `POST /auth/login` - Teacher login
- `GET /auth/check-session` - Validate teacher session

## Sample Data

When you first run the application, it automatically creates sample data including:

### Activities
- **Sports**: Chess Club, Soccer Team, Basketball Team, Morning Fitness
- **Arts**: Art Club, Drama Club, Manga Maniacs  
- **Academic**: Programming Class, Math Club, Debate Team, Science Olympiad
- **Technology**: Weekend Robotics Workshop
- Various scheduling options including weekdays, evenings, and weekends

### Teacher Accounts
- **mrodriguez** / art123 (Ms. Rodriguez)
- **mchen** / chess456 (Mr. Chen)  
- **principal** / admin789 (Principal Martinez)

> **Note**: The sample data includes pre-registered students for demonstration purposes.

## Authentication

Teachers must log in to register or unregister students for activities. The system uses secure password hashing and session management to protect student data.

## Development Guide

For detailed setup and development instructions, please refer to our [Development Guide](../docs/how-to-develop.md).
