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
TEST_CMD = pytest $(PYTESTFLAGS) && coverage html;

# Our directories
API_DIR = app
REQ_DIR = .
VENV_DIR = .venv

# Platform-specific variables
ifeq ($(OS), Windows_NT)
    ACTIVATE = . $(VENV_DIR)/Scripts/activate
    PIP = $(VENV_DIR)/Scripts/pip
else
    ACTIVATE = . $(VENV_DIR)/bin/activate
    PIP = $(VENV_DIR)/bin/pip
endif

# If python is not found, use python3 to create venv
ifeq (, $(shell which python))
    PYTHON_CREATE = python3
else
    PYTHON_CREATE = python
endif

run_local_server: dev_env tests
	$(ACTIVATE) && MONGO_URI=mongodb://localhost:27017 FLASK_APP=app flask run --debug --host=0.0.0.0 --port 8000

tests: pytests

dev_env:
	if [ ! -d $(VENV_DIR) ]; then \
		$(PYTHON_CREATE) -m venv $(VENV_DIR); \
		$(PIP) install -r $(REQ_DIR)/requirements-dev.txt; \
	fi; \
	$(ACTIVATE)

pytests: dev_env
	$(ACTIVATE) && MONGO_URI=mongodb://localhost:27017 $(TEST_CMD)

clean:
	rm -rf $(VENV_DIR) .pytest_cache htmlcov .coverage
