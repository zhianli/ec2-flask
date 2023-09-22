document.getElementById('generate-button').addEventListener('click', function() {
    // Generate a random number between 1 and 4
    const randomNumber = Math.floor(Math.random() * 4) + 1;
    
    // Reset all corners to their default state (not lit up)
    const corners = document.querySelectorAll('.corner');
    corners.forEach(corner => {
        corner.style.backgroundColor = 'transparent';
    });
    
    // Light up the corner based on the generated number
    const cornerToLightUp = document.getElementById(`corner${randomNumber}`);
    cornerToLightUp.style.backgroundColor = 'yellow';
});
