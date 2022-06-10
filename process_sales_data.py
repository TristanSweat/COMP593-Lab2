from sys import argv, exit
import os
from datetime import date

def get_sales_csv():

    #Check whether command line parameters was provided
    if len(argv) >= 2:
        sales_data_csv = argv[1]

        #Check whether the CSV path is an existing file
        if os.path.isfile(sales_data_csv):
            return sales_data_csv
        else: 
            print('Error: No CSV file does not exist')
            exit('Script execution aborted')
    else:
        print('Error: No CSV file path provided')
        exit('Script execution aborted')

def get_order_dir(sales_sata_csv):
    
    #Get directory path of sales data CSV file
    sales_dir = os.path.dirname(sales_sata_csv)

    #Determine ordersdirectory name (Orders_YYYY-MM-DD):
    todays_date = date.today().isoformat()
    Order_dir_name = 'Orders_' + todays_date
    
    #Build the full path of the orders directory
    order_dir = os.path.join(sales_dir, Order_dir_name)

    #Make the orders directory if it does not already exist
    if not os.path.exists(order_dir):
        os.makedirs(order_dir)

    return order_dir


sales_data_csv = get_sales_csv()
print(sales_data_csv)
order_dir = get_order_dir(sales_data_csv)