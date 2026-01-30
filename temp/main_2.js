const API_URL = "http://localhost:8000";

// Fetch Helper
async function fetchAPI(method, endpoint, data = null, query = "") {
  console.log(`Making ${method} request to ${endpoint}${query}`, data);
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (data) options.body = JSON.stringify(data);
  try {
    const response = await fetch(`${API_URL}${endpoint}${query}`, options);
    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error response:", errorData);
      throw new Error(JSON.stringify(errorData));
    }
    const result = await response.json();
    console.log("Success response:", result);
    return result;
  } catch (error) {
    console.error("API Error:", error);
    alert("Error: " + error.message);
    return null;
  }
}

// Load Data
async function loadData() {
  const result = await fetchAPI("GET", "/cases?page=1&limit=50");
  if (!result) return;
  const tbody = document.querySelector("#dataTable tbody");
  tbody.innerHTML = "";
  result.forEach((item, index) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
            <td>${item.country}</td>
            <td class="expandable" onclick="toggleExpand(${index})">Expand</td>
            <td>
                <button onclick='openUpdateModal("${item.country}", "", "")'>Update Country</button>
                <button onclick='openDeleteModal("${item.country}", "", "")'>Delete Country</button>
            </td>
        `;
    tbody.appendChild(tr);

    // Expanded Row
    const expandTr = document.createElement("tr");
    expandTr.id = `expand-${index}`;
    expandTr.classList.add("hidden");
    const expandTd = document.createElement("td");
    expandTd.colSpan = 3;
    item.drivers.forEach((driver, dIndex) => {
      const driverDiv = document.createElement("div");
      driverDiv.classList.add("driver-header");
      driverDiv.innerHTML = `<strong>Driver: ${driver.driver}</strong>`;
      driverDiv.innerHTML += `<span><button onclick='openUpdateModal("${item.country}", "${driver.driver}", "")'>Update Driver</button><button onclick='openDeleteModal("${item.country}", "${driver.driver}", "")'>Delete Driver</button></span>`;
      const subTable = document.createElement("table");
      subTable.classList.add("sub-table");
      subTable.innerHTML =
        "<thead><tr><th>Year</th><th>tc_loss_ha</th><th>Actions</th></tr></thead><tbody>";
      driver.losses.forEach((loss, lIndex) => {
        subTable.innerHTML += `<tr id="loss-${index}-${dIndex}-${lIndex}"><td>${loss.year}</td><td>${loss.tc_loss_ha}</td><td><button onclick='openUpdateModal("${item.country}", "${driver.driver}", ${loss.year})'>Update</button><button onclick='openDeleteModal("${item.country}", "${driver.driver}", ${loss.year})'>Delete</button></td></tr>`;
      });
      subTable.innerHTML += "</tbody>";
      driverDiv.appendChild(subTable);
      expandTd.appendChild(driverDiv);
    });
    expandTr.appendChild(expandTd);
    tbody.appendChild(expandTr);
  });
}

// Toggle Expand
function toggleExpand(index) {
  document.getElementById(`expand-${index}`).classList.toggle("hidden");
}

// Sort Table
function sortTable(col) {
  const table = document.getElementById("dataTable");
  const rows = Array.from(table.rows).slice(1);
  rows.sort((a, b) =>
    a.cells[col].innerHTML.localeCompare(b.cells[col].innerHTML)
  );
  rows.forEach((row) => table.tBodies[0].appendChild(row));
}

// Add Loss Entry
function addLossEntry(containerId) {
  const container = document.getElementById(containerId);
  const entry = document.createElement("div");
  entry.classList.add("loss-entry");
  entry.innerHTML = `
        <label>Year: <input type="number" class="year" required></label>
        <label>tc_loss_ha: <input type="number" class="ha" required step="0.01"></label>
    `;
  container.appendChild(entry);
}

// Open Modals with Pre-fill
function openUpdateModal(country, driver = "", year = "") {
  document.getElementById("updateCountry").value = country;
  document.getElementById("updateDriver").value = driver;
  document.getElementById("updateYear").value = year;
  document.getElementById("updateNewHa").placeholder = year
    ? "Enter new value"
    : "Not applicable";
  openModal("update");
}

function openDeleteModal(country, driver = "", year = "") {
  document.getElementById("deleteCountry").value = country;
  document.getElementById("deleteDriver").value = driver;
  document.getElementById("deleteYear").value = year;
  openModal("delete");
}

// Open/Close Modals
function openModal(modalId) {
  document.getElementById(`${modalId}Modal`).style.display = "block";
}

function closeModal(modalId) {
  document.getElementById(`${modalId}Modal`).style.display = "none";
}

// Create Submit (No auto-refresh)
document.getElementById("createForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  console.log("Create form submitted");
  const country = document.getElementById("createCountry").value;
  const driver = document.getElementById("createDriver").value;
  const years = document.querySelectorAll(".year");
  const has = document.querySelectorAll(".ha");
  const losses = [];
  for (let i = 0; i < years.length; i++) {
    losses.push({
      year: parseInt(years[i].value),
      tc_loss_ha: parseFloat(has[i].value),
    });
  }
  const result = await fetchAPI("POST", "/cases", { country, driver, losses });
  if (result) alert(JSON.stringify(result));
  closeModal("create");
  // Removed loadData()
});

// Update Submit (No auto-refresh)
document.getElementById("updateForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  console.log("Update form submitted");
  const country = document.getElementById("updateCountry").value;
  const driver = document.getElementById("updateDriver").value;
  const year = document.getElementById("updateYear").value
    ? parseInt(document.getElementById("updateYear").value)
    : null;
  const new_ha = parseFloat(document.getElementById("updateNewHa").value);
  const new_data = year ? { tc_loss_ha: new_ha } : {};
  const result = await fetchAPI("PUT", "/cases", {
    country,
    driver,
    year,
    new_data,
  });
  if (result) alert(JSON.stringify(result));
  closeModal("update");
  // Removed loadData()
});

// Delete Submit (No auto-refresh)
document.getElementById("deleteForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  console.log("Delete form submitted");
  const country = document.getElementById("deleteCountry").value;
  const driver = document.getElementById("deleteDriver").value || "";
  const year = document.getElementById("deleteYear").value
    ? parseInt(document.getElementById("deleteYear").value)
    : "";
  const query = `?country=${country}&driver=${driver}&year=${year}`;
  const result = await fetchAPI("DELETE", "/cases" + query);
  if (result) alert(JSON.stringify(result));
  closeModal("delete");
  // Removed loadData()
});
