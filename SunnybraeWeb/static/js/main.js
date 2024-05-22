document.addEventListener("DOMContentLoaded", function(){
    
    console.log("Dom fully loaded"); //check if dom is loaded. 

    let page = 1;

    function loadMoreProducts() {
         page++;

         fetch(`?page=${page}`)
              .then((response) => {
                   // Use Fetch API to make the request
                   if (!response.ok) {
                        throw new Error("Network response was not ok " + response.statusText);
                   }
                   return response.text();
              })
              .then((data) => {
                   const parser = new DOMParser();
                   const htmlDocument = parser.parseFromString(data, "text/html");

                   const newProducts = htmlDocument.querySelectorAll(".product-item"); // Find all new product items in the response

                   const container = document.getElementById("product-container"); // Get the product container

                   newProducts.forEach((product) => container.appendChild(product)); // Add new products to the container

                   const newPageObj = htmlDocument.querySelector(".pagination"); // Find out if there are more pages of products
                   if (!newPageObj) {
                        document.getElementById("load-more").style.display = "none";
                   }
              })
              .catch((error) => { 
                console.error("There has been a problem with your fetch operation:", error); 
              });
    }

    //document.getElementById("load-more").addEventListener("click", loadMoreProducts); //wont work anymore as when run it will return null due to the script trying to find the element before it exists in the DOM

    const loadMoreBtn = document.getElementById("load-more"); //find load more button 
    if (loadMoreBtn) { //if the button is not null 
        loadMoreBtn.addEventListener("click", loadMoreProducts);
    }

});