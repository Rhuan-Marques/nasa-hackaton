import sys
import os

def check_delimiter_consistency(lines, delimiter):
    counts = [line.count(delimiter) for line in lines]
    print(f'Delimeter for {delimiter} is consistent: {len(set(counts))}')
    return len(set(counts)) == 1  and counts[0] > 0

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

def main():

    filename = "Datasets/Dataset1/s_OSD-379.csv"

    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Check if commas are consistent
    if check_delimiter_consistency(lines, ','):
        os.makedirs('outputs\parser', exist_ok=True)
        output_path = os.path.join('outputs\parser', os.path.basename(filename))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return

    # Swap commas and semicolons
    swapped_lines = [swap_commas_and_semicolons(line) for line in lines]

    # Try splitting by TAB characters
    if check_delimiter_consistency(swapped_lines, '\t'):
        # Swap tabs with commas
        final_lines = [swap_tabs_with_commas(line) for line in swapped_lines]
        os.makedirs('outputs\parser', exist_ok=True)
        output_path = os.path.join('outputs\parser', os.path.basename(filename))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
        return

    # Try splitting by three consecutive spaces
    if check_delimiter_consistency(swapped_lines, '   '):
        # Swap triple spaces with commas
        final_lines = [swap_triple_spaces_with_commas(line) for line in swapped_lines]
        os.makedirs('outputs\parser', exist_ok=True)
        output_path = os.path.join('outputs\parser', os.path.basename(filename))
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(final_lines)
        return

    # If none of the above work, print an error
    print("Error: Unable to process the CSV file with consistent delimiters.")
    sys.exit(1)

if __name__ == "__main__":
    main()
