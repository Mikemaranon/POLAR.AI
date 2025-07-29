# POLAR Node Web Server

## Overview

The POLAR Node Web Server is a comprehensive backend solution designed to provide robust web services, database management, and command-line interface capabilities. Built using Flask framework, it implements a modular architecture that separates concerns into distinct components while maintaining secure and efficient operations.

## Core Architecture

The server implementation follows a multi-threaded approach where web services and CLI operations run concurrently. The main application orchestrates these components through separate threads, ensuring smooth operation of both interfaces without interference.

### Web Server Component

The Flask-based web server handles HTTP requests, user sessions, and API endpoints. It serves both static content and dynamic responses while maintaining security through token-based authentication and role-based access control. The server implements proper error handling and logging mechanisms to ensure reliable operation and debugging capabilities.

### Database Integration

The database management system utilizes PostgreSQL, implementing connection pooling for optimal performance. The data manager module provides a comprehensive interface for database operations while maintaining security through proper query sanitization and access control. It handles table operations, query execution, and result management with proper error handling and connection lifecycle management.

## Module Details

### Data Manager (data_m)

The Data Manager module serves as the primary interface between the application and the PostgreSQL database. It implements:

- Connection pooling for efficient resource utilization
- Parameterized queries to prevent SQL injection
- Transaction management for data consistency
- Table operation utilities for metadata and content retrieval
- Role-based access control integration with database operations

### User Manager (user_m)

User management is handled through a sophisticated authentication and authorization system that provides:

- Secure password hashing and verification
- JWT-based token generation and validation
- Session management with proper timeout handling
- Role-based access control with hierarchical permissions
- User profile management and activity tracking

### CLI Manager (cli_m)

The Command Line Interface manager provides a socket-based server that:

- Processes and executes system commands securely
- Implements proper user authentication for CLI access
- Provides dynamic command loading capabilities
- Maintains audit logs of command execution
- Restricts access to administrative users only

### API Manager (api_m)

The API module exposes RESTful endpoints that enable:

- System health monitoring and status checks
- Database operations through secure endpoints
- Shell command execution with proper authorization
- Structured response formatting
- Rate limiting and request validation

## Security Implementation

Security is implemented at multiple levels:

1. Authentication Layer
   - JWT tokens with proper expiration
   - HTTP-only cookies for token storage
   - Secure password handling

2. Authorization Layer
   - Role-based access control
   - Permission verification for all operations
   - Resource access restrictions

3. Data Security
   - Input validation and sanitization
   - Query parameterization
   - Secure connection handling

## Web Interface Details

The web interface provides several key functionalities:

### Dashboard
- System status overview
- User activity monitoring
- Resource utilization metrics

### Database Viewer
- Table listing and content viewing
- Query execution interface
- Schema management tools

### Shell Terminal
- Command execution interface
- Output display
- Command history tracking

### Command Forge (not implemented yet)
- Custom command creation
- Command testing interface
- Command management tools

## Deployment and Usage

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Required Python packages (listed in requirements.txt)

### Installation

```bash
git clone <repository-url>
cd POLAR-node
pip install -r requirements.txt
```

### Configuration

1. Set up environment variables:
   - DATABASE_URL
   - SECRET_KEY
   - JWT_SECRET
   - LOG_LEVEL

2. Configure PostgreSQL database:
   - Create database
   - Initialize tables
   - Set up user roles

### Running the Server

```bash
python3 web_server/main.py
```

This command starts both the web server and CLI server components. The web interface will be accessible at `http://localhost:5000` by default.

## Maintenance and Monitoring

The server implements comprehensive logging and monitoring:

- Application logs in `/var/log/polar/`
- Database query logging
- User activity tracking
- System resource monitoring
- Error tracking and reporting

## Contributing

Please refer to the contribution guidelines for information on how to:
- Report issues
- Submit feature requests
- Create pull requests
- Follow coding standards

# POLAR Node Web Server

## Overview

The POLAR Node Web Server is a comprehensive backend solution designed to provide robust web services, database management, and command-line interface capabilities. Built using Flask framework, it implements a modular architecture that separates concerns into distinct components while maintaining secure and efficient operations.

## Core Architecture

The server implementation follows a multi-threaded approach where web services and CLI operations run concurrently. The main application orchestrates these components through separate threads, ensuring smooth operation of both interfaces without interference.

### Web Server Component

The Flask-based web server handles HTTP requests, user sessions, and API endpoints. It serves both static content and dynamic responses while maintaining security through token-based authentication and role-based access control. The server implements proper error handling and logging mechanisms to ensure reliable operation and debugging capabilities.

### Database Integration

The database management system utilizes PostgreSQL, implementing connection pooling for optimal performance. The data manager module provides a comprehensive interface for database operations while maintaining security through proper query sanitization and access control. It handles table operations, query execution, and result management with proper error handling and connection lifecycle management.

## Module Details

### Data Manager (data_m)

The Data Manager module serves as the primary interface between the application and the PostgreSQL database. It implements:

- Connection pooling for efficient resource utilization
- Parameterized queries to prevent SQL injection
- Transaction management for data consistency
- Table operation utilities for metadata and content retrieval
- Role-based access control integration with database operations

### User Manager (user_m)

User management is handled through a sophisticated authentication and authorization system that provides:

- Secure password hashing and verification
- JWT-based token generation and validation
- Session management with proper timeout handling
- Role-based access control with hierarchical permissions
- User profile management and activity tracking

### CLI Manager (cli_m)

The Command Line Interface manager provides a socket-based server that:

- Processes and executes system commands securely
- Implements proper user authentication for CLI access
- Provides dynamic command loading capabilities
- Maintains audit logs of command execution
- Restricts access to administrative users only

### API Manager (api_m)

The API module exposes RESTful endpoints that enable:

- System health monitoring and status checks
- Database operations through secure endpoints
- Shell command execution with proper authorization
- Structured response formatting
- Rate limiting and request validation

## Security Implementation

Security is implemented at multiple levels:

1. Authentication Layer
   - JWT tokens with proper expiration
   - HTTP-only cookies for token storage
   - Secure password handling

2. Authorization Layer
   - Role-based access control
   - Permission verification for all operations
   - Resource access restrictions

3. Data Security
   - Input validation and sanitization
   - Query parameterization
   - Secure connection handling

## Web Interface Details

The web interface provides several key functionalities:

### Dashboard
- System status overview
- User activity monitoring
- Resource utilization metrics

### Database Viewer
- Table listing and content viewing
- Query execution interface
- Schema management tools

### Shell Terminal
- Command execution interface
- Output display
- Command history tracking

### Command Forge
- Custom command creation
- Command testing interface
- Command management tools

## Deployment and Usage

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Required Python packages (listed in requirements.txt)

### Installation

```bash
git clone <repository-url>
cd POLAR-node
pip install -r requirements.txt
```

### Configuration

1. Set up environment variables:
   - DATABASE_URL
   - SECRET_KEY
   - JWT_SECRET
   - LOG_LEVEL

2. Configure PostgreSQL database:
   - Create database
   - Initialize tables
   - Set up user roles

### Running the Server

```bash
python3 web_server/main.py
```

This command starts both the web server and CLI server components. The web interface will be accessible at `http://localhost:5000` by default.

## Maintenance and Monitoring

The server implements comprehensive logging and monitoring:

- Application logs in `/var/log/polar/`
- Database query logging
- User activity tracking
- System resource monitoring
- Error tracking and reporting

## Contributing

Please refer to the contribution guidelines for information on how to:
- Report issues
- Submit feature requests
- Create pull requests
- Follow coding standards
