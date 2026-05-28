# Detect OS
UNAME := $(shell uname -s 2>/dev/null || echo Windows_NT)

# Normalize OS name to "Windows_NT" for all Windows environments
ifeq ($(findstring MINGW,$(UNAME)),MINGW)
    OS := Windows_NT
else
    OS := $(UNAME)
endif

# Common variables
PYTHONFILES = $(shell ls *.py 2>/dev/null || dir /B *.py)
PKG = app
PYTESTFLAGS = -vv --verbose --cov-config=.coveragerc --cov=$(PKG) tests/
TEST_CMD = $(PYTHON) -m pytest $(PYTESTFLAGS) && $(PYTHON) -m coverage html

# Our directories
API_DIR = app
REQ_DIR = .
VENV_DIR = .venv

# Platform-specific variables
ifeq ($(OS), Windows_NT)
    PIP = $(VENV_DIR)/Scripts/pip.exe
    PYTHON = $(VENV_DIR)/Scripts/python.exe
    RUN_ENV = set MONGO_URI=mongodb://localhost:27017 && set FLASK_APP=app &&
else
    PIP = $(VENV_DIR)/bin/pip
    PYTHON = $(VENV_DIR)/bin/python
    RUN_ENV = MONGO_URI=mongodb://localhost:27017 FLASK_APP=app
endif

PYTHON_CREATE = python

run_local_server: dev_env tests
	$(RUN_ENV) $(PYTHON) app.py

tests: pytests

dev_env:
ifeq ($(wildcard $(VENV_DIR)),)
	$(PYTHON_CREATE) -m venv $(VENV_DIR)
	$(PIP) install -r $(REQ_DIR)/requirements-dev.txt
endif

pytests: dev_env
	$(RUN_ENV) $(TEST_CMD)

clean:
	rm -rf $(VENV_DIR) .pytest_cache htmlcov .coverage
