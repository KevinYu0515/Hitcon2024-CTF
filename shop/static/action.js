
const reportList = [];
const instance = axios.create({
    baseURL: 'http://ip:5000',
});

document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.item');
    cards.forEach(card => {
        card.addEventListener('click', e => {
            e.preventDefault();
            const count = card.querySelector('.item-count');
            const sell_count = card.querySelector('.item_text>span').innerHTML;
            if(count.innerHTML == sell_count) return;
            count.innerHTML = parseInt(count.innerHTML) + 1;
            count.style.display = 'block';
            if(count.innerHTML > 0){
                card.querySelector('.item_bg').classList.add('active');
                const name = card.querySelector('.item_title').innerHTML.trim();
                reportList.push(name);
            }
        })
        card.addEventListener('contextmenu', e => {
            e.preventDefault();
            const count = card.querySelector('.item-count');
            if(count.innerHTML <= 0) return;
            count.innerHTML = parseInt(count.innerHTML) - 1;
            if(count.innerHTML == 0){
                card.querySelector('.item_bg').classList.remove('active');
                count.style.display = 'none';
            }
            else {
                count.style.display = 'block';
            }
            reportList.forEach((item, index) => {
                if (reportList.indexOf(item) !== index) {
                    reportList.splice(index, 1);
                }
            });
        })
    })
})