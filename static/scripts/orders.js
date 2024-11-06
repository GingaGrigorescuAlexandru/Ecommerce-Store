document.addEventListener("DOMContentLoaded", function () {
    const viewButtons = document.querySelectorAll(".view-products-btn");
    const modal = document.getElementById("product-modal");
    const overlay = document.getElementById("overlay");
    const closeBtn = document.getElementById("close-btn");
    const orderIdElement = document.getElementById("order-id");
    const productListElement = document.getElementById("product-list");

    viewButtons.forEach((button) => {
        button.addEventListener("click", function () {
            // Get the order ID and product data
            const orderId = button.getAttribute("data-order-id");
            const productsJson = button.getAttribute("data-products-names");
            const quantitiesJson = button.getAttribute("data-products-quantities");
            const imagesJson = button.getAttribute("data-products-images");
            console.log(imagesJson)

            const products = JSON.parse(productsJson);
            const quantities = JSON.parse(quantitiesJson);
            const images = JSON.parse(imagesJson);
            console.log(products)
            console.log(quantities)
            console.log(images)

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
});