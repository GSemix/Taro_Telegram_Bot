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
        let magicTextVisible = false;

        magicTextElements.forEach((el) => {
            if (elementInView(el, 150)) {
                displayScrollElement(el);
                magicTextVisible = true;
            }
        });

        divider.style.animation = magicTextVisible ? 'none' : '';
    };

    handleScrollAnimation();
    window.addEventListener('scroll', handleScrollAnimation);
});
