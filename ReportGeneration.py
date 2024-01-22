import pandas as pd
import shelve


def combine_databases():  # merge all data into 1 table
    database_names = ["Members", "Inventory", "Question", "OrderHist", "Admin"]
    all_dataframes = []

    for db_name in database_names:
        try:
            with shelve.open('database.db', 'r') as db:
                data_dict = db.get(db_name, {})
        except Exception as e:
            print(f"Error in retrieving data from database.db for '{db_name}': {e}")
            continue

        if not data_dict:
            print(f"No data found for '{db_name}' in the database.")
            continue

        # convert data to DataFrame
        df = pd.DataFrame([obj.as_dict() for obj in data_dict.values()])

        # add prefix to columns to differentiate the diff dicta
        df.columns = [f'{db_name}_{col}' for col in df.columns]

        all_dataframes.append(df)

    if not all_dataframes:
        print("No data available for any of the specified databases.")
        return None

    # Concatenate all DataFrames
    combined_df = pd.concat(all_dataframes, axis=1)

    return combined_df

    # info on combined_df
    #  #   Column                        Non-Null Count  Dtype
    # ---  ------                        --------------  -----
    #  0   Members_Member ID             3 non-null      float64
    #  1   Members_First name            3 non-null      object
    #  2   Members_Last name             3 non-null      object
    #  3   Members_Email                 3 non-null      object
    #  4   Members_Phone no.             3 non-null      object
    #  5   Members_Password              3 non-null      object
    #  6   Inventory_Product ID          3 non-null      float64
    #  7   Inventory_Name                3 non-null      object
    #  8   Inventory_Price               3 non-null      object
    #  9   Inventory_Category            3 non-null      object
    #  10  Inventory_Remarks             3 non-null      object
    #  11  Inventory_Recommended drinks  3 non-null      object
    #  12  Inventory_Image               3 non-null      object
    #  13  Question_Question ID          1 non-null      float64
    #  14  Question_Email                1 non-null      object
    #  15  Question_Title                1 non-null      object
    #  16  Question_Question             1 non-null      object
    #  17  Question_Date posted          1 non-null      object
    #  18  Question_Overall rating       1 non-null      object
    #  19  Question_Written feedback     1 non-null      object
    #  20  OrderHist_Order ID            6 non-null      int64
    #  21  OrderHist_Products            6 non-null      object
    #  22  OrderHist_Date                6 non-null      datetime64[ns]
    #  23  OrderHist_Payment amount      6 non-null      float64
    #  24  OrderHist_Name                6 non-null      object
    #  25  OrderHist_Email               6 non-null      object
    #  26  OrderHist_Phone no.           6 non-null      object
    #  27  Admin_Admin ID                2 non-null      float64
    #  28  Admin_First name              2 non-null      object
    #  29  Admin_Last name               2 non-null      object
    #  30  Admin_Email                   2 non-null      object
    #  31  Admin_Password                2 non-null      object
