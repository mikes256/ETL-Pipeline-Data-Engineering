# Package Dependency Instructions

Step by step instructions for managing package dependencies and ensuring there are no conflicting libraries, ultimately futureproofing this ETL project.    
Synchronisation of pips in a virtual environment.

## Warning & Security
When updating and managing library dependencies, please use a new virtual environment in the same directory to update and test before updating your projects virtual environment. This will ensure your current project venv is not effected if there are conflicts with the latest library updates.

### Dates to update package annually:
+ Q1: 1st January
+ Q2: 1st April
+ Q3: 1st July
+ Q4: 1st October

## 1. Ensure you have pip tools installed in your venv
```yml 
(venv) TERMINAL: >pip install pip-tools
```

## 2. Ensure you have the orojects top-level requirements packages installed

```yaml
(venv) TERMINAL: >pip -r requirements.txt
```
## 3. Update Python packages dependencies

```yaml
(venv) TERMINAL: >pip-compile --upgrade
```

## 4. (Optional) View a pip tree of the packages dependent on the parent Python package

```yaml
(venv) TERMINAL: >pip install pipdeptree
(venv) TERMINAL: >pipdeptree
```
## 5. Check there are no conflicting Python libraries

```yaml
(venv) TERMINAL: >pip check
```
Expected output:
    

## 6. Update requirements.txt file if necessary

```yaml
(venv) TERMINAL: >pip freeze > requirements.txt
```