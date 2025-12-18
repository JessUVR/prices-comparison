// OfferModal.jsx
import React, { useEffect } from "react";

export default function OfferModal({ open, offer, onClose }) {
  // Close on ESC
  useEffect(() => {
    if (!open) return;

    const handleKeyDown = (e) => {
      if (e.key === "Escape") onClose();
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [open, onClose]);

  // Prevent background scroll when modal is open
  useEffect(() => {
    if (!open) return;

    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = originalOverflow;
    };
  }, [open]);

  // IMPORTANT: conditional return AFTER hooks
  if (!open || !offer) return null;

  const priceNumber =
    typeof offer.price === "number" ? offer.price : Number(offer.price);
  const hasValidPrice = Number.isFinite(priceNumber);
  const priceText = hasValidPrice ? `$${priceNumber.toFixed(2)}` : "—";

  const validityText = offer.validity_text
    ? offer.validity_text
    : "Sin vigencia especificada";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-3"
      role="dialog"
      aria-modal="true"
    >
      {/* Backdrop (click to close) */}
      <div
        className="absolute inset-0 bg-black/70"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal panel (limited height + internal scroll) */}
      <div
        className="relative w-[92%] max-w-2xl max-h-[85vh] overflow-hidden rounded-2xl bg-slate-900 shadow-2xl border border-slate-700"
        onClick={(e) => e.stopPropagation()} // Prevent backdrop click when clicking inside panel
      >
        {/* Header (fixed) */}
        <div className="flex items-start justify-between gap-4 p-5 border-b border-slate-700">
          <div className="min-w-0">
            <h2 className="text-slate-100 text-base font-semibold leading-snug truncate">
              {offer.title}
            </h2>
          </div>

          {/* Close button */}
          <button
            onClick={onClose}
            className="shrink-0 rounded-xl px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200"
            aria-label="Close modal"
          >
            ✕
          </button>
        </div>

        {/* Body (scrollable) */}
        <div className="p-5 grid grid-cols-1 md:grid-cols-2 gap-5 overflow-y-auto max-h-[calc(85vh-140px)]">
          {/* Image */}
          <div className="w-full h-64 bg-white rounded-xl flex items-center justify-center overflow-hidden">
            {offer.image_url ? (
              <img
                src={offer.image_url}
                alt={offer.title}
                className="max-h-full max-w-full object-contain"
              />
            ) : (
              <span className="text-slate-600 text-sm">No image</span>
            )}
          </div>

          {/* Details */}
          <div className="space-y-3">
            {/* Price card */}
            <div className="bg-slate-800/60 rounded-xl p-4 border border-slate-700">
              <p className="text-slate-400 text-xs">Price</p>
              <p className="text-cyan-400 text-3xl font-bold mt-1">
                {priceText}
              </p>
            </div>

            {/* Validity card */}
            <div className="bg-slate-800/60 rounded-xl p-4 border border-slate-700">
              <p className="text-slate-400 text-xs">Validity</p>
              <p className="text-slate-100 text-sm mt-1">{validityText}</p>
            </div>

            {/* Tip */}
            <div className="bg-slate-800/30 rounded-xl p-4 border border-slate-700">
              <p className="text-slate-300 text-sm font-semibold">Tip</p>
              <p className="text-slate-400 text-sm mt-1">
                Si estás comparando, revisa otras tiendas y decide con calma.
              </p>
            </div>
          </div>
        </div>

        {/* Footer (fixed) */}
        <div className="p-5 border-t border-slate-700 flex justify-end">
          <button
            onClick={onClose}
            className="rounded-xl px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
}
