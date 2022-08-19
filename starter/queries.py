import psycopg2
from psycopg2 import Error

from database import get_connected

try:
    # connection to database

    connection = get_connected()

    # creates cursor
    cursor = connection.cursor()
  
    ############# SQL QUERIES TO EXTRACT INFORMATION #################

    master_query = """ SELECT * FROM invoices JOIN 
                            customers ON invoices.customer_id = customers.id """

    outdoors_query = """ SELECT * FROM invoices JOIN 
                            customers ON invoices.customer_id = customers.id
                            WHERE invoices.product_category = 'Outdoors' """

    garden_query = """  SELECT * FROM invoices JOIN 
                            customers ON invoices.customer_id = customers.id
                            WHERE invoices.product_category = 'Garden' """ 
    
    product_revenue_query = """ SELECT product_category, SUM(unit_price*quantity) FROM invoices
                                 GROUP BY product_category
                                 ORDER BY SUM DESC """
                        
    
    ############ COPYING SQL QUERY OUTPUTS TO CSV FILES #############

    # master_query output
    master_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(master_query)

    # outdoors_query output
    outdoors_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(outdoors_query)

    # garden_query output
    garden_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(garden_query)

    # top_products_query
    product_revenue_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(product_revenue_query)


    #### CREATE MASTER CSV ####

    with open('master.csv', 'w') as file:
        cursor.copy_expert(master_output, file)
        print("master.csv written successfully.")


    #### CREATE OUTDOORS CSV ####

    with open('outdoors.csv', 'w') as file:
        cursor.copy_expert(outdoors_output, file)
        print("outdoors.csv written successfully.")


    #### CREATE GARDEN CSV ####

    with open('garden.csv', 'w') as file:
        cursor.copy_expert(garden_output, file)
        print("garden.csv written successfully.")


    #### CREATE TOP PRODUCTS CSV ####

    with open('product_revenue.csv', 'w') as file:
        cursor.copy_expert(product_revenue_output, file)
        print("product_revenue.csv written successfully.")


except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL DB", error)

finally:
    if (connection):
        cursor.close()
        connection.close()
        print("DB connection is closed.")