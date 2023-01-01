function setSearchDest(searchParam) {
    document.getElementById("search-trigger").setAttribute("href", `/products/search/${searchParam}`);
}