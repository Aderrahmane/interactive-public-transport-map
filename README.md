First create the tables in your local SQL database
use the python file(insert_for_all_files) to generate the insert lines for every table by redirecting the standard output from executing the python code into a file then copying it and executing the SQL query
then make sure that the username database user host and password in the main python file are changed to those of your local database
execute the main python code to start the application
Click on a point on the map as the starting location.
Choose the destination by clicking on another point on the map.
Select a mode of transportation.
Click on "Go."
The application provides a route with the name of the chosen transportation route and the estimated time.
if there is no mean of transport that passes the position you selected no route will be giving
