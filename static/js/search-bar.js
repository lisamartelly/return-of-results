'use strict';

// referenced this very closely: https://www.w3schools.com/howto/howto_js_filter_lists.asp

// search bar functionality for list pages (all studies and all participants)

function searchBar() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toUpperCase();
    const itemsList = document.getElementById("itemsList");
    const li = itemsList.getElementsByTagName('li');
  
    // Loop through list items and hide those who don't match the search query
    for (let i = 0; i < li.length; i++) {
        const a = li[i].getElementsByTagName("a")[0];
        const txtValue = a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
  }