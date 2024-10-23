document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-address-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            const addressItem = this.closest('.address-item');
            const inputs = addressItem.querySelectorAll('input:not([type="hidden"])');
            let isReadOnly = true;

            inputs.forEach(input => {
                if(input.readOnly) {
                    isReadOnly = false;
                }
            });

            if (!isReadOnly ) {
                this.src = confirmIcon;
            } else {
                inputs.forEach(input => {
                    console.log(input.readOnly)
                });
                this.src = editIcon;
                addressItem.closest("form").submit();
            };

            inputs.forEach(input => {
                input.readOnly = isReadOnly;
            });

        });
    });
});