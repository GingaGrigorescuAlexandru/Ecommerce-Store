document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.add-to-cart').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            let productId = this.dataset.productId;
            let clientId = this.dataset.clientId;
            let quantity = 1; // You can update this to be dynamic if needed
            let addProductDate = new Date().toISOString().slice(0, 10);

            let data = new FormData();
            let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            data.append('csrfmiddlewaretoken', csrfToken);
            data.append('client_id', clientId);
            data.append('product_id', productId);
            data.append('quantity', quantity);
            data.append('addProductDate', addProductDate);

            const cartImage = document.getElementById(`add-to-cart-image-${productId}`)
            console.log(cartImage)
            if (cartImage) {
                cartImage.src = addedToCartSuccessfully;
            } else {
                console.error(`Cart image not found for product ID: ${productId}`);
            }

            this.style.pointerEvents = 'none';

            fetch(`/cart/${clientId}`, {
                method: 'POST',
                body: data,
            })
            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred while adding the product to the cart.");
            });

        });
    });


        document.querySelectorAll('.add-to-favorites').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            let productId = this.dataset.productId;
            let clientId = this.dataset.clientId;
            console.log(clientId)

            let data = new FormData();
            let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            data.append('csrfmiddlewaretoken', csrfToken);
            data.append('client_id', clientId);
            data.append('product_id', productId);

            const cartImage = document.getElementById(`add-to-favorites-image-${productId}`)

            if (cartImage) {
                cartImage.src = addedToFavoritesSuccessfully;
            } else {
                console.error(`Cart image not found for product ID: ${productId}`);
            }

            this.style.pointerEvents = 'none';

            fetch('/add-item-to-favorites/', {
                method: 'POST',
                body: data,
            })

            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred while adding product to the favorites list.");
            });

        });
    });
});