// Components/Offers.jsx
import React, { useState, useMemo } from "react";
import OfferGrid from "./OfferGrid";
import OfferModal from "./OfferModal";

function Offers({ selectedStore, offers, loading, error }) {
  // Sorting option: 'none' | 'asc' | 'desc'
  const [sortOrder, setSortOrder] = useState("none");

  // Modal state
  const [selectedOffer, setSelectedOffer] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Open modal with offer details
  const openDetails = (offer) => {
    setSelectedOffer(offer);
    setIsModalOpen(true);
  };

  // Close modal
  const closeDetails = () => {
    setIsModalOpen(false);
    setSelectedOffer(null);
  };

  const title = selectedStore ? `OFERTAS – ${selectedStore.name}` : "OFERTAS";
  const isComingSoon = selectedStore?.comingSoon;

  // Compute the final list of offers to display (sorted copy of original)
  const displayedOffers = useMemo(() => {
    if (!offers || !Array.isArray(offers)) return [];

    // Work with a copy so original data stays untouched
    const copy = [...offers];

    // Sort by ascending price
    if (sortOrder === "asc") {
      copy.sort((a, b) => {
        const pa = Number(a.price ?? Infinity);
        const pb = Number(b.price ?? Infinity);
        return pa - pb;
      });
    }
    // Sort by descending price
    else if (sortOrder === "desc") {
      copy.sort((a, b) => {
        const pa = Number(a.price ?? -Infinity);
        const pb = Number(b.price ?? -Infinity);
        return pb - pa;
      });
    }

    return copy;
  }, [offers, sortOrder]);

  const hasOffers = displayedOffers?.length > 0;

  return (
    <section className="offers-section">
      {/* Section title */}
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
          Offers for <span className="font-semibold">{selectedStore.name}</span>{" "}
          will be available soon 🚧
        </p>
      )}

      {/* Loading state */}
      {selectedStore && !isComingSoon && loading && (
        <div className="flex flex-col items-center justify-center mt-6 mb-6">
          <div className="loader"></div>
          <p className="text-slate-400 text-xs mt-3 tracking-wide">
            Loading offers for{" "}
            <span className="text-slate-200">{selectedStore.name}</span>…
          </p>
        </div>
      )}

      {/* Error state */}
      {selectedStore && !isComingSoon && !loading && error && (
        <p className="text-red-400 text-sm mt-4">
          There was an error while loading the offers. Please try again later.
        </p>
      )}

      {/* No offers found */}
      {selectedStore && !isComingSoon && !loading && !error && !hasOffers && (
        <p className="text-slate-400 text-sm mt-4">
          No active offers were found for this store.
        </p>
      )}

      {/* Sorting controls (shown only when offers exist) */}
      {selectedStore && !isComingSoon && !loading && !error && hasOffers && (
        <div className="flex justify-between items-center mb-4 text-xs text-slate-400">
          {/* Left side: offers count */}
          <p>
            Showing{" "}
            <span className="text-slate-200 font-semibold">
              {displayedOffers.length}
            </span>{" "}
            offers from{" "}
            <span className="text-slate-200 font-semibold">
              {selectedStore.name}
            </span>
          </p>

          {/* Right side: sorting buttons */}
          <div className="flex items-center gap-2">
            <span className="hidden sm:inline">Sort by:</span>

            {/* Ascending button */}
            <button
              className={`px-2 py-1 rounded-full border text-[0.7rem] ${
                sortOrder === "asc"
                  ? "border-cyan-400 text-cyan-400 bg-cyan-400/10"
                  : "border-slate-600 text-slate-300 hover:border-slate-400"
              }`}
              onClick={() => setSortOrder("asc")}
            >
              Price ↑
            </button>

            {/* Descending button */}
            <button
              className={`px-2 py-1 rounded-full border text-[0.7rem] ${
                sortOrder === "desc"
                  ? "border-cyan-400 text-cyan-400 bg-cyan-400/10"
                  : "border-slate-600 text-slate-300 hover:border-slate-400"
              }`}
              onClick={() => setSortOrder("desc")}
            >
              Price ↓
            </button>

            {/* Reset button */}
            <button
              className={`px-2 py-1 rounded-full border text-[0.7rem] ${
                sortOrder === "none"
                  ? "border-slate-500 text-slate-300"
                  : "border-slate-600 text-slate-500 hover:border-slate-400"
              }`}
              onClick={() => setSortOrder("none")}
            >
              Reset
            </button>
          </div>
        </div>
      )}

      {/* Render the offer grid (sorted list) */}
      {selectedStore && !isComingSoon && !loading && !error && hasOffers && (
        <OfferGrid offers={displayedOffers} onOpenDetails={openDetails} />
      )}

      {/* Details modal */}
      <OfferModal
        open={isModalOpen}
        offer={selectedOffer}
        onClose={closeDetails}
      />
    </section>
  );
}

export default Offers;
