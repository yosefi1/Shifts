
window.addEventListener("DOMContentLoaded", function () {
  const args = window.streamlitArgs;
  const root = document.getElementById("root");
  if (!args || !args.data || !args.columns || !args.workers) {
    root.innerHTML = "<b>Error: Missing args</b>";
    return;
  }

  const table = document.createElement("table");
  table.style.borderCollapse = "collapse";
  table.style.width = "100%";

  const header = document.createElement("tr");
  const headers = ["position", ...args.columns];
  headers.forEach(h => {
    const th = document.createElement("th");
    th.textContent = h;
    th.style.border = "1px solid #ccc";
    th.style.padding = "8px";
    header.appendChild(th);
  });
  table.appendChild(header);

  args.data.forEach((row, i) => {
    const tr = document.createElement("tr");
    headers.forEach(h => {
      const td = document.createElement("td");
      td.style.border = "1px solid #ccc";
      td.style.padding = "4px";
      if (h === "position") {
        td.textContent = row[h];
      } else {
        const sel = document.createElement("select");
        args.workers.forEach(w => {
          const opt = document.createElement("option");
          opt.value = opt.textContent = w;
          if (row[h] === w) opt.selected = true;
          sel.appendChild(opt);
        });
        sel.onchange = () => {
          args.data[i][h] = sel.value;
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
});
