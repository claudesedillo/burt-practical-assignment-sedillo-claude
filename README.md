# burt-practical-assignment
Practical Assignment for Burt written in python 3.12

<<<<<<< Updated upstream
#Requirements
=======
<<<<<<< HEAD
# Requirements
=======
#Requirements
>>>>>>> c3b3dd9ecc8df42241306a60f19b108049f134d6
>>>>>>> Stashed changes
Python 3.12

# Setup / Virtual Environment

In the `burt-practical-assignment-sedillo-claude` folder, create a virtual environment:

```powershell
py -3.12 -m venv .venv
```

# Code walkthrough

The project contains only one script that reads the two JSON files and processes the data into the two CSV reports requested by the client.

As the instructions state to assume the code is production ready, the file paths are defined using BASE_DIR, DATA_DIR, and REPORTS_DIR to make the script independent from where it's executed from. The option of manually setting file paths were also considered, but was decided not to for the sake of simplicity.

The flow of the script is layout like this:

- Read the stores and transactions JSON files
- Store the stores and transactions as Python data structures
- Build a JSON lookup of stores with a store id
- Crate a directory for the CSV reports if it does not exist
- Build the transaction report using the transaction list and store lookup
- Write the transaction report to a CSV
- Build the store summary report using the transaction list and complete store list
- write the store summary report to a csv

The read_transactions() and read_stores() methods both call the base read_json() method, which reads the raw JSON files and returns the parsed data. The method also contains exception handlers for common exceptions.

After that, the build_store_lookup() builds a dictionary of stores with an ID, that way we can get a store's data by just using the ID. This will be useful when generating the transaction report.

Next, the transaction report is built using the transaction list and the store lookup. Each transaction is matched to its store using shop_id, and the required fields are added to the report. Missing or empty fields are represented as N/A where applicable. Transactions referencing an unknown store also use N/A for the store name and city.

Then, the store summary is built using the transaction list and the complete store list. Each store is initialized with zero totals, including stores without any transactions. The script then aggregates the units sold, revenue, and transaction count for each store.

The revenue is processed in the parse_revenue method. Since the values sometimes have commas or dollar symbols, they are removed using a regular expression. After that, the values are converted to a `Decimal` data type, as they are more accurate and safer to use than floating point values. Lastly, missing or invalid (ex. `null`) values are considered 0 in calculations.

Finally, the two reports are written as transaction_report.csv and store_summary.csv using Python's built-in csv module.

# How to generate reports

Make sure Python 3.12 is installed and the virtual environment is activated.

In the burt-practical-assignment-sedillo-claude folder, create a virtual environment:

```powershell
py -3.12 -m venv .venv
```

To run, simply run the following command:

```powershell
python src\run.py
```

# How to run tests

From the project root directory, run:

```powershell
python -m unittest discover -s tests -v
```

# Output file names
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
=======
>>>>>>> Stashed changes

Output Files
>>>>>>> c3b3dd9ecc8df42241306a60f19b108049f134d6

The generated reports are saved in the reports directory:

transaction_report.csv - contains the detailed transaction report
store_summary.csv - contains the aggregated sales totals for each store
