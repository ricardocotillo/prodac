const copyBtns = document.querySelectorAll('.copy-to-clipboard')

function messaging() {
  return {
    alerts: [],
    addMessages(e) {
      e.detail.messages.forEach(m => {
        this.alerts.push(m)
        setTimeout(() => {
          this.alerts.shift()
        }, 4000)
      })
    },
    removeAlert(i) {
      this.alerts.splice(i, 1)
    }
  }
}

function basicFormData() {
  return {
    loading: false,
    reset() {
      Object.values(this.$refs).forEach(r => {
        r.querySelector('small').innerText = ''
      })
    },
    processResponse(json) {
      if (json.errors) {
        Object.keys(json.errors).forEach(e => {
          this.$refs[`id_${e}`].querySelector('small').innerText = json.errors[e]
        })
      }
      
      if (json.messages && json.messages.length > 0) {
        fire('messaging:new', {messages: json.messages})
      }
    },
    onSubmit(e) {
      e.preventDefault()
      this.loading = true
      this.reset()
      const form = e.target
      const formData = new FormData(form)
      const url = form.getAttribute('action')
      fetch(url, {
        method: 'POST',
        body: formData,
      })
        .then(res => {
          console.log(res)
          return res.json()
        })
        .then(json => {
          console.log(json)
          this.loading = false
          this.processResponse(json)
        })
        .catch(err => this.loading = false)
    }
  }
}

function modalFormData() {
  return {
    open: false,
    close() {
      this.open = false
      this.reset()
    },
    ...basicFormData(),
    onSubmit() {},
  }
}

function tableData(pages) {
  return {
    page: 1,
    content: null,
    pages,
    paginateBack(url) {
      if (this.page <= 1) return
      this.page--
      url = `${url}?page=${this.page}`
      fetch(url)
        .then(res => res.text())
        .then(data => {
          this.content = data
        })
    },
    paginateForward(url) {
      if (this.page >= this.pages) return
      this.page++
      url = `${url}?page=${this.page}`
      fetch(url)
        .then(res => res.text())
        .then(data => {
          this.content = data
        })
    },
    delete(pk) {
      fetch()
    }
  }
}

function fileWidgetData(value=null) {
  return {
    src: value,
    onClick() {
      this.$refs.imageInput.click()
    },
    onChange() {
      const input = this.$refs.imageInput
      const url = input.value
      const ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
      if (input.files && input.files[0] && (ext == "png" || ext == "jpeg" || ext == "jpg" || ext == 'webp')) {
        if (this.$refs.clear) {
          this.$refs.clear.checked = false
        }
        const reader = new FileReader();
        reader.onload = (e) => {
          const result = e.target.result
          this.src = result
        }
        reader.readAsDataURL(input.files[0]);
      }
    },
    onRemove(e) {
      e.stopPropagation()
      if (this.$refs.clear) {
        this.$refs.clear.checked = true
      }
      this.src = null
      console.dir(this.$refs.clear)
    }
  }
}

function fire(eventName, detail) {
  const event = new CustomEvent(eventName, {detail})
  window.dispatchEvent(event)
}

function cropModalData() {
  return {
    open: false,
    loading: false,
    src: '',
    cropper: null,
    width: 600,
    height: 600,
    crop(e) {
      this.src = e.detail.result
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
      const croppedCanvas = this.cropper.getCroppedCanvas(600, 600)
      croppedCanvas.toBlob(blob => {
        fire('image:cropped', {blob: blob})
        this.loading = false
        this.open = false
        this.cropper.destroy()
      }, 'image/jpeg')
    },
    onCancel() {
      this.open = false
      this.cropper.destroy()
    }
  }
}

copyBtns.forEach(c => {
  c.addEventListener('click', () => {
    const text = c.dataset.text
    navigator.clipboard.writeText(text)
    fire('messaging:new', {messages: [
      {
        'level_tag': 'info',
        message: 'Link copiado correctamente',
      }
    ]})
  })
})