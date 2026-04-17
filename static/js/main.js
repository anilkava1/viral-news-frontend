document.addEventListener('DOMContentLoaded', function() {
    const newsItems = document.querySelectorAll('.clickable-news');
    newsItems.forEach(item => {
        item.style.cursor = 'pointer';
        item.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            if (url) {
                // Overlay/Timer Logic
                showTimer(url);
            }
        });
    });
});

function showTimer(url) {
    const overlay = document.createElement('div');
    overlay.style.cssText = "position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.9); z-index:10000; color:white; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;";
    overlay.innerHTML = `<h2>Loading...</h2><div style="width:300px; height:250px; background:white; margin:20px;">AD</div><p>Wait <span id="tm">5</span> sec</p>`;
    document.body.appendChild(overlay);

    let s = 5;
    const i = setInterval(() => {
        s--;
        document.getElementById('tm').innerText = s;
        if(s <= 0) {
            clearInterval(i);
            document.body.removeChild(overlay);
            window.open(url, '_blank');
        }
    }, 1000);
}