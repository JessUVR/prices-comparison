import React, { useState, useRef } from "react";
import StoreList from "./StoreList";
import Offers from "./Offers";

function Layout() {
  const [selectedStore, setSelectedStore] = useState("OXXO");
  const scrollRef = useRef(null);

  const handleSelectStore = (storeName) => {
    // If we already selected the same store, do nothing
    if (storeName === selectedStore) {
      return;
    }

    setSelectedStore(storeName);

    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    }
  };

  return (
    <div className="h-screen flex flex-col bg-sky-100 overflow-hidden">
      {/* Header */}
      <StoreList onSelectStore={handleSelectStore} />

      {/* Title OFERTAS – X */}
      <div className="bg-gray-100 py-4">
        <h2 className="text-2xl font-bold text-center">
          OFERTAS – {selectedStore}
        </h2>
      </div>

      {/* Only to Scroll */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto bg-gray-100">
        <Offers store={selectedStore} />
      </div>
    </div>
  );
}

export default Layout;
