# File paths
SRC = amazing
INCLUDES = data

EXE = $(SRC).a_maze_ing

CONFIG = $(INCLUDES)/config.txt
OUTPUT = $(INCLUDES)/maze.txt
REQUIREMENTS = $(INCLUDES)/requirements.txt

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

TRASH = $(SRC)/__pycache__ $(VENV) .mypy_cache $(OUTPUT)


# ANSI codes
GREEN = \033[0;32m
RED = \033[0;31m
YELLOW = \033[0;33m
BOLD = \033[1m

SUCCESS = \033[1;92m
RESET = \033[0m


# Mypy flags
FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs --no-error-summary


install:
	@echo "$(BOLD)Initializing project environment:$(RESET)"

	@echo "$(YELLOW)Creating virtual environment...$(RESET)"
	@python3 -m venv $(VENV) > /dev/null 2>&1
	@echo "$(GREEN)Virtual environment setup complete$(RESET)"

	@echo "\n$(YELLOW)Installing dependencies...$(RESET)"
	@$(PIP) install -r $(REQUIREMENTS) > /dev/null 2>&1
	@echo "$(GREEN)All dependencies successfully installed$(RESET)"

	@echo "\n$(SUCCESS)Project can now be run safely!$(RESET)"

run: $(CONFIG)
	@$(PYTHON) -m $(EXE) $(CONFIG)

lint:
	@echo "$(BOLD)Verifying project source code:$(RESET)"

	@echo "$(YELLOW)Running flake8...$(RESET)"
	@$(PYTHON) -m flake8
	@echo "$(GREEN)No norm errors found$(RESET)"

	@echo "\n$(YELLOW)Running mypy...$(RESET)"
	@$(PYTHON) -m mypy . $(FLAGS)
	@echo "$(GREEN)No typing errors found$(RESET)"

	@echo "\n$(SUCCESS)Success: no errors found in source code!$(RESET)"

debug:
	@$(PYTHON) -m pdb -m $(EXE) $(CONFIG)

clean:
	@echo "$(YELLOW)Commencing cleanup operation...$(RESET)"
	@found=0; \
	for i in $(TRASH); do \
		if [ -d "$$i" ]; then \
			echo " - Removed directory $(RED)'$$i'$(RESET)"; \
			found=1; \
		elif [ -e "$$i" ]; then \
			echo " - Removed file $(RED)'$$i'$(RESET)"; \
			found=1; \
		fi; \
	done; \
	if [ $$found -eq 0 ]; then \
		echo "$(GREEN)Nothing to clean :)$(RESET)"; \
	fi
	@rm -rf $(TRASH)
	@echo "$(SUCCESS)\nCleanup complete!$(RESET)"
