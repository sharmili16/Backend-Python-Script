import json
from gmail_scraper import open_db_connection, authenticate_service

def handle_email():
    """
    This function applies the rules from the rules.json file and 
    processes the emails from the database.
    """
    # Getting DB Connection
    connection = open_db_connection()
    cursor = connection.cursor()
    rules = []
    # Reading rules from rules.json
    with open('rules.json') as rf:
        rules = json.load(rf)['rules']

    # Going through the rules
    for rule in rules:
        rule_name = rule['description']
        print('Handling Rule:', rule_name)
        condition = rule['condition']
        filters = rule['filters']
        query = query_builder(filters, condition)
        cursor.execute(query)
        email_ids = [i[0] for i in cursor.fetchall()]
        print('Total Records Found:', len(email_ids))
        if email_ids:
            actions(email_ids, rule)
        print('')
    return

def actions(email_ids, rule):
    """
    This is a helper function that executes the rules.json-defined actions.
    """
    rule_name = rule['description']
    print('Deploying Action for Rule:', rule_name)
    action = rule['action']
    action_name = action['name']
    addLabelIds = []
    removeLabelIds = []
    
    if 'UNREAD' in action['apply']:
        addLabelIds.append('UNREAD')
    elif 'Mark as Read' in action['apply']:
        removeLabelIds.append('UNREAD')

    if action_name == 'Move Message':
        addLabelIds.append(action.get('destination'))

    service = authenticate_service()
    body = {
        "ids": email_ids,
        "addLabelIds": addLabelIds,
        "removeLabelIds": removeLabelIds
    }
    print(body)
    try:
        service.users().messages().batchModify(userId="me", body=body).execute()
        print('Action Processed for Rule: ', rule_name)
        print('')
    except Exception as e:
        print('Got Exception', e)


def query_builder(filters, condition):
    """
    This is an helper function to assemble  the query for each rules
    """
    field_mapper = {
        "From": "from_email",
        "To": "to_email",
        "Subject": "subject",
        "Date": "send_on"
    }
    query = 'WHERE '
    for filter in filters:

        predicate_raw = filter['predicate']
        field_raw = filter['field_name']
        value = filter['value']
        field = field_mapper[field_raw]

        # For Contains case
        if predicate_raw == 'contains':
            #handling non-case sensitive texts
            sub_query = f"{field} ILIKE '%{value}%'"

        # For Equal case
        elif predicate_raw == 'equal':
            sub_query = f"{field} = '{value}'"

        # For Date range case less than
        elif field_raw == 'Date' and predicate_raw == 'less than':
            sub_query = f"(NOW()::date - {field}::date) > {value}"
            print(sub_query)

        # For Date range case greater than
        elif field_raw == 'Date' and predicate_raw == 'greater than':
            sub_query = f"(NOW()::date - {field}::date) < {value}"
            print(sub_query)

        # For Date range case less than and equal
        elif field_raw == 'Date' and predicate_raw == 'less than or equal':
            sub_query = f"(NOW()::date - {field}::date) >= {value}"
            print(sub_query)
       
        # Other cases
        else:
            sub_query = ''
        
        if sub_query and condition == 'all':
            sub_query += ' and '
        elif sub_query:
            sub_query += ' or '
        
        else:
            print('Got Unhandled logic passing', predicate_raw)
            pass
        query = query + sub_query

   
    query = query.removesuffix(' or ')
    query = query.removesuffix(' and ')
    query = 'select email_id from mails '+ query
    return query

handle_email()
