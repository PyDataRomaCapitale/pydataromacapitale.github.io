// custom JS here
document.addEventListener('DOMContentLoaded', function() {
    const layers = Array.from(document.querySelectorAll('.parallax-layer[data-speed]'))
        .map(el => ({ el, speed: parseFloat(el.dataset.speed) || 0 }))
        .filter(layer => layer.speed > 0);

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    if (!layers.length || prefersReducedMotion.matches) {
        return;
    }

    let ticking = false;

    const updateLayers = () => {
        const scrollY = window.scrollY || window.pageYOffset;

        layers.forEach(({ el, speed }) => {
            el.style.transform = `translate3d(0, ${-scrollY * speed}px, 0)`;
        });

        ticking = false;
    };

    const onScroll = () => {
        if (!ticking) {
            window.requestAnimationFrame(updateLayers);
            ticking = true;
        }
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    updateLayers();

    prefersReducedMotion.addEventListener('change', event => {
        if (event.matches) {
            layers.forEach(({ el }) => el.style.transform = '');
            window.removeEventListener('scroll', onScroll);
        }
    });
});
