# Тестовое задание Летней школы Yandex Backend 2022

Полное задание находится в файле [Task.md](https://github.com/koted0/Yandex_MegaMarket_2022/blob/main/Task.md)

Спецификация OpenAPI для задания [openapi.yaml](https://github.com/koted0/Yandex_MegaMarket_2022/blob/main/openapi.yaml)

# Описание #

В данном задании вам предлагается реализовать бэкенд для веб-сервиса сравнения цен, аналогичный сервису [Яндекс Товары](https://yandex.ru/products). Обычно взаимодействие с такими сервисами происходит следующим образом:
1. Представители магазинов загружают информацию о своих товарах и категориях. Также можно изменять и удалять информацию о ранее загруженных товарах и категориях.
2. Покупатели, пользуясь веб-приложением, могут искать предложения разных магазинов, сравнивать цены и следить за их динамикой и историей.

Ваша задача - разработать REST API сервис, который позволяет магазинам загружать и обновлять информацию о товарах, а пользователям - смотреть какие товары были обновлены за последние сутки, а также следить за динамикой цен товара или категории за указанный интервал времени.
