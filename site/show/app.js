// Объявление переменной tg, получающей доступ к боту.
let tg = window.Telegram.WebApp;
url = new URL(window.location.href);

type_page = url.searchParams.get('num');

document.addEventListener('DOMContentLoaded', () => {
    const magicTextElements = document.querySelectorAll('.magic-text');

    const elementInView = (el, offset = 0) => {
        const elementTop = el.getBoundingClientRect().top;
        return elementTop <= ((window.innerHeight || document.documentElement.clientHeight) - offset);
    };

    const displayScrollElement = (element) => {
        element.classList.add('visible');
    };

    const handleScrollAnimation = () => {
        magicTextElements.forEach((el) => {
            if (elementInView(el, 150)) {
                displayScrollElement(el);
            }
        });
    };

    // Вызываем анимации появления текста при первоначальной загрузке
    handleScrollAnimation();

    // Отслеживаем событие прокрутки для анимации текста
    window.addEventListener('scroll', handleScrollAnimation);
});
