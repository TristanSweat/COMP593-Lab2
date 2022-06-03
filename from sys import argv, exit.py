from sys import argv, exit
import os

def get_sales_csv():

    #Check whther command line parameters was provided
    if len(argv) >= 2:
        sales_csv = argv[1]

        #Check whether the CSV path is an existing file
        if os.path.isfile(sales_csv):
            return sales_csv
        else: 
            print('Error: No CSV file does not exist')
            exit('Script execution aborted')
    else:
        print('Error: No CSV file path provided')
        exit('Script execution aborted')

sales_csv = get_sales_csv()
print(sales_csv)