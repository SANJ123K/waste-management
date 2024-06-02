document.addEventListener("DOMContentLoaded", function() {
    fetchData();
});

function fetchData() {
    const itemId = document.getElementById('item-id').value;

    fetch(`/data/${itemId}`)
        .then(response => response.json())
        .then(data => {
            let level = data.level;

            // Calculate the percentage based on the level
            const percentage = (Math.abs((18 - level) * (100 / 18)))%100;

            const circle = document.querySelector('.circle');
            const circleLevel = document.getElementById('circle-level');

            // Adjust the conic gradient based on the calculated percentage
            circle.style.background = `conic-gradient(#4caf50 0% ${percentage}%, #ddd ${percentage}% 100%)`;

            // Adjust the displayed percentage
            circleLevel.textContent = `${percentage.toFixed(2)}%`;
        })
        .catch(error => console.error('Error fetching data:', error));
}
