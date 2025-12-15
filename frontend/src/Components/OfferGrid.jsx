// Components/OfferGrid.jsx
import React from "react";
import OfferCard from "./OfferCard";

function OfferGrid({ offers }) {
  if (!Array.isArray(offers) || offers.length === 0) {
    return null;
  }

  // quitamos null/undefined por si acaso
  const safeOffers = offers.filter(Boolean);
  console.log("[OfferGrid] safeOffers:", safeOffers);

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
      {safeOffers.map((o) => (
        <OfferCard key={o.id} offer={o} />
      ))}
    </div>
  );
}

export default OfferGrid;
