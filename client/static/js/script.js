function handleSearch() {
  let filterName = document.getElementById("name-input").value;
  let filterMinPoint = document.getElementById("min-point-input").value;
  let filterMaxPoint = document.getElementById("max-point-input").value;
  let filterMinYear = document.getElementById("min-year-input").value;
  let filterMaxYear = document.getElementById("max-year-input").value;

  let url = new URL(`http://127.0.0.1:8000/list_all_movies`);

  let params = {
    name: filterName,
    min_point: filterMinPoint,
    max_point: filterMaxPoint,
    min_year: filterMinYear,
    max_year: filterMaxYear,
  };

  Object.keys(params).forEach((key) => {
    if (params[key]) {
      url.searchParams.append(key, params[key]);
    }
  });

  let movieTable = document.getElementById("movie-table");
  let rows = movieTable.querySelectorAll("tr:not(#table-headings)");

  rows.forEach((row) => {
    row.remove();
  });

  fetch(url, {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      data.map((item) => {
        let movieElement = document.createElement("tr");
        let movieName = document.createElement("td");
        movieName.textContent = item.Name;
        let moviePoint = document.createElement("td");
        moviePoint.textContent = item.Point;
        let movieYear = document.createElement("td");
        movieYear.textContent = item.Year;
        let movieDuration = document.createElement("td");
        movieDuration.textContent = item.Duration;
        movieElement.appendChild(movieName);
        movieElement.appendChild(moviePoint);
        movieElement.appendChild(movieYear);
        movieElement.appendChild(movieDuration);
        movieTable.appendChild(movieElement);
      });
    });
}

let searchButton = document.getElementById("movie-search");

searchButton.addEventListener("click", handleSearch);
