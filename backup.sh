#!/bin/bash

container_name="app-woodwork-1"
backup_dir="/root/app/backup/"

date=$(date +%Y-%m-%d)

archive_name="/root/app/works_backup_$date.zip"

source <(cat /root/app/.env)

docker exec -it $container_name python manage.py dumpdata works > $backup_dir"works_dump.json"
docker cp $container_name:/app/media/ $backup_dir
# docker cp $container_name:/app/static/ $backup_dir

zip -r "$archive_name" "$backup_dir"

if [ $? -eq 0 ]; then
  echo "Архив создан успешно: $archive_name"
  rm -rf "$backup_dir"/*
  echo "Исходная папка очищена: $backup_dir"
else
  echo "Ошибка при создании архива"
fi


function send_message_with_file() {
  file="$1"
  message="$2"

  curl -F "chat_id=$TELEGRAM_TO" -F "document=@${file};type=application/octet-stream" -F "caption=$message" https://api.telegram.org/bot$TELEGRAM_TOKEN/sendDocument
  echo "Архив отправлен успешно"
}

send_message_with_file "$archive_name" "Отправка бэкапа от $date"
rm -fr $archive_name
echo "Архив удален"
