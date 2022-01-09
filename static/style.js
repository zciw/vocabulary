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