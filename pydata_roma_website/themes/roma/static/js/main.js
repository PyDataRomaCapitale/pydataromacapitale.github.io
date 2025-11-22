// custom JS here
document.addEventListener('DOMContentLoaded', function() {
    const SKYLINE_ASPECT = 317.77332 / 666.69336; // height / width of skyline SVGs
    const root = document.documentElement;
    const parallaxBackground = document.querySelector('.parallax-background');
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    const layers = Array.from(document.querySelectorAll('.parallax-layer[data-speed]'))
        .map(el => ({
            el,
            speed: parseFloat(el.dataset.speed) || 0,
            baseOffset: parseFloat(el.dataset.offset) || 0,
            lift: parseFloat(el.dataset.lift) || 0,
            scale: parseFloat(getComputedStyle(el).getPropertyValue('--layer-scale')) || 1,
            offsetPx: 0
        }))
        .filter(layer => layer.speed > 0);

    const updateParallaxSizing = () => {
        const viewportWidth = window.innerWidth || root.clientWidth;
        const viewportHeight = window.innerHeight || root.clientHeight;
        const isMobile = viewportWidth <= 768;
        const targetTopRatio = isMobile ? 0.12 : 0.05; // keep skylines higher on mobile

        const maxScale = layers.length
            ? layers.reduce((max, layer) => Math.max(max, layer.scale), 1)
            : 1;
        const baseWidth = viewportWidth / Math.max(1, maxScale);
        const target = parallaxBackground || root;
        target.style.setProperty('--parallax-base-width', `${baseWidth}px`);

        const heightScale = viewportHeight / 1080;
        const minOffset = -viewportHeight * (isMobile ? 0.25 : 0.18);

        layers.forEach(layer => {
            layer.offsetPx = (layer.baseOffset + layer.lift) * heightScale;
            const layerHeight = baseWidth * layer.scale * SKYLINE_ASPECT;
            const targetTop = viewportHeight * targetTopRatio;
            const offset = Math.max(
                minOffset,
                targetTop + layerHeight - viewportHeight + (layer.lift * heightScale)
            );
            layer.el.style.setProperty('--layer-offset', `${offset}px`);
        });
    };

    updateParallaxSizing();

    if (!layers.length || prefersReducedMotion.matches) {
        return;
    }

    let ticking = false;
    let resizeRaf = null;

    const updateLayers = () => {
        const scrollY = window.scrollY || window.pageYOffset;

        layers.forEach(({ el, speed, offsetPx }) => {
            const offset = (offsetPx - scrollY * speed);
            el.style.transform = `translate3d(0, ${offset}px, 0)`;
        });

        ticking = false;
    };

    const onScroll = () => {
        if (!ticking) {
            window.requestAnimationFrame(updateLayers);
            ticking = true;
        }
    };

    const onResize = () => {
        if (resizeRaf) {
            window.cancelAnimationFrame(resizeRaf);
        }
        resizeRaf = window.requestAnimationFrame(() => {
            updateParallaxSizing();
            updateLayers();
            resizeRaf = null;
        });
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onResize, { passive: true });
    updateLayers();

    prefersReducedMotion.addEventListener('change', event => {
        if (event.matches) {
            layers.forEach(({ el }) => el.style.transform = '');
            window.removeEventListener('scroll', onScroll);
            window.removeEventListener('resize', onResize);
        } else {
            updateParallaxSizing();
            updateLayers();
            window.addEventListener('scroll', onScroll, { passive: true });
            window.addEventListener('resize', onResize, { passive: true });
        }
    });
});
