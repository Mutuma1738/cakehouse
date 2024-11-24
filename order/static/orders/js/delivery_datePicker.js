document.addEventListener('DOMContentLoaded', function () {
    flatpickr("#delivery_date", {
       
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        minDate: new Date(Date.now() + 24 * 60 * 60 * 1000), // Set minimum date to 24 hours from now
    });
});
