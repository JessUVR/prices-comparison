import React from "react";
import OfferCard from "./OfferCard";

function OfferGrid({ offers }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
      {offers.map((offer, index) => (
        <OfferCard
          key={index}
          title={offer.title}
          price={offer.price}
          discount={offer.discount}
        />
      ))}
    </div>
  );
}

export default OfferGrid;
