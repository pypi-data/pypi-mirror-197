import pandas as pd
import numpy as np
import os
import geopandas as gpd
from glob import glob
from datetime import datetime
from shapely.validation import make_valid

def load_most_recent_dnb():
    """ This function retrieves the most recent dnb data according to a specific folder structure. """

    dtype_dict = {
    'DUNS Number':'object',
    'Marketbase ID':'object',
    'National Company ID':'object',
    'Branch ID':'object',
    'Branch ID BE':'object',
    'National Company ID BE':'object',
    'Smart ID reference code':'object',
    'Organization ID':'object',
    'Country code':'object',
    'Telephone Area code':'object',
    'Telephone Number':'object',
    'Legal Status Code on Marketbase ID':'object',
    'Legal Status Group Code on Marketbase ID':'object',
    'Linkage Type Code on MarketBase ID':'object',
    'SBI code on MarketBase ID':'object',
    'NACE Code on MarketBase ID':'object',
    'NACE Code on MarketBase ID (BE)':'object',
    'SIC Code on MarketBase ID':'object',
    'HQE DUNS Number':'object',
    'DU DUNS Number':'object',
    'GU DUNS Number':'object',
    'Smart Category on Marketbase ID':'object'
    }
    
    user_name = os.getcwd().split('\\')[2]
    dnb_folder = [(item, int(''.join(item.split('\\')[-2].split()))) for item in glob(r"C:\Users\{}\Eurofiber Nederland BV\Project GLOBE - General\02 Data Lake\01 Companies\Smart Profile/*/".format(user_name), recursive=True)]
    dnb_folder.sort(key=lambda x:x[1], reverse=True)
    dnb = pd.read_csv(dnb_folder[0][0] + 'EurofibreData_NL.csv', dtype=dtype_dict, low_memory=False)
    return dnb  


