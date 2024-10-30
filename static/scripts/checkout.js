// This is your test secret API key.
        const stripe = Stripe("pk_test_51Q3j8SCHn57WARm8fMDgKE1yaOuhrq0IyrZm3adm8rDwDwhvEhDHnkb8iLcCHOUKm9OCwoeOaAYh4M3fJsKUlw5h00gj5ElymB");

        initialize();
        console.log("HELLLLLLLLLLLLLLLLLLLLLLLLLOOOOOOOOOOOOOOO")
        // Create a Checkout Session
        async function initialize() {
          const fetchClientSecret = async () => {
            const response = await fetch("/create-checkout-session/", {
              method: "POST",
            });
            const { clientSecret } = await response.json();
            console.log(clientSecret)
            return clientSecret;
          };

          const checkout = await stripe.initEmbeddedCheckout({
            fetchClientSecret,
          });

          // Mount Checkout
          checkout.mount('#checkout');
        }