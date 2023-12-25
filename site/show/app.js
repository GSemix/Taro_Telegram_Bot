// Объявление переменной tg, получающей доступ к боту.
let tg = window.Telegram.WebApp;
url = new URL(window.location.href);

type_page = url.searchParams.get('num');

// Объявление переменной tg, получающей доступ к боту.
let tg = window.Telegram.WebApp;
url = new URL(window.location.href);

document.addEventListener('DOMContentLoaded', () => {
    const fadeElements = document.querySelectorAll('.text-background');

    const elementInView = (el, offset = 0) => {
        const elementTop = el.getBoundingClientRect().top;
        return elementTop <= ((window.innerHeight || document.documentElement.clientHeight) - offset);
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
