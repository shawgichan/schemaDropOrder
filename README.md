# Schema Drop Order

This script (`schemaDropOrder.py`) reads a PostgreSQL schema file (`schema.sql`), determines the order in which tables should be dropped to avoid foreign key constraints, and outputs the SQL commands to a file (`drop_order.sql`).

## Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shawgichan/schemaDropOrder.git
   cd schemaDropOrder
2. **Prepare your PostgreSQL schema file:**
   Ensure it contains valid PostgreSQL CREATE TABLE and ALTER TABLE statements with foreign key constraints.
2. **Run the script:**
   python schemaDropOrder.py
   
   This will generate the drop_order.sql file in the same directory.

## Dependencies
Ensure you have Python installed on your system. The script uses standard Python libraries (re, collections) which come pre-installed with Python.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## Contact
For any questions or support, please open an issue on the GitHub repository.