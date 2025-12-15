import { useEffect, useState, useRef } from "react";

export default function ScrollToTopButton() {
  const [visible, setVisible] = useState(false);
  const isScrollingRef = useRef(false);

  useEffect(() => {
    const handleScroll = () => {
      // si estamos auto-scrolleando, ignoramos para no parpadear o re-montar raro
      if (!isScrollingRef.current) {
        setVisible(window.scrollY > 200);
      }
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    handleScroll(); // estado inicial

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (isScrollingRef.current) return; // evitar doble ejecución

    isScrollingRef.current = true;

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });

    // después de un ratito volvemos a permitir otro scroll
    setTimeout(() => {
      isScrollingRef.current = false;
      setVisible(false); // lo escondemos al terminar
    }, 500);
  };

  if (!visible) return null; // 👈 visibilidad condicional como querías

  return (
    <button
      type="button"
      onPointerDown={scrollToTop} // 👈 más confiable que solo onClick en móvil
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
