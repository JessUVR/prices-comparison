import React from "react";

function Layout({ children }) {
  return (
    <div className="h-screen flex flex-col overflow-hidden">
      <div className="shrink-0">{children[0]}</div>
      <div className="shrink-0">{children[1]}</div>
      <div className="flex-1 overflow-y-auto">{children[2]}</div>
      <div className="shrink-0">{children[3]}</div>
    </div>
  );
}

export default Layout;
