document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-to-cart').addEventListener('click', function() {
        const quantityCounter = document.getElementById('add_quantity');

        let productId = this.dataset.productId;
        let clientId = this.dataset.clientId;
        let quantity = quantityCounter.value;
        let addProductDate = new Date().toISOString().slice(0, 10);

        let data = new FormData();
        let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        data.append('csrfmiddlewaretoken', csrfToken);
        data.append('client_id', clientId);
        data.append('product_id', productId);
        data.append('quantity', quantity);
        data.append('addProductDate', addProductDate);

        fetch(`/cart/${clientId}`, {
            method: 'POST',
            body: data,
        })
        .then(response => {
            if (response.ok) {
                alert("Product added to cart!");
            } else {
                alert("Failed to add product to cart!");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while adding the product to the cart.");
        });
    });

    document.getElementById('add-to-favorites').addEventListener('click', function() {
        let productId = this.dataset.productId;
        let clientId = this.dataset.clientId;

        let data = new FormData();
        let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        data.append('csrfmiddlewaretoken', csrfToken);
        data.append('client_id', clientId);
        data.append('product_id', productId);

        const cartImage = document.getElementById(`add-to-favorites-image-${productId}`)


        fetch('/add-item-to-favorites/', {
            method: 'POST',
            body: data,
        })
        .then(response => {
            if (response.ok) {
                cartImage.src = addedToFavoritesSuccessfully;
                this.style.borderColor = "#D484E2";
                 removeTextNodes(this);
                 this.disabled = true;
                alert("Product added to favorites!");
            } else {
                alert("Failed to add product to favorites!");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while adding the product to favorites.");
        });
    });
});

function removeTextNodes(button) {
    button.childNodes.forEach((node) => {
        if (node.nodeType === Node.TEXT_NODE) {
            node.remove();
        }
    });
}

document.querySelector('.add-review-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const nrStars = document.querySelector('input[type="number"]').value;
    const reviewBody = document.querySelector('textarea[name="input_review"]').value;

    const data = {
        'input_review':  reviewBody,
        'nr_of_stars': nrStars
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data),
    })

    .then(response => {
        if (response.ok) {
            alert("Added Review!");
        } else {
            alert("Failed to add review!");
        }
    })

    .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while adding the product to the cart.");
        });
});