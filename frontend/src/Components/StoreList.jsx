import React from "react";
import oxxoLogo from "../assets/logos/oxxo.png";
import sorianaLogo from "../assets/logos/soriana.png";
import sevenEleven from "../assets/logos/sevenEleven.png";

const stores = [
  { name: "OXXO", logo: oxxoLogo },
  { name: "Soriana", logo: sorianaLogo },
  { name: "7-Eleven", logo: sevenEleven },
];

function StoreList() {
  return (
    <div className="pt-20 py-6 text-center bg-sky-100">
      <h2 className="text-xl font-semibold text-gray-800 text-center mt-10 mb-2">
        CERVEZAS DISPONIBLES 🍻
      </h2>

      <div className="bg-white rounded-xl shadow-sm p-4 max-w-3xl mx-auto flex flex-wrap justify-center gap-6">
        {stores.map((store, index) => (
          <div
            key={index}
            className="w-20 h-20 flex items-center justify-center"
          >
            <img
              src={store.logo}
              alt={store.name}
              className="w-full h-full object-contain"
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default StoreList;
