// Components/Offers.jsx
import React from "react";
import OfferGrid from "./OfferGrid";

function Offers({ selectedStore, offers, loading, error }) {
  const title = selectedStore ? `OFFERS – ${selectedStore.name}` : "OFFERS";

  const isComingSoon = selectedStore?.comingSoon;

  return (
    <section className="offers-section">
      {/* Section Title */}
      <h2 className="offers-title">{title}</h2>

      {/* No store selected */}
      {!selectedStore && (
        <p className="text-slate-400 text-sm mt-4">
          Select a store to view offers.
        </p>
      )}

      {/* Store marked as "coming soon" */}
      {selectedStore && isComingSoon && (
        <p className="text-slate-400 text-sm mt-4">
          Offers for{" "}
          <span className="font-semibold">{selectedStore.name}</span> will be
          available soon 🚧
        </p>
      )}

      {/* Loading */}
      {selectedStore && !isComingSoon && loading && (
        <div className="flex flex-col items-center justify-center mt-6 mb-6">
          <div className="loader"></div>
          <p className="text-slate-400 text-xs mt-3 tracking-wide">
            Loading offers for{" "}
            <span className="text-slate-200">{selectedStore.name}</span>…
          </p>
        </div>
      )}

      {/* Error */}
      {selectedStore && !isComingSoon && !loading && error && (
        <p className="text-red-400 text-sm mt-4">
          There was a problem loading offers. Please try again later.
        </p>
      )}

      {/* No offers */}
      {selectedStore &&
        !isComingSoon &&
        !loading &&
        !error &&
        (!offers || offers.length === 0) && (
          <p className="text-slate-400 text-sm mt-4">
            We found no active offers for this store at the moment.
          </p>
        )}

      {/* Offers Grid */}
      {selectedStore &&
        !isComingSoon &&
        !loading &&
        !error &&
        offers &&
        offers.length > 0 && <OfferGrid offers={offers} />}
    </section>
  );
}

export default Offers;
