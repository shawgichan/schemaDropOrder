import re
from collections import defaultdict, deque

# Regular expressions to extract table names and foreign key relationships
table_regex = re.compile(r'CREATE TABLE\s+"([^"]+)"', re.IGNORECASE)
fk_regex = re.compile(r'ALTER TABLE\s+"([^"]+)"\s+ADD CONSTRAINT\s+"[^"]+"\s+FOREIGN KEY\s+\("([^"]+)"\)\s+REFERENCES\s+"([^"]+)"', re.IGNORECASE)

def read_schema(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_tables_and_dependencies(schema):
    # Remove comments from the schema
    schema = re.sub(r'--.*', '', schema)

    # Split the schema into individual statements
    statements = re.split(r';\s*', schema)

    tables = set()
    dependencies = defaultdict(list)

    for statement in statements:
        # Check for table creation
        table_match = table_regex.search(statement)
        if table_match:
            table_name = table_match.group(1)
            tables.add(table_name)

        # Check for foreign key constraints
        for fk_match in fk_regex.findall(statement):
            source_table, _, referenced_table = fk_match
            dependencies[source_table].append(referenced_table)

    return tables, dependencies

def determine_drop_order(tables, dependencies):
    in_degree = {table: 0 for table in tables}
    for table in dependencies:
        for referenced_table in dependencies[table]:
            in_degree[referenced_table] += 1

    queue = deque([table for table in tables if in_degree[table] == 0])
    drop_order = []

    while queue:
        table = queue.popleft()
        drop_order.append(table)
        for referenced_table in dependencies[table]:
            in_degree[referenced_table] -= 1
            if in_degree[referenced_table] == 0:
                queue.append(referenced_table)

    # Handle remaining tables with circular dependencies
    for table in tables:
        if table not in drop_order:
            drop_order.append(table)

    return drop_order

def main(schema_file_path, output_file_path):
    schema = read_schema(schema_file_path)
    tables, dependencies = extract_tables_and_dependencies(schema)
    drop_order = determine_drop_order(tables, dependencies)

    with open(output_file_path, 'w') as file:
        for table in drop_order:
            file.write(f"DROP TABLE IF EXISTS \"{table}\" CASCADE;\n")

if __name__ == "__main__":
    schema_file_path = 'schema.sql'
    output_file_path = 'drop_order.sql'
    main(schema_file_path, output_file_path)
