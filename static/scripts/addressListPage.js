document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-address-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const addressItem = this.closest('.address-item');
            const inputs = addressItem.querySelectorAll('input');
            let disabled = true;
            inputs.forEach(input => {
                if (input.disabled === true) {
                    input.disabled = false;
                    disabled = false
                } else {
                    input.disabled = true;
                    disabled = true
                }
            });

            if (disabled === false) {
                this.src = confirmIcon;
            } else {
                this.src = editIcon;
            };
        });
    });
});