def load_ibis(specific_year=False, merged=False):
    """ this function retrieves the most recent ibis file from the specific folder, unless a specifc year is provided in string format """

    user_name = os.getcwd().split('\\')[2]
    if specific_year == False and merged == False:
        folder = [(item, int(item.split('_')[-1].split('.')[0])) for item in glob(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\ibis/*".format(user_name)) if 'MERGED' not in item]
        folder.sort(key=lambda x:x[1], reverse=True)     

        ibis = gpd.read_file(folder[0][0])
        ibis = ibis[~ibis['geometry'].isna()]
        ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)  
        ibis['geometry'] = ibis['geometry'].apply(lambda x: make_valid(x))     
        return ibis
    
    elif specific_year != False and merged == False:
        try:
            ibis = gpd.read_file(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\ibis/IBIS_NL_{}.zip".format(user_name, specific_year))
            ibis = ibis[~ibis['geometry'].isna()]
            ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)      
            ibis['geometry'] = ibis['geometry'].apply(lambda x: make_valid(x))
            return ibis        
        except:
            return np.nan    

    elif specific_year == False and merged == True:
        folder = [(item, int(item.split('_')[-1].split('.')[0])) for item in glob(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\ibis/*".format(user_name)) if 'MERGED' in item]
        folder.sort(key=lambda x:x[1], reverse=True)     

        ibis = gpd.read_file(folder[0][0])
        ibis = ibis[~ibis['geometry'].isna()]
        ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)    
        ibis['geometry'] = ibis['geometry'].apply(lambda x: make_valid(x))   
        return ibis

    else:
        try:
            ibis = gpd.read_file(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\ibis/IBIS_NL_MERGED_{}.zip".format(user_name, specific_year))
            ibis = ibis[~ibis['geometry'].isna()]
            ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)   
            ibis['geometry'] = ibis['geometry'].apply(lambda x: make_valid(x))   
            return ibis        
        except:
            return np.nan    


# def load_ibis(specific_year=False):
#     """ this function retrieves the most recent ibis file from the specific folder, unless a specifc year is provided in string format """

#     user_name = os.getcwd().split('\\')[2]
#     if specific_year == False:
#         folder = [(item, int(item.split('_')[-1].split('.')[0])) for item in glob(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\ibis/*".format(user_name))]
#         folder.sort(key=lambda x:x[1], reverse=True)     

#         ibis = gpd.read_file(folder[0][0])
#         ibis = ibis[~ibis['geometry'].isna()]
#         ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)       
#         return ibis   
#     else:
#         try:
#             ibis = gpd.read_file(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\ibis/IBIS_NL_{}.zip".format(user_name, specific_year))
#             ibis = ibis[~ibis['geometry'].isna()]
#             ibis['geometry'] = ibis['geometry'].to_crs(epsg=4326)      
#             return ibis        
#         except:
#             return np.nan     


def load_pc6(specific_year=False):
    """ this function retrieves the most recent pc6 file from the specific folder, unless a specifc year is provided in string format """

    user_name = os.getcwd().split('\\')[2]
    if specific_year == False:
        folder = [(item, int(item.split('-')[-1].split('.')[0])) for item in glob(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\postcode\pc6/*".format(user_name))]
        folder.sort(key=lambda x:x[1], reverse=True)     

        pc_6 = gpd.read_file(folder[0][0])
        pc_6 = pc_6.dropna(subset='geometry') 
        pc_6 = pc_6.to_crs({'init': 'epsg:4326'})   
        return pc_6   
    else:
        try:
            pc_6 = gpd.read_file(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\postcode\pc6/CBS-PC6-{}.zip".format(user_name, specific_year))
            pc_6 = pc_6.dropna(subset='geometry') 
            pc_6 = pc_6.to_crs({'init': 'epsg:4326'})     
            return pc_6        
        except:
            return np.nan     


def load_pc4(specific_year=False):
    """ this function retrieves the most recent pc4 file from the specific folder, unless a specifc year is provided in string format """

    user_name = os.getcwd().split('\\')[2]
    if specific_year == False:
        folder = [(item, int(item.split('-')[-1].split('.')[0])) for item in glob(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\postcode\pc4/*".format(user_name))]
        folder.sort(key=lambda x:x[1], reverse=True)     

        pc_4 = gpd.read_file(folder[0][0])
        pc_4 = pc_4.dropna(subset='geometry') 
        pc_4 = pc_4.to_crs({'init': 'epsg:4326'})   
        return pc_4   
    else:
        try:
            pc_4 = gpd.read_file(r"C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\postcode\pc4/CBS-PC4-{}.zip".format(user_name, specific_year))
            pc_4 = pc_4.dropna(subset='geometry') 
            pc_4 = pc_4.to_crs({'init': 'epsg:4326'})     
            return pc_4        
        except:
            return np.nan      
        

def load_pc_hn(specific_year=False):
    """ this function loads the most recent pc_hn file by CBS/scraper from the specific folder, unless a specific year is provided in string format """

    user_name = os.getcwd().split('\\')[2]    
    if specific_year == False:
        folder = [(item, datetime.strptime(item.split('\\')[-1].split('_')[0][-8:], '%Y%m%d')) for item in glob(r'C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\postcode\pc_hn/*'.format(user_name)) if 'csv' in item]
        folder.sort(key=lambda x:x[1], reverse=True)   
        pc_hn = pd.read_csv(folder[0][0], sep=';')
        return pc_hn
    else:
        folder = [(item, datetime.strptime(item.split('\\')[-1].split('_')[0][-8:], '%Y%m%d')) for item in glob(r'C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\postcode\pc_hn/*'.format(user_name)) if 'csv' in item]
        folder.sort(key=lambda x:x[1], reverse=True)   
        [item for item in folder if item[1].year==int(specific_year)]
        pc_hn = pd.read_csv(folder[0][0], sep=';')
        return pc_hn 
    

def load_most_recent_dnb_enriched():
    """ This function retrieves the most recent enriched dnb data according to a specific folder structure. """

    dtype_dict = {
    'DUNS Number':'object',
    'Marketbase ID':'object',
    'National Company ID':'object',
    'Branch ID':'object',
    'Branch ID BE':'object',
    'National Company ID BE':'object',
    'Smart ID reference code':'object',
    'Organization ID':'object',
    'Country code':'object',
    'Telephone Area code':'object',
    'Telephone Number':'object',
    'Legal Status Code on Marketbase ID':'object',
    'Legal Status Group Code on Marketbase ID':'object',
    'Linkage Type Code on MarketBase ID':'object',
    'SBI code on MarketBase ID':'object',
    'NACE Code on MarketBase ID':'object',
    'NACE Code on MarketBase ID (BE)':'object',
    'SIC Code on MarketBase ID':'object',
    'HQE DUNS Number':'object',
    'DU DUNS Number':'object',
    'GU DUNS Number':'object',
    'Smart Category on Marketbase ID':'object',
    'RIN_NUMMER':'object'
    }
    
    user_name = os.getcwd().split('\\')[2]
    dnb_folder = [(item, int(''.join(item.split('\\')[-2].split()))) for item in glob(r"C:\Users\{}\Eurofiber Nederland BV\Project GLOBE - General\02 Data Lake\01 Companies\SP Enriched/*/".format(user_name), recursive=True)]
    dnb_folder.sort(key=lambda x:x[1], reverse=True)
    dnb = pd.read_csv(dnb_folder[0][0] + 'EurofibreData_NL.csv', dtype=dtype_dict, low_memory=False)
    return dnb


def load_smartprofile_contacts():
    """ this function loads the contacts file saved a the specific location"""

    dtype_dict = {
    'Site Key':'object',
    'Phone':'object',
    'USSIC87 code':'object',
    'Nace 2.0':'object',
    'Company Number (National ID)':'object',
    'Contact key':'object'
    }

    user_name = os.getcwd().split('\\')[2]
    file = pd.read_excel(r'C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\smartprofile\contact_details\0._PROSPECT_LIST_WITH_CONTACTS_-_NL.xlsx'.format(user_name), dtype=dtype_dict)
    return file


def load_sbi():
    """ this function loads the sbi verticals etc. """

    dtype_dict = {
    'SBI 2-cijfer':'object',
    'SBI volledig':'object',
    }

    user_name = os.getcwd().split('\\')[2]
    file = pd.read_excel(r'C:\Users\{}\Eurofiber Nederland BV\My Folder - General\database\sbi\SBI Overzicht Codes en Omschrijvingen.xlsx'.format(user_name), dtype=dtype_dict, sheet_name='SBI Compleet') 
    return file