# Personal Finance Manager

A Python application to record, categorize, and summarize personal income and expenses, with persistent storage in SQLite.

![Python](https://img.shields.io/badge/Python-3.x-blue) ![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)

## Features
- Add, view, update, and delete income and expense records (CRUD)
- Categorize transactions (e.g. food, travel, bills)
- View financial summaries such as monthly totals and category-wise spending
- Data saved in a local SQLite database, so records persist between runs

## Tech Stack
| Area | Tools |
|------|-------|
| Language | Python |
| Database | SQLite (`sqlite3` module) |
| Interface | Command line |

## Project Structure
```
personal-finance-manager/
├── main.py            # Entry point
├── database.py        # Database connection and queries
├── finance.db         # SQLite database (created on first run)
└── README.md
```

## Database Schema
| Table | Columns |
|-------|---------|
| transactions | id, type (income/expense), category, amount, date, description |

## Getting Started

### Prerequisites
- Python 3.8 or higher

### Installation and Run
```bash
git clone https://github.com/kavishri-23/personal-finance-manager.git
cd personal-finance-manager
python3 main.py
```

## Usage
1. Run `python3 main.py`.
2. Choose an option from the menu: add a transaction, view records, update or delete, or see a summary.
3. Your data is saved automatically in `finance.db`.

## What I Learned
- Designing a relational schema and writing SQL queries from Python
- Implementing CRUD operations with the `sqlite3` module
- Organizing a Python project into separate modules

## Future Improvements
- Budget limits and alerts
- Export reports to CSV
- Charts for spending trends

## Author
**Kavishri Senguttuvan**
[GitHub](https://github.com/kavishri-23) · [LinkedIn](https://www.linkedin.com/in/kavishrisenguttuvan)
