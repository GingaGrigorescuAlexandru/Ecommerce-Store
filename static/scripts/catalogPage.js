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
                cartImage.src = addedSuccesfully;
            } else {
                console.error(`Cart image not found for product ID: ${productId}`);
            }

            this.style.pointerEvents = 'none';

            fetch(`/cart/${clientId}`, {
                method: 'POST',
                body: data,
            })
            .then(response => {
                if(response.ok) {
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
    });
});