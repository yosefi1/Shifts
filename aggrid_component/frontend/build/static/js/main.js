
window.addEventListener("DOMContentLoaded", function () {
  const root = document.getElementById("root");
  const data = window.streamlitData.args;
  const table = document.createElement("table");
  table.style.border = "1px solid #ccc";
  table.style.width = "100%";
  table.style.textAlign = "center";

  const headerRow = document.createElement("tr");
  const cols = ["position", ...data.columns];
  cols.forEach(col => {
    const th = document.createElement("th");
    th.textContent = col;
    th.style.border = "1px solid #ccc";
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);

  data.data.forEach(row => {
    const tr = document.createElement("tr");
    cols.forEach(col => {
      const td = document.createElement("td");
      if (col === "position") {
        td.textContent = row[col];
      } else {
        const select = document.createElement("select");
        data.workers.forEach(worker => {
          const opt = document.createElement("option");
          opt.value = opt.textContent = worker;
          if (row[col] === worker) opt.selected = true;
          select.appendChild(opt);
        });
        select.onchange = () => {
          row[col] = select.value;
          window.streamlitData.setComponentValue(data.data);
        };
        td.appendChild(select);
      }
      td.style.border = "1px solid #ccc";
      tr.appendChild(td);
    });
    table.appendChild(tr);
  });

  root.innerHTML = "";
  root.appendChild(table);
});
