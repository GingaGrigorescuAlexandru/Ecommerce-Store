const newsletterSuccessIcon = document.getElementById('newsletter-submit-success');

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