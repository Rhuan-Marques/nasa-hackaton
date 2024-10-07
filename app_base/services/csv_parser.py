def check_delimiter_consistency(lines, delimiter):
    counts = [line.count(delimiter) for line in lines]
    return len(set(counts)) == 1 and counts[0] > 0

def swap_commas_and_semicolons(line):
    # Escape backslashes first
    line = line.replace('\\', '\\\\')
    # Temporarily replace semicolons to avoid conflict during replacement
    line = line.replace(';', '__SEMICOLON__')
    # Replace commas with semicolons
    line = line.replace(',', ';')
    # Replace temporary semicolons with escaped semicolons
    line = line.replace('__SEMICOLON__', '\\;')
    return line

def swap_tabs_with_commas(line):
    return line.replace('\t', ',')

def swap_triple_spaces_with_commas(line):
    return line.replace('   ', ',')

def parse_to_csv(lines: list[str]) -> list[str]:
    # Check if commas are consistent
    if check_delimiter_consistency(lines, ','):
        return lines

    # Swap commas and semicolons
    swapped_lines = [swap_commas_and_semicolons(line) for line in lines]

    # Try splitting by TAB characters
    if check_delimiter_consistency(swapped_lines, '\t'):
        # Swap tabs with commas
        final_lines = [swap_tabs_with_commas(line) for line in swapped_lines]
        return final_lines

    # Try splitting by three consecutive spaces
    if check_delimiter_consistency(swapped_lines, '   '):
        # Swap triple spaces with commas
        final_lines = [swap_triple_spaces_with_commas(line) for line in swapped_lines]
        return final_lines
    # If none of the above work, print an error
    raise ValueError('Could not parse lines as CSV file')


