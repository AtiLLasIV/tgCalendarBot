from datetime import datetime, timezone, timedelta

user_data = dict()
# Tasks_dict = dict()

date_format = "%d.%m.%Y_%H:%M"

# по умолчанию записываем сейчашнее время:
default_date_object = datetime.now().strftime(date_format)

# пока часовой пояс только МСК
offset = timedelta(hours=3)
tz = timezone(offset, name='МСК')
