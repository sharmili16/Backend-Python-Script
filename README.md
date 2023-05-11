## Standalone Python Script for Gmail API:
## Workflow:
1.	Gmail Authentication with OAuth2client
2.	By creating a project, enabling the APIs & Services and creating the OAuth client ID, download the ‘credentials.json’ from the Google cloud platform.
3.	From the ‘gmail_scraper’ , the script will call the ‘authenticate.service() ’
4.	To run the project, 

      a.	pip install –r reqirements.txt
      
      b.	python gmails_to_db.py, the emails are processed , rows are inserted to the database and the database connection is closed.
      
      c.	After successful authentication, ‘token.json’ is generated automatically.
      
      d.	Python actions_on_gmail.py, records matching to the ‘rules.json’ is displayed.
      
      ![image](https://github.com/sharmili16/Backend-Python-Script/assets/92683122/d36d41dc-4409-4cc4-a967-20a694731e78)

      
      e.	The inbox e-mails specified in the rules is now block shifted to SPAM folder.
      
      ![image](https://github.com/sharmili16/Backend-Python-Script/assets/92683122/9ff2ca13-df86-4860-abdf-e5b1367c9442)

## Storing the Data in Database:
1.	PostgreSQL is used to store the database.
2.	A New Database called “project” is created and a table is created in pgAdmin4
3.	The rows are inserted to the database when gmails_to_db runs.

![image](https://github.com/sharmili16/Backend-Python-Script/assets/92683122/8c6f2d85-870b-44f2-ba34-82acac1eb52e)





 
