window.onload = () => {
  const splash = document.querySelector('#splash-screen')
  splash.style.display = 'none'
  new Splide( '.splide', {
    autoplay: true,
    type: 'loop',
    pagination: false,
    arrows: false,
    interval: 4000,
  } ).mount()
}

function pageData() {
  return {
    init() {
      this.page = window.location.hash !== '' ? window.location.hash : '#home'
      const navIcons = document.querySelectorAll('#nav-menu a')
      navIcons.forEach(icon => icon.addEventListener('click', e => {
        this.page = e.target.getAttribute('href')
      }))
    },
    page: '#home'
  }
}

function menuData() {
  return {
    current: null,
    onClick(e) {
      const icon = e.target
      if (this.current) {
        this.current.classList.remove('text-primary')
      }
      icon.classList.add('text-primary')
      this.current = icon
    }
  }
}