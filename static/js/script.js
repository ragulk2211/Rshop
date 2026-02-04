//  add to cart 


const products_container = document.querySelector("#products-container");

let cart_count = document.querySelector("#cart-count") ;
// Load current value

async function loadcartCount() {
    const countUrl = cart_count.dataset.countUrl;

    try{
        const result = await fetch(countUrl);
        const data = await result.json();
        cart_count.innerHTML.data.cart_count
    }
    catch(erroe){
        console.error(`Cart count fetch error : ${error}`)
    }
}
if (cart_count){
    loadcartCount
}

const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value


// add to cart url
const addUrl = products_container.dataset.addUrl;

// adding event listener onto product cards through their parent container

products_container.addEventListener('click', async function (event) {
    if(!event.target.classList.contains('add-to-cart')){
        return;
    }
    const btn = event.target;
    const product_card = btn.closest(".product-card");
    const productId = product_card.dataset.productId;

    btn.disabled = true;

    // try to make a POST request

    try{
        const response = await fetch(addUrl, {
            method : 'POST',
            headers : {
                'X-CSRFToken': csrfToken,
                
                "Content-Type" : "application/X-WWW-form-urlencoded"
            },
            body : `product_id=${productId}`
        })
        const data = await response.json();

        // if the backend returns 401 status,

        if (response.status === 401 && data.redirect_url){
            window.location.href = data.redirect_url;
            return;
        }
        if (data.cart_count !== undefined){
            cart_count.innerHTML = data.cart_count;
        }
    }
    catch(error){
        console.error(`cart error ${error}`)    
    }
    finally{
        btn.disabled = false;
        btn.innerText = "Add to Cart"
    }
});

// function getCookie(name){
//     let cookieValue = null;

//     if (document.cookie && document.cookie !== cookie){
//         const cookies = document.cookie.split()
//     }
// }