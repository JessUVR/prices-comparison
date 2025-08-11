import React from "react";
import Layout from "./Components/Layout";
import Header from "./Components/Header";
import Footer from "./Components/Footer";
import StoreList from "./Components/StoreList";
import Offers from "./Components/Offers";

function App() {
  return (
    <Layout>
      <Header />
      <StoreList />
      <Offers />
      <Footer />
    </Layout>
  );
}

export default App;
