import React from "react";
import oxxoLogo from "../assets/logos/oxxo.png";
import sorianaLogo from "../assets/logos/soriana.png";
import sevenEleven from "../assets/logos/sevenEleven.png";

// StoreList.jsx
const STORES = [
  {
    id: 1,
    name: "OXXO",
    slug: "oxxo", // 👈 clave para el backend
    logo: "/img/oxxo.png",
  },
  {
    id: 2,
    name: "Soriana",
    slug: "soriana", // 👈 ya la dejas lista aunque no funcione aún
    logo: "/img/soriana.png",
  },
  // luego agregas más
];

export function StoreList({ selectedStore, onSelectStore }) {
  return (
    <div className="store-list">
      {STORES.map((store) => (
        <button
          key={store.id}
          onClick={() => onSelectStore(store.slug)}
          className={store.slug === selectedStore ? "active" : ""}
        >
          <img src={store.logo} alt={store.name} />
          <span>{store.name}</span>
        </button>
      ))}
    </div>
  );
}

export default StoreList;
