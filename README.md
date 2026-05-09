# FM26 Player Analysis API

A comprehensive REST API for analyzing and tracking Football Manager 2026 (FM26) player data. This application provides endpoints to manage player information, attributes, positions, and performance metrics.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## Features

- **Player Management**: Add, list, and retrieve player records with comprehensive attributes
- **Player Attributes**: Track 40+ player statistics including technical, physical, and mental attributes
- **Position-Based Rating**: Analyze players for specific positions (Goalkeeper, Defenders, Midfielders, Forwards) with weighted attribute scoring
- **Data Import**: Import player data from RTF/delimited text files
- **Position Management**: 10 distinct player positions with customized attribute weights
- **Database Support**: MongoDB integration with mock database option for testing
- **CORS Enabled**: Full cross-origin resource sharing support for frontend integration
- **API Documentation**: Interactive Swagger UI documentation via flask-restx
- **Testing**: Comprehensive test suite with pytest and coverage reporting
- **Type Safety**: MyPy static type checking

## Technology Stack

- **Framework**: Flask 3.1.1 with Flask-RESTX for REST API and Swagger documentation
- **Database**: MongoDB with mongomock for testing
- **Data Processing**: pandas for parsing and handling player data
- **Security**: bcrypt for password hashing
- **Testing**: pytest with coverage
- **Code Quality**: flake8, mypy
- **Server**: Gunicorn for production deployment

## Prerequisites

- Python 3.8 or higher
- MongoDB (local or remote instance) - or use mock DB for development
- pip package manager

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FM26-player-analysis
```

### 2. Create Virtual Environment

#### On Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### On Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

For development environment (includes testing tools):
```bash
pip install -r requirements-dev.txt
```

## Configuration

### Environment Variables

Create a `.env` file in the project root directory with the following variables:

```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
DB_NAME=fm26_db

# Database Options
MOCK_DB=false                    # Set to 'true' to use in-memory mock database
DEBUG=true                       # Set to 'false' for production
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGO_URI` | `mongodb://localhost:27017/testdb` | MongoDB connection string |
| `DB_NAME` | `testdb` | Database name in MongoDB |
| `MOCK_DB` | `true` | Use in-memory mock database instead of MongoDB |
| `DEBUG` | `true` | Enable Flask debug mode |

## Running the Application

### Option 1: Using Flask Development Server (Local Development)

```bash
MONGO_URI=mongodb://localhost:27017 python app.py
```

The API will be available at `http://localhost:8000`

### Option 2: Using Makefile (Recommended for Development)

```bash
make run_local_server
```

This command:
1. Creates a virtual environment if it doesn't exist
2. Installs all development dependencies
3. Runs tests
4. Starts the Flask development server with MongoDB

### Option 3: Using Gunicorn (Production)

```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

- `-w 4`: Run with 4 worker processes
- `-b 0.0.0.0:8000`: Bind to all interfaces on port 8000

### Option 4: With Flask CLI

```bash
export FLASK_APP=app.py
export MONGO_URI=mongodb://localhost:27017
flask run --debug --host=0.0.0.0 --port=8000
```

## API Documentation

### Interactive API Docs

Once the application is running, visit:

- **Swagger UI**: `http://localhost:8000/`
- **ReDoc (Alternative)**: Available through Swagger UI

### Main Endpoints

#### Players API
- `GET /players/list` - List all players with attributes
- `GET /players/<name>` - Get a specific player by name
- `POST /players/import` - Import players from an RTF/delimited file
- `POST /players/analyse/<name>` - Analyze a player's suitability for a specific position/role
- `GET /players/analyse/<name>/best` - Get a player's top 5 best positions/roles

**Available Player Roles for Analysis:**
- Goalkeeper
- SweeperKeeper
- BallPlayingDef
- CenterBack
- WingBack
- DeepLyingPlaymaker
- BallWinningMid
- BoxToBox
- AdvancedPlaymaker
- ShadowStriker

**Player Attributes** (40+ tracked attributes):
acceleration, adaptability, aerial_reach, agility, aggression, ambition, anticipation, balance, bravery, command_of_area, communication, composure, concentration, corners, crossing, decisions, determination, dribbling, eccentricity, flair, finishing, first_touch, free_kick_taking, handling, heading, jumping_reach, kicking, leadership, long_shots, long_throws, marking, natural_fitness, off_the_ball, one_on_ones, pace, passing, penalty_taking, positioning, punching_tendency, reflexes, rushing_out_tendency, stamina, strength, tackling, teamwork, technique, throwing, vision, work_rate

### Example Requests

#### List All Players
```bash
curl http://localhost:8000/players/list
```

#### Get a Specific Player
```bash
curl http://localhost:8000/players/John%20Doe
```

#### Import Players from File
```bash
curl -X POST http://localhost:8000/players/import \
  -H "Content-Type: application/json" \
  -d '{"players.rtf": "/path/to/players_data.rtf"}'
```

#### Analyze Player Suitability for a Position
```bash
curl -X POST http://localhost:8000/players/analyse/John%20Doe \
  -H "Content-Type: application/json" \
  -d '{"role": "Striker"}'
```

