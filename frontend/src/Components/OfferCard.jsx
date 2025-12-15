// OfferCard.jsx
import React from "react";

function OfferCard({ offer }) {
  return (
    <div
      className="
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
          h-52              /* uniform frame size */
          bg-white
          rounded-xl
          mb-4
          flex
          items-center
          justify-center
          overflow-hidden
        "
      >
        <img
          src={offer.image_url}
          alt={offer.title}
          className="max-h-full max-w-full object-contain"
        />
      </div>

      {/* Title */}
      <h3 className="text-slate-100 font-semibold text-sm leading-tight mb-2">
        {offer.title}
      </h3>

      {/* Price */}
      <p className="text-cyan-400 font-bold text-lg">${offer.price}.00</p>
    </div>
  );
}

export default OfferCard;
