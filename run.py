import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    get sales figures from the user
    """
    while True:
        print("please enter sales data from the last market.") 
        print("data should be six numbers seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
    
        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("data is valid")
            break

    return sales_data


def validate_data(values):
    """
    inside the try, converts all string values into intergers.
    raises value error if string cannot be converted into int, or if there arent exactly 6 values.
    """
   
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"EXACTLY 6 VALUES REQUIRED, YOU PROVIDEED {len(values)}"

            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_sales_worksheet(data):
    """
    update sales worksheet add new row with list of data provided 
    """

    print ("updating worksheet  .... \n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    compare sales and stock and calculate the surplus of each item
    surplus = sales - stock
    positive surplus indicates waste 
    negative surplus = extras made when stock sold out 
    """
    print("calculating surplus data .... \n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)

def main():
    """
    run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)


print("welcome to ls data automation")
main()