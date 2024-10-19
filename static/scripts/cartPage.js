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


document.querySelectorAll('.cart-add-count').forEach(input => {
    input.addEventListener('change', function() {

        const quantity = parseInt(this.value);
        const pricePerUnit = parseFloat(this.closest('.cart-item-container').dataset.price);
        const itemTotalPriceElement = this.closest('.cart-item-container').querySelector('.item-total-price');

        const subtotalElement = document.getElementById('subtotal');
        const totalElement = document.getElementById('total');

        // Update the item total price
        const itemTotalPrice = quantity * pricePerUnit;
        itemTotalPriceElement.textContent = itemTotalPrice.toFixed(2) + ' RON';

        // Calculate new subtotal
        let newSubtotal = 0;
        document.querySelectorAll('.item-total-price').forEach(totalPriceElement => {
            newSubtotal += parseFloat(totalPriceElement.textContent);
        });
        subtotalElement.textContent = newSubtotal.toFixed(2) + ' RON';
        totalElement.textContent = newSubtotal.toFixed(2) + ' RON'; // Adjust if you have shipping fees etc.
    });
});