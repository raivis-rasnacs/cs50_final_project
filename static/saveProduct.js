function saveProduct() {
    var product = {};
    product["Brand"] = document.getElementById("product-brand").value;
    product["Model"] = document.getElementById("product-model").value;
    product["Description"] = document.getElementById("product-description").value;
    product["Category"] = document.getElementById("product-category").value;
    product["Price"] = document.getElementById("product-price").value;
    if (document.getElementById("product-image").files[0]) {
        product["Image_file"] = document.getElementById("product-image").files[0].name;
    }
    
    console.log(product);
    fetch("/admin/new_product",
    {
        headers : {
            'Content-Type' : 'application/json'
        },
        method: "POST",
        body : JSON.stringify({
            'productData' : product
        })
            
            //'image' : document.getElementById("product-image").files[0]
        
    })
    .then(response => response.json())
    .then(message => {
        alert(message["message"]);
    })
}