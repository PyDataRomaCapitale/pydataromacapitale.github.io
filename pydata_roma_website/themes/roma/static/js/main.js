// custom JS here
document.addEventListener('DOMContentLoaded', function() {
    const SKYLINE_ASPECT = 317.77332 / 666.69336; // height / width of skyline SVGs
    const MOBILE_BREAKPOINT = 768;
    const MOBILE_SPEED_MULTIPLIER = 0.4;
    const root = document.documentElement;
    const parallaxBackground = document.querySelector('.parallax-background');
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const snapSections = Array.from(document.querySelectorAll('.snap-section'));
    const getScrollPadding = () => {
        const bodyStyle = getComputedStyle(document.body);
        return parseFloat(bodyStyle.scrollPaddingTop) || 0;
    };

    const layers = Array.from(document.querySelectorAll('.parallax-layer[data-speed]'))
        .map(el => ({
            el,
            baseSpeed: parseFloat(el.dataset.speed) || 0,
            speed: parseFloat(el.dataset.speed) || 0,
            baseOffset: parseFloat(el.dataset.offset) || 0,
            lift: parseFloat(el.dataset.lift) || 0,
            tail: parseFloat(el.dataset.tail) || 0,
            scale: parseFloat(getComputedStyle(el).getPropertyValue('--layer-scale')) || 1,
            offsetPx: 0
        }))
        .filter(layer => layer.speed > 0);

    const updateParallaxSizing = () => {
        const viewportWidth = window.innerWidth || root.clientWidth;
        const viewportHeight = window.innerHeight || root.clientHeight;
        const isMobile = viewportWidth <= MOBILE_BREAKPOINT;
        const containerHeight = parallaxBackground?.getBoundingClientRect().height || viewportHeight;
        const horizonRatio = parseFloat(
            getComputedStyle(parallaxBackground || root).getPropertyValue('--horizon-ratio')
        ) || 0.58;
        const horizonPosition = containerHeight * horizonRatio;

        const maxScale = layers.length
            ? layers.reduce((max, layer) => Math.max(max, layer.scale), 1)
            : 1;
        const baseWidth = viewportWidth / Math.max(1, maxScale);
        const target = parallaxBackground || root;
        target.style.setProperty('--parallax-base-width', `${baseWidth}px`);

        layers.forEach(layer => {
            layer.speed = layer.baseSpeed * (isMobile ? MOBILE_SPEED_MULTIPLIER : 1);
        });

        layers.forEach(layer => {
            const layerHeight = baseWidth * layer.scale * SKYLINE_ASPECT;
            const baseOffset = (layer.baseOffset || 0) + (layer.lift || 0);
            const tail = layer.tail * ((viewportHeight || 1) / 900);
            const offset = horizonPosition + baseOffset - containerHeight + (layerHeight / 2) + tail;
            layer.offsetPx = offset;
            layer.el.style.setProperty('--layer-offset', `${offset}px`);
        });
    };

    updateParallaxSizing();

    const parallaxEnabled = layers.length > 0 && !prefersReducedMotion.matches;
    let ticking = false;
    let resizeRaf = null;
    let snapTimer = null;
    let autoSnapping = false;
    let activeIndex = 0;
    let activeRaf = null;

    const updateLayers = () => {
        if (!parallaxEnabled) {
            ticking = false;
            return;
        }
        const scrollY = window.scrollY || window.pageYOffset;

        layers.forEach(({ el, speed, offsetPx }) => {
            const offset = (offsetPx - scrollY * speed);
            el.style.transform = `translate3d(0, ${offset}px, 0)`;
        });

        ticking = false;
    };

    const scrollToSection = (index) => {
        if (!snapSections[index]) return;
        const rect = snapSections[index].getBoundingClientRect();
        const scrollY = window.scrollY || window.pageYOffset;
        const snapPadding = getScrollPadding();
        const targetTop = Math.max(0, rect.top + scrollY - snapPadding);
        autoSnapping = true;
        window.scrollTo({ top: targetTop, behavior: 'smooth' });
        window.setTimeout(() => { autoSnapping = false; }, 520);
    };

    const snapToNearestSection = () => {
        if (!snapSections.length || prefersReducedMotion.matches) {
            return;
        }

        const viewportHeight = window.innerHeight || root.clientHeight;
        const scrollY = window.scrollY || window.pageYOffset;
        const snapPadding = getScrollPadding();
        const reference = scrollY + viewportHeight * 0.4;
        const snapDeadband = viewportHeight * 0.22;

        let closestIdx = activeIndex;
        let minDist = Infinity;

        snapSections.forEach((section, idx) => {
            const rect = section.getBoundingClientRect();
            const top = rect.top + scrollY - snapPadding;
            const dist = Math.abs(top - reference);
            if (dist < minDist) {
                minDist = dist;
                closestIdx = idx;
            }
        });

        if (!autoSnapping && minDist < snapDeadband) {
            scrollToSection(closestIdx);
        }
    };

    const scheduleSnap = () => {
        if (!snapSections.length || prefersReducedMotion.matches || autoSnapping) {
            return;
        }
        if (snapTimer) {
            window.clearTimeout(snapTimer);
        }
        snapTimer = window.setTimeout(snapToNearestSection, 260);
    };

    const onScroll = () => {
        if (parallaxEnabled && !ticking) {
            window.requestAnimationFrame(updateLayers);
            ticking = true;
        }
        scheduleSnap();
        if (!activeRaf) {
            activeRaf = window.requestAnimationFrame(updateActiveSection);
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

    const updateActiveSection = () => {
        if (!snapSections.length) {
            activeRaf = null;
            return;
        }
        const viewportHeight = window.innerHeight || root.clientHeight;
        const scrollY = window.scrollY || window.pageYOffset;
        const snapPadding = getScrollPadding();
        if (scrollY <= snapPadding + 10) {
            activeIndex = 0;
            updateSnapUI();
            activeRaf = null;
            return;
        }
        const reference = scrollY + viewportHeight * 0.1;

        let closestIdx = activeIndex;
        let minDist = Infinity;

        snapSections.forEach((section, idx) => {
            const rect = section.getBoundingClientRect();
            const top = rect.top + scrollY - snapPadding;
            const dist = Math.abs(top - reference);
            if (dist < minDist) {
                minDist = dist;
                closestIdx = idx;
            }
        });

        if (closestIdx !== activeIndex) {
            activeIndex = closestIdx;
            updateSnapUI();
        }
        activeRaf = null;
    };

    // Snap-section reveal animations
    if (snapSections.length && !prefersReducedMotion.matches) {
        const reveal = (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('snap-visible');
                } else {
                    entry.target.classList.remove('snap-visible');
                }
            });
        };
        const observer = new IntersectionObserver(reveal, {
            threshold: 0.35,
            rootMargin: '-10% 0% -20% 0%'
        });
        snapSections.forEach(sec => observer.observe(sec));
    } else {
        snapSections.forEach(sec => sec.classList.add('snap-visible'));
    }

    // Snap controls (dots only)
    const createSnapControls = () => {
        if (snapSections.length <= 1) return null;

        const control = document.createElement('div');
        control.className = 'snap-controls';

        const dotsWrap = document.createElement('div');
        dotsWrap.className = 'snap-dots';

        snapSections.forEach((section, idx) => {
            const dot = document.createElement('button');
            dot.className = 'snap-dot';
            const label = section.dataset.title || section.querySelector('h2')?.textContent || `Section ${idx + 1}`;
            dot.setAttribute('aria-label', label);
            // dot.setAttribute('title', label); // Removed to use custom CSS label
            dot.addEventListener('click', () => scrollToSection(idx));
            dotsWrap.appendChild(dot);
        });

        control.appendChild(dotsWrap);

        document.body.appendChild(control);
        return { control, dots: Array.from(dotsWrap.children) };
    };

    const updateSnapUI = () => {
        if (!snapUI) return;
        snapUI.dots.forEach((dot, idx) => {
            dot.classList.toggle('active', idx === activeIndex);
        });
    };

    const snapUI = createSnapControls();

    if (snapUI) {
        // Handle initial hash navigation
        if (window.location.hash) {
            const targetId = window.location.hash.substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                const idx = snapSections.indexOf(targetSection);
                if (idx !== -1) {
                    activeIndex = idx;
                    // Defer the scroll slightly to override browser default if needed
                    // or just let the updateActiveSection catch it.
                    // But to be safe and ensure alignment:
                    window.setTimeout(() => scrollToSection(idx), 100);
                }
            }
        } else {
            activeIndex = 0;
        }

        updateActiveSection();
        updateSnapUI();
        window.requestAnimationFrame(updateActiveSection);
    }

    // Handle scroll cue click without hash change
    const scrollCue = document.querySelector('.scroll-cue');
    if (scrollCue) {
        scrollCue.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = scrollCue.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                const idx = snapSections.indexOf(targetSection);
                if (idx !== -1) {
                    scrollToSection(idx);
                } else {
                    targetSection.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    }

    prefersReducedMotion.addEventListener('change', event => {
        if (event.matches) {
            layers.forEach(({ el }) => el.style.transform = '');
            autoSnapping = false;
            if (snapTimer) {
                window.clearTimeout(snapTimer);
            }
        } else {
            updateParallaxSizing();
            updateLayers();
        }
    });
});
