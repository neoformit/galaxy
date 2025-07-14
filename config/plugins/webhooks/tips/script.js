// Show random Galaxy tips on tool/workflow submission page


function fetchRandomTip(count) {
  const randomIndex = Math.floor(Math.random() * count);
}


$(document).ready(function() {
  parent = document.getElementById('galaxy_tips');
  const url = '/api/webhooks/tips/count';
  const tipsCount = fetch(url)
    .then(response => response.json())
    .then(data => fetchRandomTip(data.count))
    .catch(error => {
      console.error('Error fetching tips count:', error);
    });
});
