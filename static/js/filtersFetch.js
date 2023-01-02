// Pagination variables
var quantity;
var perPage = 12;
var pages;
var currentPage = 1;
var products;

function filtersFetch() {
    var categories = document.getElementsByClassName('category-item');
    var selectedCategories = [];
    var allCategories = [];
    
    for (var cat of categories) {
        allCategories.push(cat.name);
        if (cat.checked == true) {
            selectedCategories.push(cat.name);
        }
    }

    if (selectedCategories == 0) {
        selectedCategories = [...allCategories];
    }

    var order = document.querySelector(".sorting:checked").id;
    var highestPrice = document.getElementById("price-range").value;

    fetch("/products",
    {
        headers : {
            'Content-Type' : 'application/json'
        },
        method: "POST",
        body : JSON.stringify({
            'selectedCategories' : selectedCategories,
            'sortingOrder' : order,
            'searchParameter' : searchParameter,
            'highestPrice' : highestPrice
        })
    })
    .then(response => response.json())
    .then(fetchedProducts => {
        products = fetchedProducts;
        searchParameter = null;
        quantity = products["products"].length;
        if (quantity % perPage != 0) {
            pages = parseInt(quantity / perPage) + 1;
        }
        else {
            pages = parseInt(quantity / perPage);
        }
        renderPagination(pages);
        showProductsPerPage();
    })
}

function showProductsPerPage(page = 1, button = undefined) {
    var productsGrid = document.getElementById("productsGrid");
    while (productsGrid.children.length > 0) {
        productsGrid.children[0].remove();
    }
    
    const start = perPage * page - perPage;
    const end = perPage * page;
    if (button != undefined) {
        setCorrectColors(button);
    }

    for (let i = start; i < end; i++) {
        try {
            var productLink = document.createElement("a");
            productLink.setAttribute("href", `/products/${products["products"][i][0]}`)
            var productCard = document.createElement("div");
            productCard.classList.add("product-card", "card");
            if (products["products"][i][6] == null) {
                productCard.innerHTML = `
                <img class="card-img-top product-img" src="static/images/no-photo.jpg}" alt="">`;
            }
            else {
                productCard.innerHTML = `
                <img class="card-img-top product-img" src="/static/images/${products["products"][i][6]}" alt="">`;
            }
            productCard.innerHTML += `
            <h5 class="card-title">${products["products"][i][1]} ${products["products"][i][2]}</h5>
            <h5 class="card-text">${products["products"][i][5].toFixed(2)}$</h5>`;
            productLink.append(productCard);
            productsGrid.append(productLink);
        }
        catch {
            break;
        }
    }
}
filtersFetch();

function setCorrectColors(activatedButton) {
    const div = document.getElementById("pagination-menu");
    for (button of div.children) {
        if (button != activatedButton) {
            button.classList.add("btn-outline-primary");
            button.classList.remove("btn-primary");
            button.disabled = false;
        }
        else if (button == activatedButton) {
            button.classList.add("btn-primary");
            button.classList.remove("btn-outline-primary");
            button.disabled = true;
        }
    }
}

function renderPagination(pages) {
    const div = document.getElementById("pagination-menu");

    // Clears current pagination
    div.innerHTML = "";

    for (let i = 1; i <= pages; i++) {
        const button = `<button onclick="showProductsPerPage(this.innerHTML, this)" class="pagination-btn btn">${i}</button>`;
        div.insertAdjacentHTML("beforeend", button);
        if (i == 1) {
            div.children[i - 1].classList.add("btn-primary");
            div.children[i - 1].disabled = true;
        }
        else {
            div.children[i - 1].classList.add("btn-outline-primary");
        }
    }
}


