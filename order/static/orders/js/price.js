function updatePrice() {
    const weightSelect = document.getElementById('id_cake_size_kg');
    const selectedOption = cake_size_kgSelectSelect.options[cake_size_kgSelect.selectedIndex];
    const price = selectedOption.getAttribute('data-price');
    document.getElementById('price').innerText = `Price: ${price}`;
}
