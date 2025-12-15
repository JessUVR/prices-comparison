// App.jsx
import React, { useState, useEffect } from "react";
import StoreList from "./Components/StoreList";
import Offers from "./Components/Offers";
import ScrollToTopButton from "./Components/ScrollToTopButton";

const API_BASE_URL = `http://${window.location.hostname}:8000`;

function App() {
  const [selectedStore, setSelectedStore] = useState(null);
  const [offers, setOffers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!selectedStore) return;

    if (selectedStore.comingSoon) {
      setOffers([]);
      setError(null);
      setLoading(false);
      return;
    }

    const controller = new AbortController();

    async function fetchOffers() {
      try {
        setLoading(true);
        setError(null);

        const res = await fetch(
          `${API_BASE_URL}/offers/store/${selectedStore.slug}`,
          { signal: controller.signal }
        );

        if (!res.ok) {
          throw new Error(`Error ${res.status} loading offers`);
        }

        const data = await res.json();

        let normalizedOffers;
        if (Array.isArray(data)) {
          normalizedOffers = data;
        } else if (data && Array.isArray(data.offers)) {
          normalizedOffers = data.offers;
        } else {
          normalizedOffers = [];
        }

        setOffers(normalizedOffers);
      } catch (err) {
        if (err.name === "AbortError") return;
        setError(err.message || "Error loading offers");
        setOffers([]);
      } finally {
        setLoading(false);
      }
    }

    fetchOffers();
    return () => controller.abort();
  }, [selectedStore]);

  return (
    <div className="min-h-screen bg-[#0f141a] text-slate-50">
      {/* Barra normal de tiendas, sin sticky */}
      <header className="max-w-5xl mx-auto px-3 pt-4 pb-2">
        <StoreList
          selectedStore={selectedStore}
          onSelectStore={setSelectedStore}
        />
      </header>

      {/* Contenido principal */}
      <main className="max-w-5xl mx-auto px-3 pb-10">
        <Offers
          selectedStore={selectedStore}
          offers={offers}
          loading={loading}
          error={error}
        />
      </main>

      <ScrollToTopButton />
    </div>
  );
}

export default App;
