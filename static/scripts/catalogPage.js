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


function displayFilterList(element) {
    const headerIcon = element.querySelector('.filter-icon');

    if (element.id === "price-header") {
    const budget_bar = document.getElementById("budget-selector");

        if(budget_bar.style.display === "none") {
            budget_bar.style.display = "flex";
            headerIcon.src = minusIcon;
        } else {
            budget_bar.style.display = "none";
            headerIcon.src = plusIcon;
        }
    }

    else {
    const selectableList = element.querySelector('.selectable-list');

    if (selectableList) {
        if (selectableList.style.display === "none" || selectableList.style.display === "") {
            selectableList.style.display = "flex";
            headerIcon.src = minusIcon;
        } else {
            selectableList.style.display = "none";
            headerIcon.src = plusIcon;
        }
        event.stopPropagation();
    };
    }
};

document.getElementById('budget').addEventListener('input', function() {
    const rangeValue = document.getElementById('rangeValue');
    rangeValue.textContent = this.value;
});


document.querySelectorAll('.filter-instance input[type="checkbox"], #budget-selector input[type="range"]').forEach(filter => {
    filter.addEventListener('change', function() {
        applyFilters();
    })
})

function applyFilters() {
    let selectedProductCategories = [];
    let selectedColors = [];
    let selectedDomains = [];
    let selectedSizes = [];

    document.querySelectorAll('.filter-instance input[type="checkbox"]:checked').forEach(checkbox => {
        if(checkbox.id.startsWith("productTypes")) {
            selectedProductCategories.push(checkbox.value);
        }else if (checkbox.id.startsWith("domains")) {
            selectedDomains.push(checkbox.value);
        }else if (checkbox.id.startsWith("colors")) {
            selectedColors.push(checkbox.value);
        }else if (checkbox.id.startsWith("sizes")) {
            selectedSizes.push(checkbox.value);
        };
    });

    console.log(selectedSizes);
    console.log(selectedColors);

    let budget = document.getElementById('budget').value;

    let filterData = {
        productCategories: selectedProductCategories,
        selected_budget: budget,
        colors: selectedColors,
        domains: selectedDomains,
        sizes: selectedSizes,
    };

    fetch('/filter-catalog-products/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrf-token').content,
        },
        body: JSON.stringify(filterData),
    })

    .then(response => response.json())

    .then(data => {
        document.querySelector('.catalog-container').innerHTML = data.html;
    })
    .catch(error => console.error('Error:', error));
};


document.getElementById('budget').addEventListener('input', function() {
    const value = this.value; // 'this' refers to the input element now
    const min = this.min ? this.min : 0;
    const max = this.max ? this.max : 100;
    const percentage = ((value - min) / (max - min)) * 100;

    // Set the background as a linear gradient based on the current value
    this.style.background = `linear-gradient(90deg, #D484E2 ${percentage}%, transparent ${percentage}%)`;
});