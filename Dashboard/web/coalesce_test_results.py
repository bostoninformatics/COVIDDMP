import pandas as pd

def combine_results(test_tb):

    # Read in data and split TestDateTime and define indices for combine_first
    test_df = test_tb.copy(deep=False)
    test_df = test_df[['PersonID', 'TestDateTime', 'TestLocation', 'TestResult', 'OrderableItemName', 'LabChemTestName', 'Source']]
    test_df['TestDateTime'] = pd.to_datetime(test_df['TestDateTime']) 
    test_df['TestDate'] = test_df['TestDateTime'].dt.date
    test_df['TestMinute'] = test_df['TestDateTime'].dt.minute
    test_df['TestSecond'] = test_df['TestDateTime'].dt.second
    test_df.set_index(["PersonID", "TestResult", "TestDate", "TestMinute", "TestSecond"], inplace=True, 
                      append=False, drop=True)
    
    # Split data by source, separate user entered data, remove duplicate entries from each source and reset indices for entered
    # Case if Fileman and CDW are present
    if any(test_df['Source'] == 'CDW') and any(test_df['Source'] == 'FileMan'):
         FileMan, CDW = [x for _, x in test_df.groupby(test_df['Source'] == 'CDW')]
         CDW = CDW.copy(deep=False)
         CDW = CDW.drop_duplicates(subset=['TestDateTime'], keep='first', inplace=False)
         FileMan = FileMan.loc[FileMan['Source'] == 'FileMan',].copy(deep=False)
         FileMan = FileMan.drop_duplicates(subset=['TestDateTime'], keep='first', inplace=False)
   
         # Combine fileman and CDW data, using CDW data unless it is empty.  Then concatenate with user entered data
         test_table = CDW.combine_first(FileMan)
         test_table = test_table.reset_index()
         test_table = test_table[['PersonID', 'TestLocation', 'TestDateTime', 'TestResult', 'OrderableItemName', 'LabChemTestName', 'Source']] 
         test_table = test_table.sort_values(by='TestDateTime').copy(deep=False)
     
    # If there is no Fileman data, only use CDW data
    elif any(test_df['Source'] == 'CDW') and not any(test_df['Source'] == 'FileMan'):
         CDW = test_df.loc[test_df['Source'] == 'CDW',].copy(deep=False)
         CDW = CDW.drop_duplicates(subset=['TestDateTime'], keep='first', inplace=False)
         CDW = CDW.reset_index()
         CDW = CDW[['PersonID', 'TestLocation', 'TestDateTime', 'TestResult', 'OrderableItemName', 'LabChemTestName', 'Source']] 
         CDW = CDW.sort_values(by='TestDateTime')
         test_table = CDW.copy(deep=False)
    
    # If there is no CDW data, only use Fileman data
    elif not any(test_df['Source'] == 'CDW') and any(test_df['Source'] == 'FileMan'):
         FileMan = test_df.loc[test_df['Source'] == 'FileMan',].copy(deep=False)
         FileMan = FileMan.drop_duplicates(subset=['TestDateTime'], keep='first', inplace=False)
         FileMan = FileMan.reset_index()
         FileMan = FileMan[['PersonID', 'TestLocation', 'TestDateTime', 'TestResult', 'OrderableItemName', 'LabChemTestName', 'Source']] 
         FileMan = FileMan.sort_values(by='TestDateTime')
         test_table = FileMan.copy(deep=False)

    # If neither CDW nor FileMan data are present return an empty table
    else:
         test_table = pd.DataFrame(columns=['PersonID', 'TestLocation', 'TestDateTime', 'TestResult', 'OrderableItemName', 'LabChemTestName', 'Source'])
    
    # Return Result
    return test_table