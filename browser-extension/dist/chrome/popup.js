// Cross-browser API
const browserAPI = typeof browser !== 'undefined' ? browser : chrome;

document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('hello-btn');
  
  button.addEventListener('click', () => {
    alert('Hello from Forktimize extension!');
    console.log('Hello World button clicked');
  });
});