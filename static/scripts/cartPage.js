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

document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.eliminate-product-from-cart-button').forEach(button => {
            button.addEventListener('click', function() {
                let productId = this.dataset.productId;  // Access product ID from data attribute
                let clientId = this.dataset.clientId;

                let data = new FormData();
                let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
                data.append('csrfmiddlewaretoken', csrfToken);
                data.append('client_id', clientId);
                data.append('product_id', productId);

                fetch('/delete-from-cart/', {
                method: 'POST',
                body: data,
                })

                .then(response => response.json())
                .then(data => {
                    if (data.message === 'Item successfully deleted') {
                        window.location.reload();
                    }
                    else {
                        alert('Error' + data.message)
                    }
                })

                .catch(error => {
                    console.error('Error:', error);
                    alert("An error occurred while deleting the product from the cart.");
                })
            });
        });
    });