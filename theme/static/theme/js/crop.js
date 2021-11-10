const modal = document.querySelector('#crop-modal')
    const closeIcon = document.querySelector('#crop-modal .close')
    closeIcon.addEventListener('click', function(e) {
    modal.classList.remove('block')
})