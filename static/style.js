function toggle(element) {
    console.log('toggle')
    element.classList.toggle('open');
    let content = document.querySelector('#navl').innerHTML;
    let mobileContent = document.querySelector('#mobile-nav');
    if (mobileContent.innerHTML === content) {
        mobileContent.innerHTML = '';
    } else {
        mobileContent.innerHTML = content;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const night = document.querySelector('.night');
    night.addEventListener('click', function() {
        document.body.classList.toggle('dark');
        if (night.innerHTML == 'Noc') {
            night.innerHTML = 'Dzień'
        } else { night.innerHTML = 'Noc' }
    });

});