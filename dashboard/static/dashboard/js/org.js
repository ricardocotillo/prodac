const orgUserBtn = document.querySelector('#create-org-user')

if (orgUserBtn) {
  orgUserBtn.addEventListener('click', e => {
    fire('formmodal:open')
  })
}