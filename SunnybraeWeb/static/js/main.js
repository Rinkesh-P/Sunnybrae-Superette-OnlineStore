document.addEventListener("DOMContentLoaded", function(){
    

    document.addEventListener("click", function(event){ //For when the user clicks on the add button on the product.html page 
        if (event.target && event.target.classList.contains("add-btn")) {
            const productId = event.target.getAttribute("data-product");
            const action = 'add';
            //console.log (productId, action);  // check if add btn is workin 
            updateUserOrder(productId, action);
        }

       if (event.target && event.target.classList.contains("chg-quantity")) { //for when the user clicks on the increase/decrease arrows in the cart.html page
            const productId = event.target.getAttribute("data-product");
            const action = event.target.getAttribute("data-action");
            //console.log (productId, action);  // check if arrows are working 
            updateUserOrder(productId, action);
        }
    });

     function updateUserOrder(productId, action) { //CSRF token from the 'X-Csrftoken' HTTP header has incorrect length  
     
          // When user clicks on the add/remove buttons this function will run which will provide the updateItem function in views.py with the 
          // required information to make changes to the cart. 

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]'); // CSRF Token is already in html, but have to read in JS 
        if (!csrfToken){
            console.error("Token could not be found"); 
        }

        const url = '/updateItem/';
        fetch(url, {
             method: 'POST',
             headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrfToken.value
             },
             body: JSON.stringify({ 'productId': productId, 'action': action })
        })
             .then(response => response.json())
             .then(data => {
                  //console.log('Data:', data);
                  location.reload();
             });
     }

     document.getElementById('reset').addEventListener('click', function(){ //reset button on the product page to reset any searchs made
          window.location.href = this.getAttribute('data-url'); 
     });
     


});