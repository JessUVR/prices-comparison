// StoreList.jsx
import React from "react";
import oxxoLogo from "../assets/logos/oxxo.png";
import sorianaLogo from "../assets/logos/soriana.png";
import sevenElevenLogo from "../assets/logos/sevenEleven.png";

const STORES = [
  { id: 1, slug: "oxxo", name: "OXXO", comingSoon: false },
  { id: 2, slug: "soriana", name: "Soriana", comingSoon: true },
  { id: 3, slug: "7eleven", name: "7-Eleven", comingSoon: true },
  { id: 4, slug: "merco", name: "Merco", comingSoon: false },
];

function StoreList({ selectedStore, onSelectStore }) {
  return (
    <div className="store-list">
      {STORES.map((store) => {
        const isActive = selectedStore?.slug === store.slug;

        return (
          <button
            key={store.id}
            onClick={() => {
              if (isActive) return; // ⛔ avoids reloading the same store
              onSelectStore(store);

              // 🔄 Reset scroll to top
              window.scrollTo({ top: 0, behavior: "smooth" });
            }}
            className={`store-item ${isActive ? "store-item--active" : ""}`}
          >
            {store.name}
            {store.comingSoon && " (coming soon)"}
          </button>
        );
      })}
    </div>
  );
}

export default StoreList;
