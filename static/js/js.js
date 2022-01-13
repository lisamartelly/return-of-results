'use strict';


// function showStudies() {
//     fetch('json_studies')
//       .then(response => response.json())
//       .then(responseData =>

// inspired by: https://www.algolia.com/blog/engineering/how-to-implement-autocomplete-with-javascript-on-your-website/
            
var search_terms = ['apple', 'apple watch', 'apple macbook', 'apple macbook pro', 'iphone', 'iphone 12'];
 
function autocompleteMatch(input) {
  if (input == '') {
    return [];
  }
  var reg = new RegExp(input)
  return search_terms.filter(function(term) {
	  if (term.match(reg)) {
  	  return term;
	  }
  });
}
 
function showResults(val) {
  res = document.getElementById("result");
  res.innerHTML = '';
  let list = '';
  let terms = autocompleteMatch(val);
  for (i=0; i<terms.length; i++) {
    list += '<li>' + terms[i] + '</li>';
  }
  res.innerHTML = '<ul>' + list + '</ul>';
}


// function showStudies(val) {
//     res = document.getElementById("study");
//     res.innerHTML = '';
//     if (val == '') {
//       return;
//     }
//     let list = '';
//     fetch('/json_studies' + val)
//     .then(response => response.json())
//     .then(responseData => {
//        for (i=0; i<responseData.length; i++) {
//          list += '<li>' + responseData[i] + '</li>';
//        }
//        res.innerHTML = '<ul>' + list + '</ul>';
//        return true;
//      }).catch(function (err) {
//        console.warn('Something went wrong.', err);
//        return false;
//      });
//   }