const video = document.querySelector('#video')

window.onload = () => {
  const splash = document.querySelector('#splash-screen')
  splash.style.display = 'none'
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

function bookingFormData() {
  return {
    ...basicFormData(),
    loading: false,
    slotsURL: JSON.parse(document.querySelector('#slots-url').textContent),
    fp: null,
    init() {
      const dateInput = this.$el.date
      const slotSelect = this.$el.slot
      const currentDate = new Date()
      this.fp = flatpickr(dateInput, {
        dateFormat: 'Y-m-d',
        minDate: new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() + 1),
        maxDate: new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() + 7),
      })
      dateInput.addEventListener('change', (e) => {
        if (slotSelect.options.length > 0) {
          Array.from(slotSelect.options).forEach(opt =>  slotSelect.remove(opt)) 
        }
        const d = e.target.value
        if (!d) {
          return
        }
        const url = `${this.slotsURL}?date=${d}`
        fetch(url)
          .then(res => res.json())
          .then(json => {
            Object.keys(json.slots).map((s, i) => {
              const opt = document.createElement('option')
              opt.value = i === 0 ? '' : s
              opt.selected = i === 0
              opt.text = s
              if (!json.slots[s]) {
                opt.disabled = true
              }
              return opt
            }).forEach(opt => slotSelect.options.add(opt))
          })
      })
    },
    clean() {
      this.fp.clear()
    },
    onSubmit(e) {
      e.preventDefault()
      const cardPk = JSON.parse(document.querySelector('#card-pk').textContent)
      this.reset()
      const form = e.target
      const formData = new FormData(form)
      formData.append('card', cardPk)
      const url = form.getAttribute('action')
      fetch(url, {
        method: 'POST',
        body: formData,
      })
        .then(res => res.json())
        .then(json => {
          this.loading = false
          this.processResponse(json)
          this.clean()
        })
        .catch(err => this.loading = false)
    }
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

if (video) {
  const openVideo = document.querySelector('#open-video')
  openVideo.addEventListener('click', function(e) {
    video.style.display = 'flex'
  })
  const close = video.querySelector('span')
  close.addEventListener('click', function(e) {
    video.style.display = 'none'
  })
}