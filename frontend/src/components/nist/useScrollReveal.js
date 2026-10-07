import { useCallback, useEffect, useRef, useState } from 'react';

/**
 * Reveals an element once it scrolls into view.
 *
 * Returns a ref to attach and an `isVisible` flag. Falls back to visible=true
 * when IntersectionObserver is unavailable (e.g. jsdom in tests) so content is
 * never permanently hidden.
 */
export function useRevealOnScroll({ threshold = 0.15, rootMargin = '0px 0px -40px 0px' } = {}) {
  const ref = useRef(null);
  // Without IntersectionObserver (e.g. jsdom) content is shown immediately so
  // it is never permanently hidden.
  const [isVisible, setIsVisible] = useState(() => typeof IntersectionObserver === 'undefined');

  useEffect(() => {
    const node = ref.current;
    if (!node || typeof IntersectionObserver === 'undefined') return undefined;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold, rootMargin }
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, [threshold, rootMargin]);

  return { ref, isVisible };
}

/**
 * Smoothly scrolls to a section by id, accounting for the sticky page header.
 */
export function useScrollToSection() {
  return useCallback((id) => {
    if (typeof document === 'undefined') return;
    const target = document.getElementById(id);
    if (!target) return;

    const headerOffset = 72;
    const top = target.getBoundingClientRect().top + window.scrollY - headerOffset;

    const prefersReducedMotion =
      typeof window.matchMedia === 'function' &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    window.scrollTo({ top, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
  }, []);
}