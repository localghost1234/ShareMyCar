generate_header_row = lambda headers: "  |  ".join(f"{h:<15}" for h in headers)

# Helper function to calculate max column widths
def calculate_max_widths(data, headers):
    column_widths = [len(header) for header in headers]
    for row in data:
        for i, value in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(value)))
    return column_widths