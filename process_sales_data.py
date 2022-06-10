from sys import argv, exit
import os
from datetime import date
import pandas as pd
import re

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

def get_order_dir(sales_data_csv):
    
    #Get directory path of sales data CSV file
    sales_dir = os.path.dirname(sales_data_csv)

    #Determine ordersdirectory name (Orders_YYYY-MM-DD):
    todays_date = date.today().isoformat()
    Order_dir_name = 'Orders_' + todays_date
    
    #Build the full path of the orders directory
    order_dir = os.path.join(sales_dir, Order_dir_name)

    #Make the orders directory if it does not already exist
    if not os.path.exists(order_dir):
        os.makedirs(order_dir)

    return order_dir

def split_sales_into_orders(sales_data_csv, order_dir):

    # Read data from ther sales data CSV into a DataFrame
    sales_df = pd.read_csv(sales_data_csv)

    #Inserting new column for total price
    sales_df.insert(7, 'TOTAL PRICE', sales_df['ITEM QUANTITY'] * sales_df['ITEM PRICE'])

    #Drop unwanted coumns
    sales_df.drop(columns=['ADDRESS', 'CITY', 'STATE', 'POSTAL CODE', 'COUNTRY'], inplace=True)

    for order_id, order_df in sales_df.groupby('ORDER ID'):

        #Drop the order ID Column
        order_df.drop(columns=['ORDER ID'], inplace=True)

        #Sort the order by item number
        order_df.sort_values(by='ITEM NUMBER', inplace=True)

        #Add grand total row at the bottom
        grand_total = order_df['TOTAL PRICE'].sum()
        grand_total_df = pd.DataFrame({'ITEM PRICE': ['GRAND TOTAL:'], 'TOTAL PRICE': [grand_total]})
        order_df = pd.concat([order_df, grand_total_df])

        #Determine the save path of the order file
        customer_name = order_df['CUSTOMER NAME'].values[0]
        customer_name = re.sub(r'\W', '', customer_name)
        order_file_name = 'Order' + str(order_id) + '_' + customer_name + '.xlsx'
        order_file_path = os.path.join(order_dir, order_file_name)

        #Save the order information to an Excel spreadsheet
        sheet_name = 'Order #' + str(order_id)
        order_df.to_excel(order_file_path, index=False, sheet_name=sheet_name)

     



sales_data_csv = get_sales_csv()
order_dir = get_order_dir(sales_data_csv)
split_sales_into_orders(sales_data_csv, order_dir)