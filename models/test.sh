echo 'create Client fuulname="abu malik" email="aaaaaaaae@mail.com" password_hash="123456"' | Foodify_MYSQL_USER=root Foodify_MYSQL_PWD=root Foodify_MYSQL_HOST=localhost Foodify_MYSQL_DB=foodify_db ./console.py

echo 'create Client username="migo" email="mg@mail.com" password_hash="1111111"' | Foodify_MYSQL_USER=root Foodify_MYSQL_PWD=root Foodify_MYSQL_HOST=localhost Foodify_MYSQL_DB=foodify_db ./console.py



CREATE USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';


GRANT ALL PRIVILEGES ON *.* TO 'test'@'localhost';

FLUSH PRIVILEGES;

