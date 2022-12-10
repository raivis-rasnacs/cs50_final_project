function bannerFetch() {
    fetch("/",
    {
        headers : {
            'Content-Type' : 'application/json'
        },
        method: "POST",
        body : JSON.stringify( {
            'numberOfProducts' : 3
        })
    })
    .then(response => response.json())
    .then(products => {
        showProducts(products);
    })
}

function showProducts(products) {
    var banner = document.getElementById("productsBannerList");
    for (let i = 0; i < products["products"].length; i++) {
        const listItem = document.createElement("li");
        const newProduct = document.createElement("div");
        newProduct.classList.add("bannerProductDiv");
        newProduct.id = `product${i}`;
        const image = document.createElement("img");
        image.src = `/static/images/products/${products["products"][i][6]}`;
        image.classList.add("bannerProductImg");
        const name = document.createElement("h3");
        name.textContent = `${products["products"][i][1]} ${products["products"][i][2]}`;
        const oldPrice = document.createElement("h3");
        oldPrice.classList.add("oldPriceTag");
        oldPrice.textContent = `${parseFloat(products["products"][i][5] + parseFloat(20)).toFixed(2)}$`
        const newPrice = document.createElement("h3");
        newPrice.classList.add("newPriceTag");
        newPrice.textContent = `${parseFloat(products["products"][i][5].toFixed(2))}$`
        newProduct.append(image, name, oldPrice, newPrice);
        listItem.append(newProduct);
        banner.append(listItem);
    }
}

bannerFetch();