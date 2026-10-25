import React from "react";
import ReactDOM from "react-dom/client";
import HtmlFragment from "./components/views/HtmlFragmentsView";

async function myList(endpoint) {
  const response = await fetch(endpoint);

  if (!response.ok) {
    throw new Error("Request failed");
  }

  return response.json();
}

ReactDOM.createRoot(
  document.getElementById("root")
).render(
  <React.StrictMode>
    <HtmlFragment data={await myList("/api/query-language")}/>
  </React.StrictMode>
);