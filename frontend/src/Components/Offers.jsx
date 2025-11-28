import React from "react";
import OfferGrid from "./OfferGrid";

const mockData = {
  OXXO: [
    { title: "Tecate Light 6-pack", price: 89.99, discount: 15 },
    { title: "Heineken 6-pack", price: 99.99, discount: 10 },
    { title: "Coors Light 6-pack", price: 49.99, discount: 30 },
    { title: "Modelo Especial 6-pack", price: 74.99, discount: 20 },
    { title: "Indio 6-pack", price: 67.5, discount: 25 },
    { title: "Corona Extra 6-pack", price: 82.99, discount: 18 },
    { title: "Bud Light 6-pack", price: 84.9, discount: 15 },
    { title: "Coors Light 6-pack", price: 79.9, discount: 20 },
    { title: "Michelob Ultra 6-pack", price: 92.5, discount: 12 },
  ],
  Soriana: [
    { title: "Modelo Especial 6-pack", price: 74.99, discount: 20 },
    { title: "Indio 6-pack", price: 67.5, discount: 25 },
    { title: "Corona Extra 6-pack", price: 82.99, discount: 18 },
    { title: "Tecate Light 6-pack", price: 89.99, discount: 15 },
    { title: "Heineken 6-pack", price: 99.99, discount: 10 },
    { title: "Coors Light 6-pack", price: 49.99, discount: 30 },
    { title: "Modelo Especial 6-pack", price: 74.99, discount: 20 },
    { title: "Bud Light 6-pack", price: 84.9, discount: 15 },
    { title: "Coors Light 6-pack", price: 79.9, discount: 20 },
    { title: "Michelob Ultra 6-pack", price: 92.5, discount: 12 },
  ],
  "7-Eleven": [
    { title: "Bud Light 6-pack", price: 84.9, discount: 15 },
    { title: "Coors Light 6-pack", price: 79.9, discount: 20 },
    { title: "Michelob Ultra 6-pack", price: 92.5, discount: 12 },
    { title: "Modelo Especial 6-pack", price: 74.99, discount: 20 },
    { title: "Indio 6-pack", price: 67.5, discount: 25 },
    { title: "Corona Extra 6-pack", price: 82.99, discount: 18 },
    { title: "Tecate Light 6-pack", price: 89.99, discount: 15 },
    { title: "Heineken 6-pack", price: 99.99, discount: 10 },
    { title: "Coors Light 6-pack", price: 49.99, discount: 30 },
    { title: "Modelo Especial 6-pack", price: 74.99, discount: 20 },
  ],
};

function Offers({ store }) {
  const offers = mockData[store];

  console.log("Selected:", store);
  console.log("Offers:", offers);

  return (
    <div className="px-4 pb-20">
      <OfferGrid offers={offers} />
    </div>
  );
}

export default Offers;
