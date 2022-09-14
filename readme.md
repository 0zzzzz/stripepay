##  Запуск проекта:
### тестовый администратор log/pass: admin/admin 

pip install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8078

___
## Номер тестовой карты (остальные реквизиты любые):
4242 4242 4242 4242

___
## Запуск проекта через docker:
### Предварительно заменив в stripepay/settings.py sqlite (83-88 строки) на postgresql (90-99)
### docker-compose создаёт вольюм для базы данных в папке с проектом
### Доступен по порту :8078

docker-compose up

docker-compose run web python manage.py createsuperuser -- создать суперпользователя
___

## API эндпойнты:

http://localhost:8078/item/<pk>
GET -- выводит HTML страницу, на которой будет информация о выбранном Item и кнопка Buy.

http://localhost:8078/buy/<pk>
GET -- переход на форму оплаты товара по его id

http://localhost:8078/order/<pk>
GET -- выводит HTML страницу, на которой будет информация о выбранном заказе и кнопка Buy.

http://localhost:8078/buy_order/<pk>
GET -- переход на форму оплаты заказа по его id
