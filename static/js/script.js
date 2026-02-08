//  add to cart


const products_container = document.querySelector("#products-container");

let cart_count = document.querySelector("#cart-count");
// Load current value

async function loadcartCount() {
    const countUrl = cart_count.dataset.countUrl;

    try {
        const result = await fetch(countUrl);
        const data = await result.json();
        cart_count.innerHTML = data.cart_count;
    }
    catch (error) {
        console.error(`Cart count fetch error : ${error}`)
    }
}
if (cart_count) {
    loadcartCount()
}

const csrfToken = document.querySelector('[name = csrfmiddlewaretoken]').value




// adding event listener onto product cards through their parent container
if (products_container) {
    // add to cart url
    const addUrl = products_container.dataset.addUrl;


    products_container.addEventListener('click', async function (event) {
        if (!event.target.classList.contains('add-to-cart')) {
            return;
        }
        const btn = event.target;
        const product_card = btn.closest(".product-card");
        const productId = product_card.dataset.productId;

        btn.disabled = true;

        // try to make a POST request

        try {
            const response = await fetch(addUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,

                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `product_id=${productId}`
            })
            const data = await response.json();

            // if the backend returns 401 status,

            if (response.status === 401 && data.redirect_url) {
                window.location.href = data.redirect_url;
                return;
            }
            if (data.cart_count !== undefined) {
                cart_count.innerHTML = data.cart_count;
            }
        }
        catch (error) {
            console.error(`cart error ${error}`)
        }
        finally {
            btn.disabled = false;
            btn.innerText = "Add to Cart"
        }
    });
}

// function getCookie(name){
//     let cookieValue = null;

//     if (document.cookie && document.cookie !== cookie){
//         const cookies = document.cookie.split()
//     }
// }

document.addEventListener("DOMContentLoaded", () => {

    const cartPage = document.querySelector("#cart-page");
    if (!cartPage) return;

    const plusUrl = cartPage.dataset.plusUrl;
    const minusUrl = cartPage.dataset.minusUrl;
    const removeUrl = cartPage.dataset.removeUrl;

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]")?.value;
    }

    function updateSummary(data) {
        document.querySelector("#summary-total-items").innerText = data.total_qty;
        document.querySelector("#summary-total-price").innerText = `₹${data.total_price}`;
    }

    function updateCartItemUI(cartItem, data) {
        cartItem.querySelector(".qty").innerText = data.qty;
        cartItem.querySelector(".subtotal").innerText = `₹${data.subtotal}`;
        updateSummary(data);
    }

    async function sendCartRequest(url, productId) {

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `product_id=${productId}`
        });

        return await response.json();
    }

    cartPage.addEventListener("click", async (e) => {

        const cartItem = e.target.closest(".cart-item");
        if (!cartItem) return;

        const productId = cartItem.dataset.productId;

        // PLUS
        if (e.target.classList.contains("qty-plus")) {
            const data = await sendCartRequest(plusUrl, productId);

            if (data.success) {
                updateCartItemUI(cartItem, data);
            }
        }

        // MINUS
        if (e.target.classList.contains("qty-minus")) {
            const data = await sendCartRequest(minusUrl, productId);

            if (data.success) {

                if (data.removed) {
                    cartItem.remove();
                } else {
                    updateCartItemUI(cartItem, data);
                }

                if (data.cart_empty) {
                    location.reload();
                }
            }
        }

        // REMOVE
        if (e.target.classList.contains("remove-item")) {
            const data = await sendCartRequest(removeUrl, productId);

            if (data.success) {
                cartItem.remove();
                updateSummary(data);

                if (data.cart_empty) {
                    location.reload();
                }
            }
        }

    });

});
