// Components/OfferGrid.jsx
import React from "react";
import OfferCard from "./OfferCard";

export default function OfferGrid({ offers = [], onOpenDetails }) {
  return (
    <div className="offer-grid">
      {/* Render offer cards */}
      {offers.map((offer) => (
        <OfferCard key={offer.id} offer={offer} onOpenDetails={onOpenDetails} />
      ))}
    </div>
  );
}
