// Объявление переменной tg, получающей доступ к боту.
let tg = window.Telegram.WebApp;

// Создание объекта choise с начальными значениями для свойств "type" и "name".
var choise = {
        "type": "choise_type_taro",
        "name": ""
}

// Функция для выбора типа таро с передачей имени элемента в качестве аргумента.
function choise_type_taro(item_name) {
        // Установка значения свойства "name" объекта choise равным переданному аргументу.
        choise["name"] = item_name
        // Отправка объекта choise в функцию sendData.
        tg.sendData(JSON.stringify(choise));
};

// Асинхронная функция для получения типов таро с внешнего API.
async function get_types_taro() {
        // Отправка запроса на получение типов таро с внешнего API.
    await fetch('https://hse-server.tw1.ru/api_taro/get_types_taro')
    .then((data) => {
        // Преобразование ответа в формат JSON.
        return data.json()
    })
    .then(response => {
        // Проверка наличия элемента с идентификатором "types_taro".
                if (document.getElementById("types_taro")) {
                        // Обновление содержимого элемента данными из свойства 'data' объекта response.
                        document.getElementById("types_taro").innerHTML = response['data'];
                }
    })
}

// Установка обработчика события onload для окна.
window.onload = function() {
        // Вызов функции get_types_taro при полной загрузке страницы.
        get_types_taro()
}












