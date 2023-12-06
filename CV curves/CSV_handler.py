##===============================================##
##        File: CSV_handler.py
##      Author: GOTTFRID OLSSON 
##     Created: 2022-02-04
##     Updated: 2023-08-04
##       About: Useful functions for handling
##              CSV-files.
##              Useful functions:
##               - combine_CSV_files_to_one
##               - print_arrays_to_CSV
##               - print_CSV_to_LaTeX_table
##===============================================##


## LIBRARIES ##
import pandas as pd
from datetime import datetime #for metadata in print_CSV_to_LaTeX_table

## CONSTANTS ##
CSV_DELIMITER = ','


## FUNCTIONS ##
def read(CSV_file_path, skiprows=0, print_message=True):
    #print("In progress: Reading CSV" + CSV_filePath)
    CSV =  pd.read_csv(CSV_file_path, sep=CSV_DELIMITER, skiprows=skiprows)
    if print_message:
        print("DONE: Reading CSV: " + CSV_file_path)
    return CSV

# i'm not sure how to do this nicely. yet. //2022-02-04, 19:12
def write_DataFrame_to_CSV(DataFrame, write_file_path, encoding='utf-8'):
    print("In progress: Exporting DataFrame to CSV")
    DataFrame.to_csv(write_file_path, sep=CSV_DELIMITER, encoding=encoding, index=False)
    print("Done: Writing DataFrame to CSV: " + write_file_path)

def combine_list_of_lists_and_header_to_DataFrame(list_of_lists, header):
    dataframe = pd.DataFrame(list_of_lists).transpose()
    dataframe.columns = header
    return dataframe

def get_header(CSV_data):
    return CSV_data.columns.values


def combine_CSV_files_to_one(output_path, paths):
    """Takes several CSV files and appends them columnwise to a new CSV file

    INPUT:
        output_path: path to where the outputted csv should go
        
        paths: paths to CSV files in array: [csv_path_1, csv_path_2, ..., csv_path_n]

    Code modified from: https://stackoverflow.com/questions/19945296/combining-csv-files-column-wise
    """

    headers = []
    columns = []

    for path in paths:

        CSV_i = read(path, print_message=False)
        headers_i = get_header(CSV_i)

        for header in headers_i:
            headers.append(header)
            columns.append(CSV_i[header])
    
    dataframe = combine_list_of_lists_and_header_to_DataFrame(columns, headers)
    write_DataFrame_to_CSV(dataframe, output_path)
    
    print(f"Successfully appended {len(paths)} CSV files to output path: '{output_path}'")
    



def print_arrays_to_CSV(path_to_CSV_file, *args, print_message=False):
    """Prints array(s) with corresponding header(s) to a file with comma separated values (CSV)

        Input:
            path_to_csv: the path to where the CSV file should be printed

            *args: array(s) and corresponding header(s) in this format:
                    header_1, array_1, header_2, array_2, ..., header_n, array_n

            print_message: displays a message "Sucessfully printed CSV file (...)" (default False)

        Output:
            A CSV file with utf-8 formatting at path_to_csv, with the array(s) as column(s) and corresponding header(s)

            Lines larger down than the length of array(s) are printed as ',' without an empty space [Plot-Data once complained when there was an empty space]
        
        Warnings:
            ValueError: if the length of args is not even

            ValueError: if the number of array(s) is not equal to the number of header(s)
    """

    if len(args) % 2 != 0:
        raise ValueError("WARNING: the number of arrays + headers is not even. This may cause errors in printing!")
    
    arrays, headers, lines_per_array = [], [], []

    for index, arg in enumerate(args):

        if index % 2 == 0:
            headers.append(arg)
        else:
            arrays.append(arg)
            lines_per_array.append(len(arg))
      

    if len(arrays) != len(headers):
        raise ValueError("WARNING: the number of arrays does not equal the number of headers!")


    with open(path_to_CSV_file, 'w', encoding="utf-8") as CSV_file:
        
        # Print header line
        for header_number, header in enumerate(headers):
            CSV_file.write(str(header))

            # print comma separator between values (CSV) or newline at end of line
            if header_number != len(headers) - 1:
                CSV_file.write(",")
            else:
                CSV_file.write("\n")

        # Print CSV data
        for line in range(max(lines_per_array)):

            for array_number, array in enumerate(arrays):
                # print value of array at line, or if outside length of aray print nothing
                try:
                    CSV_file.write(str(array[line]))
                except:
                    CSV_file.write(str("")) 
                
                # print comma separator between values (CSV) or newline at end of line
                if array_number != len(arrays) - 1:
                    CSV_file.write(",")
                else:
                    CSV_file.write("\n")
    

    if print_message:
        print(f"Successfully printed {len(arrays)} arrays to CSV file at path: '{path_to_CSV_file}'")


