# python-cli-tools

A collection of Python CLI tools built to develop core Python skills including file I/O, API integration, class design, regex, and testing.

## Tools

### 1. Titanic Statistics (`tools/titanic_stats.py`)
Reads the Kaggle Titanic dataset and calculates survival rates by gender and passenger class.

```python
python tools/titanic_stats.py data/Titanic-Dataset.csv
```

### 2. Weather (`tools/weather.py`)
Fetches current weather information for a given city using the Open-Meteo API.

```python
python tools/weather.py Tokyo
```

### 3. Todo List (`tools/todo.py`)
A persistent todo list that saves data to a JSON file. Supports add, list, done, and delete commands.

```python
python tools/todo.py add "Buy milk"
python tools/todo.py list
python tools/todo.py done 1
python tools/todo.py delete 1
```

### 4. Text Analyzer (`tools/text_analyzer.py`)
Analyzes a text file and outputs character/word/line counts, top word frequencies, and extracts email addresses and URLs using regex.

```python
python tools/text_analyzer.py data/sample.txt
```

### 5. Data Pipeline (`tools/data_pipeline.py`)
Reads a CSV file, cleans missing values, computes summary statistics for numeric columns, and exports results as JSON. Tested with the Kaggle House Prices dataset.

```python
python tools/data_pipeline.py data/train.csv output/result.json
```

## Setup

```python
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

## Test

```python
pytest tests/ -v
```