Response returns a rating score (0-20) indicating the player's suitability for that position.

#### Get Player's Best 5 Roles
```bash
curl http://localhost:8000/players/analyse/John%20Doe/best
```

Response returns the player's top 5 positions/roles with their ratings.

## Project Structure

```
FM26-player-analysis/
├── app.py                      # Application entry point
├── makefile                    # Build and task automation
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── .env                        # Environment variables (local)
├── README.md                   # This file
├── app/
│   ├── __init__.py            # Flask app factory and configuration
│   ├── config.py              # Configuration classes (Config, ProductionConfig, TestingConfig)
│   ├── apis/
│   │   ├── __init__.py
│   │   ├── parser.py          # Data parser for importing player data
│   │   ├── players.py         # Players API namespace and endpoints
│   │   └── positions.py       # Positions API and player attributes
│   └── db/
│       ├── __init__.py        # Database initialization
│       ├── constants.py       # Database constants
│       ├── models.py          # Data models
│       ├── player.py          # Player database operations
│       └── utils.py           # Database utility functions
├── tests/
│   ├── __init__.py
│   ├── utils.py               # Test utilities and fixtures
│   └── unit/
│       └── test_player        # Player API tests
├── docs/                       # Documentation
├── htmlcov/                    # HTML coverage reports
├── frontend/                   # Frontend application (if applicable)
└── reports/                    # Test reports
```

## Testing

### Running All Tests

```bash
make pytests
```

Or using pytest directly:

```bash
pytest -vv --cov=app tests/
```

### Test Coverage

Generate HTML coverage report:

```bash
pytest -vv --cov=app --cov-report=html tests/
```

Coverage report will be available in `htmlcov/index.html`

### Running Specific Tests

```bash
# Run a single test file
pytest tests/unit/test_player.py -v

# Run tests matching a pattern
pytest -k "test_create" -v
```

### Type Checking

```bash
mypy app/
```

### Code Quality

```bash
flake8 app/
```

## Development

### Setting Up Development Environment

1. Follow the [Installation](#installation) steps
2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Create `.env` file with development settings:
   ```env
   MONGO_URI=mongodb://localhost:27017
   DB_NAME=fm26_dev
   MOCK_DB=true
   DEBUG=true
   ```

### Code Style Guidelines

- Follow PEP 8 coding standards
- Use type hints for all functions
- Add docstrings to classes and functions
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Common Development Tasks

```bash
# Run the application
make run_local_server

# Run tests with coverage
pytest -vv --cov=app --cov-report=html tests/

# Type checking
mypy app/

# Code linting
flake8 app/
```

### Database Setup for Development

#### Using Mock Database (Recommended for Quick Development)
```env
MOCK_DB=true
```

#### Using Local MongoDB

1. Install MongoDB:
   - **macOS**: `brew install mongodb-community`
   - **Windows**: Download from [mongodb.com](https://www.mongodb.com/try/download/community)
   - **Linux**: `sudo apt-get install mongodb`

2. Start MongoDB:
   ```bash
   mongod
   ```

3. Update `.env`:
   ```env
   MONGO_URI=mongodb://localhost:27017
   MOCK_DB=false
   ```

## Troubleshooting

### Common Issues and Solutions

#### MongoDB Connection Error

**Error**: `Failed to connect to MongoDB`

**Solution**:
1. Check if MongoDB is running
2. Verify `MONGO_URI` in `.env` is correct
3. Use `MOCK_DB=true` for development without MongoDB

#### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
# macOS/Linux:
lsof -i :8000

# Windows:
netstat -ano | findstr :8000

# Kill the process (use PID from above)
# macOS/Linux:
kill -9 <PID>

# Windows:
taskkill /PID <PID> /F
```

#### Virtual Environment Issues

**Error**: `Command not found: python` or pip errors

**Solution**:
1. Ensure virtual environment is activated
2. Try using `python3` instead of `python`
3. Recreate virtual environment:
   ```bash
   rm -rf .venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

#### Import Errors

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
1. Activate virtual environment
2. Reinstall dependencies: `pip install -r requirements.txt`

#### Environment Variables Not Loading

**Issue**: `.env` file not being read

**Solution**:
1. Ensure `.env` is in the project root directory
2. Restart the application
3. Check that `python-dotenv` is installed: `pip install python-dotenv`

### Getting Help

- Check the [API Documentation](#api-documentation) for endpoint details
- Review test files in `tests/` for usage examples
- Check Flask and Flask-RESTX documentation
- Report issues with detailed error messages and stack traces

## Production Deployment

### Pre-deployment Checklist

1. Set `DEBUG=false` in environment variables
2. Set `MOCK_DB=false` and configure real MongoDB
3. Update `FLASK_ENV=production`
4. Use a production-grade WSGI server (Gunicorn, uWSGI)
5. Configure proper logging
6. Set up environment-specific configuration

### Example Production Command

```bash
gunicorn -w 4 -b 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  "app:create_app()"
```

## License

[Add your license here]

## Support and Contact

[Add contact information or support details]