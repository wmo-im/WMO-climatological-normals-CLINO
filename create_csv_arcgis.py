"""
Create a function that merge the 8 principal clino data frames:

 - wmo_normals_9120_DP01
 - wmo_normals_9120_MNVP
 - wmo_normals_9120_MSLP
 - wmo_normals_9120_PRCP
 - wmo_normals_9120_TAVG
 - wmo_normals_9120_TMAX
 - wmo_normals_9120_TMIN
 - wmo_normals_9120_TSUN

create a merged solution with :
- 1 feature per month (12 in total)
- 1 row per mesure : n rows *8 

"""

## Importations
import pandas as pd

def change_wrong_lines(file_path, expected_columns, delimiter=',') : 
    valid_data = []    # To store valid rows

    # Open and read the CSV file line by line
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):  # line numbers start at 1
            # Split the row into columns using the given delimiter
            row = line.strip().split(delimiter)
            
            # Check if the row has the expected number of columns
            if len(row) == expected_columns:
                valid_data.append(row)  # Add valid rows to the list
            else:
                # Manage honk kong stations
                if "Hong_Kong" in row:
                    print(f"Row {line_num} has 'Hong_kong' and '_china' separated in 2 colums")

                    index = row.index("Hong_Kong")  # Get index of "Hong_Kong"

                    # Merge "Hong_Kong" with the next value and remove the next value
                    if index + 1 < len(row):  # Ensure there's a value to merge
                        row[index] = row[index] + row[index + 1]  # Merge with the next value
                        row.pop(index + 1)  # Remove the next value after "Hong_Kong"

                    # Add the fixed row to valid_data if the length now matches expected_columns
                    if len(row) == expected_columns:
                        valid_data.append(row)
                        print(f"Row {line_num} is now valid")
                    else:
                        print(f"Row {line_num} is still invalid after fixing: {row}")

    # Save the valid data to a new CSV (or overwrite the original)
    with open(file_path, 'w') as output_file:
        for row in valid_data:
            output_file.write(delimiter.join(row) + '\n')



def merge_clino_arcgismap():

    ## Creating list of additional information  
    list_month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Annual"]
    list_month_pdf = ["Station", "No", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "I-XI"]
    list_unit = ["Days", "hPa", "hPa", "mm", "Deg_C", "Deg_C", "Deg_C", "hours"]
    list_suffixes = ["Total days with ≥1 mm precipitation", "Mean Vapor Pressure", "Mean Sea Level Pressure", "Precipitation", "Mean Temperature", "Mean Maximum Temperature", "Mean Minimum Temperature", "Total Sunshine"]
    list_files = ["wmo_normals_9120_DP01", "wmo_normals_9120_MNVP", "wmo_normals_9120_MSLP", "wmo_normals_9120_PRCP", "wmo_normals_9120_TAVG", "wmo_normals_9120_TMAX", "wmo_normals_9120_TMIN", "wmo_normals_9120_TSUN"]
    list_clino = []
    
    ## Upload the data and clean the string
    for file in list_files:
        data_path = "data/data-composite-primary-parameters/" + file + ".csv"
        try : 
            df_clino = pd.read_csv(data_path)

        except Exception as e: 
            print(f"WARNING : {e}") 
            df_clino_wrong = pd.read_csv(data_path, on_bad_lines='skip')
            change_wrong_lines(data_path, len(df_clino_wrong.columns), delimiter=',')
            df_clino = pd.read_csv(data_path)

        df_clino.columns = df_clino.columns.str.strip()
        df_clino['Station'] = df_clino['Station'].str.strip()
        list_clino.append(df_clino)



    # Create a measure type column 
    for i, df in enumerate(list_clino):
        df["mesure"] = [list_suffixes[i] for a in range(len(df))]
        df["unit"] = [list_unit[i] for a in range(len(df))]
    
    # Concatenate the 8 dataframes
    df_clino_conc = pd.concat(list_clino)
    
    [pd.to_numeric(df_clino_conc[value]) for value in list_month]
    
    ## cleaning 
    for month in list_month:
        df_clino_conc.loc[df_clino_conc[month]==-99.90] = None
        df_clino_conc.loc[df_clino_conc[month]<-99] = None
    # Can be activate for DEBUG : 
    # print(f"numbers of values changed form -99.90 to None  : {str(df_clino_conc.loc[df_clino_conc[month]==-99.9][month].count())}")
    
    df_clino_conc.to_csv('data/data-for-arcgis-map/wmo_argis_map.csv', index=False)


if __name__ == "__main__":
    # Execute the function 
    merge_clino_arcgismap()