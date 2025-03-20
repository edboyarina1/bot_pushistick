import requests
import csv
from datetime import datetime, timedelta
import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_data():
    gid = sheet_gids['Преподаватели']
    SHEETS_URL = f
    response = requests.get(SHEETS_URL)
    response.raise_for_status()
    decoded_content = response.content.decode('utf-8')
    reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
    data = [row for row in reader]
    logger.info("Fetched main data: %s", data)
    return data

def fetch_individual_sheet(surname):
    try:
        gid = sheet_gids.get(surname)
        individual_sheet_url = f
        response.raise_for_status()
        decoded_content = response.content.decode('utf-8')
        reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')
        data = [row for row in reader]
        logger.info("Fetched data for sheet %s: %s", surname, data)
        return data
    except Exception as e:
        logger.error("Error fetching data for sheet %s: %s", surname, e)
        return []

def get_notifications_data():
    main_data = fetch_data()
    notifications = []

    for row in main_data:
        surname = row['Фамилия']
        telegram_id = row['Телеграмм']
        if not surname or not telegram_id:
            logger.warning("Skipping row due to missing surname or telegram_id: %s", row)
            continue

        individual_data = fetch_individual_sheet(surname)

        for entry in individual_data:
            logger.info("Processing entry from sheet %s: %s", surname, entry)
            try:
                date_str = entry['Дата']
                time_str = entry['Время']
                if date_str and time_str:
                    notification_time = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M") - timedelta(hours=1)

                    notifications.append({
                        'telegram_id': telegram_id,
                        'notification_time': notification_time,
                        'message': f"Напоминание: У вас сессия с {entry['Студент']} в {entry['Время']} на {entry['Дата']}."
                    })
            except KeyError as e:
                logger.error("Missing key %s in entry from sheet %s: %s", e, surname, entry)
            except ValueError as e:
                logger.error("Error parsing date/time in entry from sheet %s: %s", surname, entry)

    logger.info("Notifications data: %s", notifications)
    return notifications

def get_user_sessions(username):
    main_data = fetch_data()
    sessions = []

    for row in main_data:
        if row['Телеграмм'] == username:
            surname = row['Фамилия']
            logger.info("Found surname %s for username %s", surname, username)
            individual_data = fetch_individual_sheet(surname)

            for entry in individual_data:
                if entry['Дата'] and entry['Время']:
                    sessions.append({
                        'student': entry['Студент'],
                        'date': entry['Дата'],
                        'time': entry['Время']
                    })
    logger.info("Sessions for username %s: %s", username, sessions)
    return sessions