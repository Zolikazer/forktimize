console.log('Forktimize extension loaded on:', window.location.hostname);

// Listen for messages from the webpage
window.addEventListener('message', (event) => {
  // Check if extension is present
  if (event.data.type === 'FORKTIMIZE_EXTENSION_CHECK') {
    window.postMessage({type: 'FORKTIMIZE_EXTENSION_PRESENT'}, '*');
  }
  
  // Handle export button click
  if (event.data.type === 'FORKTIMIZE_EXPORT_CLICKED') {
    alert('Yo! Extension got the message! 🔥');
  }
});