// Show random Galaxy tips on tool/workflow submission page

$(document).ready( () => {

  const TIPS_GITHUB_URL = "https://api.github.com/repos/usegalaxy-au/galaxy-tips/contents/tips";
  const TIPS_GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/usegalaxy-au/galaxy-tips/refs/heads/main/tips/"
  const TIPS_HEADER_IMG_URL = "https://github.com/usegalaxy-au/galaxy-tips/blob/main/static/img/header.png?raw=true";
  const TIP_HEADER = `<img class="galaxy-tips-logo" src="${TIPS_HEADER_IMG_URL}" alt="Galaxy Tips header image">`;
  const parent = document.getElementById('galaxy_tips');


  async function waitForImagesToLoad(container) {
    const images = container.querySelectorAll('img');

    const promises = Array.from(images).map(img => {
      if (img.complete) return Promise.resolve();
      return new Promise(resolve => {
        img.addEventListener('load', () => {
          console.log(`Image loaded: ${img.src}`);
          resolve();
        }, { once: true });
        img.addEventListener('error', resolve, { once: true });
      });
    });

    await Promise.all(promises);
  }


  function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  const fetchGalaxyTipsCount = fetch(TIPS_GITHUB_URL)
    .then(res => {
      if (!res.ok) throw new Error(`GitHub API error: ${res.status}`);
      return res.json();
    })
    .then(items => items.filter(i => i.type === 'file').length)
    .catch(console.error);


  fetchGalaxyTipsCount.then(count => {
    console.log(`Found ${count} Galaxy tips in GitHub remote.`);
    if (count === 0 || !parent) {
      return;
    }
    const randomIndex = getRandomInt(1, count);
    const tipUrl = `${TIPS_GITHUB_RAW_BASE_URL}/${randomIndex}.html`;

    fetch(tipUrl)
      .then(res => {
        if (!res.ok) throw new Error(`Error fetching tip: ${res.status}`);
        return res.text();
      })
      .then(tipContent => {
        parent.innerHTML = `<div class="galaxy-tip">
          ${TIP_HEADER}
          ${tipContent}
        </div>`;
      })
      .then(() => waitForImagesToLoad(parent))
      .then(() => parent.querySelector('.galaxy-tip').classList.add('loaded'))
      .catch(console.error);
  });

});
