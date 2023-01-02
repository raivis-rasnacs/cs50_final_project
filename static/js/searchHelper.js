function setSearchDest(searchParam) {
    document.getElementById("search-trigger").setAttribute("action", `/products/search/${searchParam}`);
}