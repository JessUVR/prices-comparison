import { useEffect, useState, useRef } from "react";

export default function ScrollToTopButton() {
  const [visible, setVisible] = useState(false);
  const isScrollingRef = useRef(false);

  useEffect(() => {
    const handleScroll = () => {
      // if we are auto-scrolling, ignore to avoid flickering or weird remounting
      if (!isScrollingRef.current) {
        setVisible(window.scrollY > 200);
      }
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll(); // initial state

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (isScrollingRef.current) return; // avoid double scrolls

    isScrollingRef.current = true;

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });

    // after a short delay we allow scrolling again
    setTimeout(() => {
      isScrollingRef.current = false;
      setVisible(false); // lo escondemos al terminar
    }, 500);
  };

  if (!visible) return null; // conditional visibility

  return (
    <button
      type="button"
      onPointerDown={scrollToTop}
      className="
        fixed bottom-5 right-5 z-50
        flex items-center justify-center
        w-14 h-14
        rounded-full shadow-xl
        bg-slate-900 text-white
        hover:bg-slate-800 active:scale-95
        transition-transform transition-colors
      "
      aria-label="Volver arriba"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        className="w-6 h-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth="2"
      >
        <path strokeLinecap="round" strokeLinejoin="round" d="M5 15l7-7 7 7" />
      </svg>
    </button>
  );
}
