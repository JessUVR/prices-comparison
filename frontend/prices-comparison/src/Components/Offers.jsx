import React from "react";
import OfferGrid from "./OfferGrid";

const offers = [
  { title: "Corona Extra 6-pack", price: 89.99, discount: 15 },
  { title: "Michelob Ultra 6-pack", price: 79.99, discount: 25 },
  { title: "Modelo Extra 6-pack", price: 69.99, discount: 35 },
  { title: "Budweiser 6-pack", price: 59.99, discount: 20 },
  { title: "Heineken 6-pack", price: 99.99, discount: 10 },
  { title: "Coors Light 6-pack", price: 49.99, discount: 30 },
  { title: "Amstel Light 6-pack", price: 89.99, discount: 15 },
  { title: "Pacifico Clara 6-pack", price: 79.99, discount: 25 },
  { title: "Negra Modelo 6-pack", price: 69.99, discount: 35 },
];

function Offers() {
  return (
    <div className="px-4 pb-20">
      <div className="sticky top-0 bg-gray-100 py-4 z-10">
        <h2 className="text-2xl font-bold text-center">OFERTAS</h2>
      </div>
      <OfferGrid offers={offers} />
    </div>
  );
}

export default Offers;
