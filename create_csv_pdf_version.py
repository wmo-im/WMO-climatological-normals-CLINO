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
- sort country then by mesure type and add a title for each

"""

## Importations
import pandas as pd

def add_titles(df):
    previous_country = ""
    previous_mesure = ""
    new_rows = []  

    for i, row in df.iterrows():
        # Check if the current 'Country' is different from the previous one
        if row['Country'] != previous_country:
            # Create a title row for the 'Country'
            country_title_row = [None] * len(df.columns)
            country_title_row[0] = row['Country']
            new_rows.append(country_title_row)  # Add the country title row
            previous_country = row['Country']

        # Check if the current 'mesure' is different from the previous one
        if row['mesure'] != previous_mesure:
            # Create a title row for the 'mesure'
            mesure_title_row = [None] * len(df.columns)
            mesure_title_row[2] = row['mesure']
            new_rows.append(mesure_title_row)  # Add the mesure title row
            previous_mesure = row['mesure']

        # Add the original row
        new_rows.append(row.values)

    # Convert the list of rows back to a DataFrame
    new_df = pd.DataFrame(new_rows, columns=df.columns)
    return new_df



def merge_clino_pdf_version():


    ## Creating list of additional information  
    list_month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Annual"]
    list_month_pdf = ["Station", "No", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "I-XI"]
    list_suffixes = ["Total days with ≥1 mm precipitation", "Mean Vapor Pressure", "Mean Sea Level Pressure", "Precipitation", "Mean Temperature", "Mean Maximum Temperature", "Mean Minimum Temperature", "Total Sunshine"]
    list_clino = []
    file_path ='data/data-for-arcgis-map/wmo_argis_map.csv'

    df_clino = pd.read_csv(file_path)


    df_clino_conc_countr_sort = df_clino.sort_values(by=['Country', 'mesure', 'Station']).drop(columns=['Elem', 'Rgn', 'WIGOS_ID', 'Latitude', 'Longitude', 'Elevation'])
    df_clino_conc_countr_sort['Station'], df_clino_conc_countr_sort['ID'] = df_clino_conc_countr_sort['ID'], df_clino_conc_countr_sort['Station'] 
    df_clino_conc_countr_sort.columns = ['Station', 'Country', 'ID'] + list_month + ['mesure', 'unit']


    df_clino_conc_countr_sort = add_titles(df_clino_conc_countr_sort)
    
    df_clino_conc_countr_sort = df_clino_conc_countr_sort.drop(columns=['Country', 'mesure', 'unit'])

    df_clino_conc_countr_sort.columns = list_month_pdf

    df_clino_conc_countr_sort.to_csv('data/data-for-pdf-publication/wmo_pdf_publi.csv', index=False)




    ## print information about clino
    for i, df_clino in enumerate(list_clino):
        print("Result for " + str(list_suffixes[i]))
        print(["Unique WIGOS_ID : " + str(df_clino['WIGOS_ID'].nunique()),
               "Unique ID : " + str(df_clino['ID'].nunique()), 
               "Unique station : " + str(df_clino['Station'].nunique()), 
               "Size : " + str(len(df_clino)), 
               "Empty ID : " + str(df_clino['ID'].isnull().sum()),
               "Empty WIGOS_ID : " + str(df_clino['WIGOS_ID'].isnull().sum()),
               "Empty station : " + str(df_clino['Station'].isnull().sum())])
        print("\n")

if __name__ == "__main__":
    # Execute the function 
    merge_clino_pdf_version()
