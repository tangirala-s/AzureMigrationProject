import logging
import azure.functions as func
import psycopg2-binary
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    connection = psycopg2.connect(host="migrationserver.postgres.database.azure.com",
                                    dbname="tehcconfdb",
                                    user="serveradmin@migrationserver",
                                    password="P@ssword")
    cursor = connection.cursor()

    try:
        # TODO: Get notification message and subject from database using the notification_id
        logging.info('Getting notification message and subject from database using the notification_id')
        id_query = cursor.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))

        # TODO: Get attendees email and name
        logging.info('Getting attendees email and name')
        cursor.execute("SELECT first_name, last_name, email FROM attendee;")
        attendees = cursor.fetchall()

        # TODO: Loop through each attendee and send an email with a personalized subject
        logging.info('Looping through each attendee and send an email with a personalized subject')
        for attendee in attendees:
                subject = '{}: {}'.format(attendee.first_name, id_query.subject)
                Mail(attendee.email, subject, id_query.message)

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        logging.info('Updating the notification table')
        completed_date = datetime.utcnow()
        status = 'Notified {} attendees'.format(len(attendees))
        update_query = cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(status, completed_date, notification_id))

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        connection.rollback()
    finally:
        # TODO: Close connection
        cursor.close()
        connection.close()
