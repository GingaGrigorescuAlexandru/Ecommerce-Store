const newsletterSuccessIcon = document.getElementById('newsletter-submit-success');

const button = document.getElementById('updated_info_submit_button');

button.addEventListener('click', function(event) {
    event.preventDefault();

    const form = document.querySelector('.update-user-info');
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData(form);

    if(this.innerText === 'Update'){
        this.style.backgroundColor = 'white';
        this.style.color = 'black';
        this.style.border = '2px solid black';
        this.innerText = 'Save';
        this.style.boxSizing = 'border-box';
        form.querySelectorAll('input').forEach(function(input) {
            input.disabled = false;
        });

    } else {
        this.style.backgroundColor = 'black';
        this.style.color = 'white';
        this.style.border = 'none';
        this.innerText = 'Update';

        form.querySelectorAll('input').forEach(function(input) {
            input.disabled = true;
        });
        fetch('/update-user/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })

        .then(data => {
            console.log('Success:', data);
            form.querySelectorAll('input').forEach(function(input) {
                input.disabled = true;
            });
        })

        .catch(error => {
            console.error('Error:', error);
        });

        }
    console.log("Hello");
});



button.addEventListener('mouseenter', function() {
    if(this.innerText === 'Save') {
        this.style.border = '2px solid #D484E2';
    };
});

button.addEventListener('mouseleave', function() {
    if(this.innerText === 'Save') {
        this.style.border = '2px solid black';
    };
});


document.querySelector('.newsletter-form').addEventListener('submit', async function(event) {
    event.preventDefault();


    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const emailInput = document.querySelector('input[name="newsletter-email-input"]').value;
    const url = this.getAttribute('data-url');

    const data = {
        'client_id_input':  logged_user,
        'newsletter-email-input': emailInput
    };
    console.log("HERE5")
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const jsonResponse = await response.json();
            this.style.display = "none";
            newsletterSuccessIcon.style.display = "flex";
        } else {
            console.error('Error:', response.statusText);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
});