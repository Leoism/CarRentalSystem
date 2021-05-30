window.onload = () => {
  // Displays the rating value to the user
  const output = document.getElementById('rating-val');
  const slider = document.getElementById('rating');
  output.innerText = slider.value;
  slider.oninput = () => {
    output.innerText = slider.value;
  }
}
