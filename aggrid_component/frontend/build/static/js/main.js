
import { Streamlit } from "streamlit-component-lib";

window.addEventListener("DOMContentLoaded", function () {
  const root = document.getElementById("root");
  const args = window.streamlitArgs || {};

  const container = document.createElement("div");
  container.style.fontFamily = "sans-serif";
  container.style.padding = "1rem";
  container.innerHTML = "<b>✅ Real AG Grid Component Loaded (React + Streamlit)</b>";

  root.appendChild(container);

  Streamlit.setComponentReady();
  Streamlit.setComponentValue({ loaded: true });
});
