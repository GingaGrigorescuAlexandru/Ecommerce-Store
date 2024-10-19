document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.cart-add-count').forEach(function(inputElement) {
        inputElement.addEventListener('change', function() {
            let productId = this.dataset.productId;  // Access product ID from data attribute
            let clientId = this.dataset.clientId;
            let quantity = this.value;
            let addProductDate = new Date().toISOString().slice(0, 10);

            let data = new FormData();
            let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            data.append('csrfmiddlewaretoken', csrfToken);
            data.append('client_id', clientId);
            data.append('product_id', productId);
            data.append('quantity', quantity);
            data.append('addProductDate', addProductDate);

            // Log for debugging
            console.log('Updating quantity for product ID:', productId);

            fetch(`/cart/${clientId}`, {
                method: 'POST',
                body: data,
            })

            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred while updating the product quantity.");
            });
        });
    });
});
