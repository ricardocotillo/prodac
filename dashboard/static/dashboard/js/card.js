function qrData() {
  return {
    loading: false,
    generated: false,
    onClick() {
      this.loading = true
      const cardURL = JSON.parse(document.querySelector('#cardURL').textContent)
      const svg = new QRCode(cardURL).svg()
      const parser = new DOMParser()
      const doc = parser.parseFromString(svg, 'image/svg+xml')

      const wrapper = this.$refs.wrapper
      this.loading = true
      this.generated = true
      wrapper.appendChild(doc.documentElement)
      fire('qrcode:generated', {svg})
    }
  }
}

function updateServices() {
  return {
    ...basicFormData(),
    onSubmit(e) {
      e.preventDefault()
      const formData = new FormData(e.target)
      const url = e.target.getAttribute('action')
      fetch(url, {
        method: 'POST',
        body: formData
      })
        .then(res => res.json())
        .then(json => {
          this.updateFormIds(json['data'])
          this.processResponse(json)
          this.loading = false
        })
        .catch(err => this.loading = false)
    },
    updateFormIds(ids) {
      Object.keys(ids).forEach(k => {
        this.$el[k].value = ids[k]
      })
      const formsAdded = Object.keys(ids).length
      const initialForms = this.$el['form-INITIAL_FORMS']
      initialForms.value = formsAdded + Number(initialForms.value)
    }
  }
}

function cropIconData() {
  return {
    ...cropModalData(),
    width: null,
    height: null,
    crop(e) {
      this.src = e.detail.result
      this.width = e.detail.width
      this.height = e.detail.height
      this.open = true
      const img = this.$refs.cropperImg
      this.$nextTick(() => {
        this.cropper = new Cropper(img, {
          aspectRatio: 1,
          viewMode: 0,
          minContainerWidth: 350,
          minContainerHeight: 350,
        })
      })
    },
    onSave() {
      this.loading = true
      const croppedCanvas = this.cropper.getCroppedCanvas({width: this.width, height: this.height, fillColor: '#ffffff'})
      const dataURL = croppedCanvas.toDataURL('image/jpeg')
      fire(`image:cropped:${this.width}:${this.height}`, {dataURL})
      this.loading = false
      this.open = false
      this.cropper.destroy()
    },
    onCancel() {
      this.open = false
      this.cropper.destroy()
      fire(`image:cancel:${this.width}:${this.height}`)
    }
  }
}

function updateCard() {
  return {
    ...basicFormData(),
    logo: null,
    init() {
      window.addEventListener('logo:update', e => {
        this.logo = e.detail.dataURL
      })
    },
    async toBlob(dataURL) {
      const res = await fetch(dataURL)
      const blob = await res.blob()
      return blob
    },
    storeQR(e) {
      const svg = e.detail.svg
      const blob = new Blob([svg], {type: 'image/svg+xml'});
      this.blob = blob
    },
    processResponse(json) {
      const messages = json.messages
      if (json.errors) {
        Object.keys(json.errors).forEach(e => {
          if (e === 'qrcode') {
            messages.push({
              'level_tag': 'error',
              'message': json.errors[e]
            })
          } else {
            this.$refs[`id_${e}`].querySelector('small').innerText = json.errors[e]
          }
        })
      }
      
      if (json.messages && json.messages.length > 0) {
        fire('messaging:new', {messages: json.messages})
      }
    },
    async onSubmit(e) {
      e.preventDefault()
      this.loading = true
      const form = e.target
      const formData = new FormData(form)
      if (this.logo) {
        const logoBlob = await this.toBlob(this.logo)
        formData.set('logo', logoBlob, 'logo.jpg')
      }
      const url = window.location.pathname
      fetch(url, {
        method: 'POST',
        body: formData,
      })
        .then(res => res.json())
        .then(json => {
          this.loading = false
          this.processResponse(json)
        })
        .catch(err => {
          this.loading = false
          console.log(err)
        })
    }
  }
}