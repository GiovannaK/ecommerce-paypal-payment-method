(function () {
    select_variation = document.getElementById('select-variations');
    variation_price = document.getElementById('variation-price');

    if (!select_variation) {
        return;
    }

    if (!variation_price) {
        return;
    }

    select_variation.addEventListener('change', function () {
        price = this.options[this.selectedIndex].getAttribute('data-price');

        variation_price.innerHTML = price;
    })
})();
