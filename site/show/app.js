// Объявление переменной tg, получающей доступ к боту.
let tg = window.Telegram.WebApp;
url = new URL(window.location.href);

type_page = url.searchParams.get('num');

document.addEventListener('DOMContentLoaded', () => {
    const magicTextElements = document.querySelectorAll('.magic-text');
    const divider = document.querySelector('.divider');

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

        // Управление анимацией разделителя
        const magicTextVisible = Array.from(magicTextElements).some(el => elementInView(el, 150));
        if (magicTextVisible) {
            divider.style.animation = 'none'; // Отключить анимацию, если текст виден
        } else {
            divider.style.animation = ''; // Включить анимацию, если текст скрыт
        }
    };

    // Вызываем анимации появления текста и управление анимацией разделителя при первоначальной загрузке
    handleScrollAnimation();

    // Отслеживаем событие прокрутки для анимаций текста и разделителя
    window.addEventListener('scroll', handleScrollAnimation);
});
