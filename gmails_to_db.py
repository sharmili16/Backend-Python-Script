import psycopg2
from gmail_scraper import open_db_connection, authenticate_service


def getEmails(count):
	"""
	This function imports the logged-in user's email list into the Postgres database.
	"""
	## call the authenticate_service() from gmail_scraper and authenticates the user
	service = authenticate_service()

	# messages().list() - Lists the messages in the user's mailbox and maxResult can be altered
	result = service.users().messages().list(maxResults=email_count, userId='me').execute()
	messages = result.get('messages')
	print(result)

	#Getting DB Connection
	connection = open_db_connection()
	cursor = connection.cursor()

	# Mapping between email header names and database column names
	header_map = {
		'Subject': 'subject',
		'From': 'from_email',
		'To': 'to_email',
		'Date': 'send_on'
	}

	items = []
	print('Processing Emails')
	
	#Iterating through messages
	for msg in messages:
		# Get the message from its id
		email_id = msg.get('id')
		# messages().get() - Gets the specified message
		txt = service.users().messages().get(userId='me', id=email_id).execute()

		try:
			payload = txt.get('payload', {})
			headers = payload.get('headers', [])
			#print(headers) - contains the entire json response


			header_values = {}
			for header in headers:
				name = header.get('name', header['name'])
				value = header['value']
				header_values[header_map.get(name, name)] = value	

					
			header_values['send_on'] = header_values['send_on'].removesuffix(' (UTC)') if 'send_on' in header_values else None
			
			subject = header_values.get('subject')
			sender = header_values.get('from_email')
			receiver = header_values.get('to_email')
			date = header_values.get('send_on')
			
			items.append((str(email_id), str(sender), str(receiver), str(subject), str(date)))

		except Exception as e:
			print('Got Exception', e)

	# Batch insert into the database			
	insert_query = '''
	INSERT INTO MAILS (email_id, from_email, to_email, subject, send_on) VALUES (%s, %s, %s, %s, %s)
	'''
	try:
		cursor.executemany(insert_query, items)
		connection.commit()
		print(f"Inserted {len(items)} rows into the database.")
	except (Exception, psycopg2.Error) as error:
		print("Error while inserting into PostgreSQL", error)
		
		
	#Close the database connection
	cursor.close()
	connection.commit()
	print("Database connection closed.")

email_count = 25
getEmails(email_count)
