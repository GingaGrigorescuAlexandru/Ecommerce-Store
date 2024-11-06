document.addEventListener("DOMContentLoaded", function () {
    const viewButtons = document.querySelectorAll(".view-products-btn");
    const modal = document.getElementById("product-modal");
    const overlay = document.getElementById("overlay");
    const closeBtn = document.getElementById("close-btn");
    const orderIdElement = document.getElementById("order-id");
    const productListElement = document.getElementById("product-list");

    const changeOrderStateButtons = document.querySelectorAll(".change-order-state-button")

    viewButtons.forEach((button) => {
        button.addEventListener("click", function () {
            // Get the order ID and product data
            const orderId = button.getAttribute("data-order-id");
            const productsJson = button.getAttribute("data-products-names");
            const quantitiesJson = button.getAttribute("data-products-quantities");
            const imagesJson = button.getAttribute("data-products-images");

            const products = JSON.parse(productsJson);
            const quantities = JSON.parse(quantitiesJson);
            const images = JSON.parse(imagesJson);

            // Set the order ID in the modal
            orderIdElement.textContent = "Order ID: " + orderId;
            productListElement.innerHTML = "";

            // Loop through each product and display details
            products.forEach((productName, index) => {
                const productElement = document.createElement("div");
                productElement.innerHTML = `
                    <div class="product-item">
                        <img class="product-image" src="https://stomagia.s3.amazonaws.com/${images[index]}" alt="${productName}" />
                        <div class="product-details">
                            <p>Product: ${productName}</p>
                            <p>Quantity: ${quantities[index]}</p>
                        </div>
                    </div>
                    <hr>
                `;
                productListElement.appendChild(productElement);
            });

            // Show the modal and overlay
            modal.style.display = "block";
            overlay.style.display = 'block';
        });
    });

    // Close the modal
    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
        overlay.style.display = 'none';
    });

    // Close the modal if clicked outside of the modal content
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
            overlay.style.display = 'none';
        }
    });

    changeOrderStateButtons.forEach((button) => {
        button.addEventListener('click', function(event) {
            const buttonText = event.target.innerText; // Get the text of the button

            if (buttonText === 'Ship') {
                order_status = 'Shipped';
            } else if (buttonText === 'Archive') {
                order_status = 'Archived';
            } else {order_status = 'Delete'};



            const orderId = button.getAttribute('data-order-id')

            const row = event.target.closest('tr'); // Get the row element of the clicked button
            const isConfirmed = confirm(`Are you sure you want to ${buttonText} this order?`);

            if(!isConfirmed) {
                return
            };

            let data = new FormData()
            let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            data.append('csrfmiddlewaretoken', csrfToken);
            data.append('order_id', orderId);
            data.append('order_status', order_status);

            fetch('/update-order-status/', {
                method: 'POST',
                body: data,
            })
            .then(response => {
                if(!response.ok) {
                    throw new Error('The response is not ok!');
                }
                return response.json();
            })
            .then(data => {
            console.log('Order status updated successfully');
            })
            .catch(error => {
                console.log('Error', error);
                alert("An error occurred while updating the order's status")
            });


            if (isConfirmed) {
                if (buttonText === 'Ship') {
                    event.target.innerText = 'Archive';
                    row.querySelectorAll('td').forEach((cell) => {
                        cell.style.backgroundColor = '#a0d468'; // Green for shipped
                        cell.style.color = 'black'; // White text for contrast
                    });
                } else if (buttonText === 'Archive') {
                    event.target.innerText = 'Delete';
                    row.querySelectorAll('td').forEach((cell) => {
                        cell.style.backgroundColor = '#ffd966'; // Yellow for archived
                        cell.style.color = 'black'; // Black text for contrast
                    });
                };

                // Update the status text in the status column (assuming it's the 9th <td>)
                row.querySelector('td:nth-child(9)').innerText = buttonText;
            } else {
                alert('Action canceled!');
            }
        });
    });

});