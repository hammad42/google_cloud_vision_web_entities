def BQ(documentEntities: dict,table_id):

     from google.cloud import bigquery
     print("Inserting into BQ ************** ")
     #Insert into BQ    
     client = bigquery.Client()    

     table = client.get_table(table_id)

     print ('Adding the row')
     rows_to_insert= [documentEntities]

     print (' ********** NEW Row Column: ',rows_to_insert)
     errors = client.insert_rows_json(table, rows_to_insert) 
     if errors == []:

          print("New rows have been added.") 
     else:

          print ('Encountered errors: ',errors)
     return errors