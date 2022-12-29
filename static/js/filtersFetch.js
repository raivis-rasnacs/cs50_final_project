function filtersFetch() {
    var categories = document.getElementsByClassName('category-item');
    var selectedCategories = [];
    var allCategories = [];
    
    for (cat of categories) {
        allCategories.push(cat.name);
        if (cat.checked == true) {
            selectedCategories.push(cat.name);
        }
    }
    
    if (selectedCategories == 0) {
        selectedCategories = [...allCategories];
    }

    fetch("/products/filter",
    {
        headers : {
            'Content-Type' : 'application/json'
        },
        method: "POST",
        body : JSON.stringify( {
            'selectedCategories' : selectedCategories
        })
    })
    .then(response => response.json())
    .then(products => {
        showFiltered(products);
    })
}

function showFiltered(products) {
    var productsGrid = document.getElementById("productsGrid");
    while (productsGrid.children.length > 0) {
        productsGrid.children[0].remove();
    }
    
    for (product of products["products"]) {
        var productLink = document.createElement("a");
        productLink.setAttribute("href", `products/${product[0]}`)
        var productCard = document.createElement("div");
        productCard.classList.add("product-card", "card");
        if (product[6] == null) {
            productCard.innerHTML = `
            <img class="card-img-top product-img" src="static/images/products/no-photo.jpg" alt="">`;
        }
        else {
            productCard.innerHTML = `
            <img class="card-img-top product-img" src="static/images/products/${product[6]}" alt="">`;
        }
        productCard.innerHTML += `
        <h5 class="card-title">${product[1]} ${product[2]}</h5>
        <h6 class="card-text">${product[5]}€</h6>`;
        productLink.append(productCard);
        productsGrid.append(productLink);
    }
}
filtersFetch();