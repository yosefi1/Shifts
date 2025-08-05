
const Streamlit = window.Streamlit;

function renderDropdownComponent(args) {
  const root = document.getElementById("root");
  if (!args || !args.data || !args.columns || !args.workers) {
    root.innerHTML = "<b>Error loading dropdown component</b>";
    return;
  }

  const table = document.createElement("table");
  table.style.borderCollapse = "collapse";
  table.style.width = "100%";

  const headers = ["position", ...args.columns];
  const headerRow = document.createElement("tr");
  headers.forEach(h => {
    const th = document.createElement("th");
    th.textContent = h;
    th.style.border = "1px solid #ccc";
    th.style.padding = "6px";
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);

  args.data.forEach((row, rowIndex) => {
    const tr = document.createElement("tr");
    headers.forEach(h => {
      const td = document.createElement("td");
      td.style.border = "1px solid #ccc";
      td.style.padding = "4px";

      if (h === "position") {
        td.textContent = row[h];
      } else {
        const sel = document.createElement("select");
        args.workers.forEach(worker => {
          const opt = document.createElement("option");
          opt.value = opt.textContent = worker;
          if (row[h] === worker) opt.selected = true;
          sel.appendChild(opt);
        });
        sel.onchange = () => {
          args.data[rowIndex][h] = sel.value;
          Streamlit.setComponentValue(args.data);
        };
        td.appendChild(sel);
      }

      tr.appendChild(td);
    });
    table.appendChild(tr);
  });

  root.innerHTML = "";
  root.appendChild(table);
  Streamlit.setComponentReady();
  Streamlit.setComponentValue(args.data);
}

window.onload = () => {
  Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, (event) => {
    renderDropdownComponent(event.detail.args);
  });
  Streamlit.setComponentReady();
};
