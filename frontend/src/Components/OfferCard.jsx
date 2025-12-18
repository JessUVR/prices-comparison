// Components/OfferCard.jsx
import React from "react";

function OfferCard({ offer, onOpenDetails }) {
  return (
    <button
      type="button"
      onClick={() => onOpenDetails?.(offer)}
      className="
        text-left w-full
        bg-slate-800 
        rounded-2xl 
        p-4 
        shadow-lg 
        transition-transform 
        hover:scale-[1.02] 
        hover:shadow-xl
      "
    >
      {/* Image with uniform frame */}
      <div
        className="
          w-full
          h-52
          bg-white
          rounded-xl
          mb-4
          flex
          items-center
          justify-center
          overflow-hidden
        "
      >
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

      {/* Title */}
      <h3 className="text-slate-100 font-semibold text-sm leading-tight mb-2">
        {offer.title}
      </h3>

      {/* Price */}
      <p className="text-cyan-400 font-bold">
        {typeof offer.price === "number"
          ? `$${offer.price.toFixed(2)}`
          : `$${offer.price}`}
      </p>

      {/* Hint */}
      <p className="text-slate-400 text-xs mt-2">Click para ver detalles</p>
    </button>
  );
}

export default OfferCard;
