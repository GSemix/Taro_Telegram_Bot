// Объявление переменной tg, получающей доступ к боту.
let tg = window.Telegram.WebApp;
url = new URL(window.location.href);

id = url.searchParams.get('id');

// Объявление переменной tg, получающей доступ к боту.
let tg = window.Telegram.WebApp;
url = new URL(window.location.href);

document.addEventListener('DOMContentLoaded', () => {
    const fadeElements = document.querySelectorAll('.text-background');

    const elementInView = (el, offset = 0) => {
        const elementRect = el.getBoundingClientRect();
        const elementTop = elementRect.top;
        const elementBottom = elementRect.bottom;

        // Проверяем, находится ли элемент частично или полностью в области видимости
        return (
            elementTop + offset < window.innerHeight && 
            elementBottom - offset > 0
        );
    };

    const displayElement = (element) => {
        element.classList.add('fade-in');
    };

    const handleScrollAnimation = () => {
        fadeElements.forEach((el) => {
            if (elementInView(el, 150)) {
                displayElement(el);
            }
        });
    };

    // Вызываем анимации при первоначальной загрузке и отслеживаем событие прокрутки
    handleScrollAnimation();
    window.addEventListener('scroll', handleScrollAnimation);
});

async function get_content() {
    console.log(1)
    await fetch('https://hse-server.tw1.ru/api_taro/get_taro_answer/' + id)
    .then((data) => {
        return data.json()
    })
    .then(response => {
                if (document.getElementById("content")) {
                        document.getElementById("content").innerHTML = response['data'];
                }
    })
    console.log(2)
}

window.onload = function() {
        console.log(0)
        get_content()
}








