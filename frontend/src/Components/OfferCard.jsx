import React from "react";

function OfferCard({ title, price, discount }) {
  return (
    <div className="bg-white p-4 rounded-lg shadow hover:shadow-lg hover:scale-[1.02] transition-all duration-200 text-center">
      <h3 className="text-lg font-semibold text-gray-800 mb-2">{title}</h3>
      <p className="text-2xl font-bold text-green-600 mb-1">${price}</p>
      {discount && (
        <p className="inline-block text-sm font-medium text-red-600 bg-red-100 px-3 py-1 rounded-full">
          {discount}% de descuento
        </p>
      )}
    </div>
  );
}

export default OfferCard;