def print_CSV_to_LaTeX_table(CSV_filepath, TXT_filepath, column_indices=None, row_indices=None, column_names=None, caption='Caption', table_placement='hbt!', print_message=True, include_metadata=True):
    '''
        Takes a CSV-file and prints selected columns and rows as a table, formatted for use in LaTeX, to a TXT-file.
        Note: utf-8 encoding is used, i.e. 'å', 'ä', and 'ö' will not be recognized.

        REQUIRED ARGUMENTS
        CSV_filepath:       (string) absolute path to .csv-file where values will be taken, structured as the table will be
        TXT_filepath:       (string) absolute path to .txt-file where table will be printed

        OPTIONAL ARGUMENTS
        column_indices:     (list) indices selecting columns to print (e.g. [0,1,3,5]). Note: can be in any order, e.g. [1,2,0,3] is ok
        row_indices:        (list) indices selecting rows to pring (e.g. [0,2,3]). Note: can be in any order, e.g. [5,1,3] is ok
        column_names:       (list of strings) names of columns to be printed in table (index corresponds to header in df), if 'None' the header of the CSV-file will be used (e.g. ['Col 1', 'Col 2', None, 'Col 4'])
        caption:            (string) caption of table (default: 'Caption')
        table_placement:    (string) placement of table (default: 'hbt!')
        print_message:      (bool) prints a message of what CSV-file got printed to what TXT-file (default: True)
        include_metadata:   (bool) prints metadata (date and time and settings for the CSV to table conversion) as a comment, with %, in LaTeX (default: True)
    '''
    
    # Read CSV #
    df = read(CSV_filepath)
    header = get_header(df)


    # Assign row and column indices #
    if row_indices is None:
        row_indices = [i for i in range(df.shape[0])]

    if column_indices is None:
        column_indices = [j for j in range(df.shape[1])]


    # Open and write to file #
    with open(TXT_filepath, 'w') as table:

        # Metadata #
        date_time = datetime.now()
        date_time = date_time.strftime("%Y-%m-%d %H:%M")
        CSV_filename = CSV_filepath.split("\\")[-1]
        table.write(f'% {date_time}, table created from CSV-file: {CSV_filename}, using row indices: {row_indices}, column indices: {column_indices}\n')


        # Initiate table #
        ls = 'l'*len(column_indices)
        table.write('\\begin{table}[' + table_placement + '] \n\\centering \n\\caption{' + caption + '} \n\\begin{tabular}[t]{@{}' + ls + '@{}} \n\\toprule \n')
    

        # Column names #
        for i, column_index in enumerate(column_indices):
            try:
                column_name = header[column_index]
                if column_names[i] is not None:
                    column_name = column_names[i]
            except:
                column_name = header[column_index]
            
            table.write(column_name)
            
            if column_index != column_indices[-1]:
                table.write(' & ')
                
        table.write('\\\\ \n\\midrule \n')


        # Values #
        for i, row_index in enumerate(row_indices):

            for j, column_index in enumerate(column_indices):
                value = df.loc[i,header[j]].item()
                table.write('\\num{')
                table.write(f'{value}')
                table.write('}')

                if column_index != column_indices[-1]:
                    table.write(' & ')
                else:
                    table.write(' \\\\ \\addlinespace \n')


        # Finalize table #
        table.write('\\bottomrule \n\\end{tabular} \n\\end{table}')

        if print_message:
            print(f"\nCSV-file: {CSV_filepath}\nhas successfully been printed as a LaTeX table: {TXT_filepath}\n")

# EOF #
