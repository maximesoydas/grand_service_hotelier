  var initialView = [48.5734053, 7.7521113]; // Strasbourg coordinates
  var initialZoom = 13;
  var map;
  var addressMap = {};
  var currentIntervention;

  document.addEventListener("DOMContentLoaded", function () {
    map = L.map("map").setView(initialView, initialZoom);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    fetchInterventions();
  });

  function fetchInterventions() {
    fetch("/api/interventions/")
      .then((response) => response.json())
      .then((interventions) => {
        var tbody = document.getElementById("interventions-body");
        tbody.innerHTML = ""; // Clear existing content

        interventions.forEach(function (intervention) {
          if (intervention.latitude && intervention.longitude) {
            var address = intervention.Adresse;
            if (!addressMap[address]) {
              addressMap[address] = [];
            }
            addressMap[address].push(intervention);

            var row = `
                <tr class="hover:bg-gray-100 cursor-pointer" onclick="showModal('${address}')">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${intervention.Adresse}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${intervention["Type d'intervention"]}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${intervention["Précision de l'intervention"]}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${intervention["Statut de l'intervention"]}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${intervention["Date de l'intervention"]}</td>
                </tr>
              `;
            tbody.insertAdjacentHTML("beforeend", row);
          }
        });

        for (var address in addressMap) {
          (function (addr) {
            var lat = addressMap[addr][0].latitude;
            var lng = addressMap[addr][0].longitude;

            var marker = L.marker([lat, lng]).addTo(map);
            marker.bindPopup(`<b>${addr}</b>`);
            marker.on("click", function () {
              showModal(addr);
            });
          })(address);
        }

        // Hide the loading indicator after data is loaded
        document.getElementById("loading-indicator").style.display = "none";
      })
      .catch((error) => {
        console.error("Error fetching interventions:", error);
        // Hide the loading indicator in case of error
        document.getElementById("loading-indicator").style.display = "none";
      });
  }

  function showModal(address) {
    var interventionsForAddress = addressMap[address];
    var modalContent = "";

    interventionsForAddress.forEach(function (intervention, index) {
      modalContent += `
          <div class="intervention-item mb-4">
            <p><strong>Intervention ${index + 1}</strong></p>
            <p>${intervention["Adresse"]}</p>
            <p>Type d'intervention: ${intervention["Type d'intervention"]}</p>
            <p>Précision de l'intervention: ${
              intervention["Précision de l'intervention"]
            }</p>
            <p>Statut de l'intervention: ${
              intervention["Statut de l'intervention"]
            }</p>
            <p>Date de l'intervention: ${
              intervention["Date de l'intervention"]
            }</p>
            <button class="mt-2 white-black-border-animated inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500" onclick="selectIntervention(${index}, '${address}')">Sélectionner cette intervention</button>
            <button class="mt-2 white-black-border-animated inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500" onclick="deleteIntervention(${index}, '${address}')">Supprimer cette intervention</button>
          </div>
          <hr/>
        `;
    });

    document.getElementById("modal-content").innerHTML = modalContent;
    document.getElementById("modal-selection").classList.remove("hidden");
    document.getElementById("modal-update").classList.add("hidden");
    document.getElementById("intervention-modal").classList.remove("hidden");
  }

  function selectIntervention(index, address) {
    var intervention = addressMap[address][index];
    currentIntervention = intervention;

    document.getElementById("modal-address-update").textContent =
      intervention.Adresse;
    document.getElementById("modal-type").textContent =
      intervention["Type d'intervention"];
    document.getElementById("modal-precision").textContent =
      intervention["Précision de l'intervention"];
    document.getElementById("modal-status").value =
      intervention["Statut de l'intervention"];

    document.getElementById("modal-selection").classList.add("hidden");
    document.getElementById("modal-update").classList.remove("hidden");
  }

  function closeModal() {
    document.getElementById("intervention-modal").classList.add("hidden");
  }

  function updateStatus() {
    var newStatus = document.getElementById("modal-status").value;
    fetch("/api/update_intervention_status/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        Adresse: currentIntervention.Adresse,
        "Type d'intervention": currentIntervention["Type d'intervention"],
        "Précision de l'intervention":
          currentIntervention["Précision de l'intervention"],
        "Date de l'intervention": currentIntervention["Date de l'intervention"],
        "Statut de l'intervention": newStatus,
      }),
    })
      .then((response) => {
        if (response.ok) {
          window.location.href = "/interventions";
        } else {
          console.error("Failed to update status:", response.statusText);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  function deleteIntervention(index, address) {
    var intervention = addressMap[address][index];
    fetch("/api/delete_intervention/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        Adresse: intervention.Adresse,
        "Type d'intervention": intervention["Type d'intervention"],
        "Précision de l'intervention":
          intervention["Précision de l'intervention"],
        "Date de l'intervention": intervention["Date de l'intervention"],
      }),
    })
      .then((response) => {
        if (response.ok) {
          window.location.href = "/interventions";
        } else {
          console.error("Failed to delete intervention:", response.statusText);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  function openAddInterventionModal() {
    document
      .getElementById("add-intervention-modal")
      .classList.remove("hidden");
  }

  function closeAddInterventionModal() {
    document.getElementById("add-intervention-modal").classList.add("hidden");
  }

  function addIntervention() {
    var form = document.getElementById("add-intervention-form");
    var formData = new FormData(form);
    var data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    const date = data["Date_de_l_intervention"];
    const time = data["Heure_de_l_intervention"];
    data["Date de l'intervention"] = `${date} ${time}:00`;

    fetch("/api/add_intervention/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (response.ok) {
          window.location.href = "/interventions";
        } else {
          console.error("Failed to add intervention:", response.statusText);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  function resetMapView() {
    map.setView(initialView, initialZoom);
  }

  function sortTable(columnIndex) {
    var table = document.getElementById("interventions-table");
    var tbody = table.tBodies[0];
    var rows = Array.from(tbody.rows);
    var isNumericColumn =
      !isNaN(Date.parse(rows[0].cells[columnIndex].textContent)) ||
      !isNaN(rows[0].cells[columnIndex].textContent);

    rows.sort(function (a, b) {
      var cellA = a.cells[columnIndex].textContent.trim();
      var cellB = b.cells[columnIndex].textContent.trim();

      if (isNumericColumn) {
        if (!isNaN(Date.parse(cellA))) {
          // Compare dates
          return new Date(cellA) - new Date(cellB);
        }
        // Compare numeric values
        return cellA - cellB;
      } else {
        return cellA.localeCompare(cellB);
      }
    });

    rows.forEach(function (row) {
      tbody.appendChild(row);
    });
  }

document.addEventListener("DOMContentLoaded", function () {
  flatpickr("#Date_de_l_intervention", {
    dateFormat: "Y-m-d"
  });

  flatpickr("#Heure_de_l_intervention", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true
  });
});
