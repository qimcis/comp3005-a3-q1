# Chi McIsaac, 101345751 
COMP3005 Assignment 3 – Question 1

Simple Python console app that connects to PostgreSQL, manages a `students` table.

## Prerequisites
- Python 3.10+
- PostgreSQL 13+ with an accessible role (update `config.py` with your credentials)

## Setup
1. Create and activate a virtual environment, then install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create the assignment database (default name in `config.py` is `comp3005`). 

   ```bash
   createdb comp3005
   ```
3. Run the provided SQL script to build the table and seed the starter rows:
   ```bash
   psql -d comp3005 -f db/init.sql
   ```
4. Update the values in `config.py` so they match your PostgreSQL host, port, database name, username, and password.

## Running the Demo
```bash
python app.py
```

Pass `--step` to pause between actions to go step by step
```bash
python app.py --step
```

## Video Submission
```
https://www.loom.com/share/835e0dda91384aa1b6a6c54aae3ff8fc
```
