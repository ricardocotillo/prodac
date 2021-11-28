
function profileImageData() {
  return {
    loading: false,
    onClick() {
      this.$refs.imgInput.click()
    },
    onChange() {
      const input = this.$refs.imgInput
      const url = input.value
      const ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
      if (input.files && input.files[0] && (ext == "png" || ext == "jpeg" || ext == "jpg")) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const result = e.target.result
          fire('modal:open', {result})
        }
        reader.readAsDataURL(input.files[0]);
      }
    },
    croppedImg(e) {
      this.loading = true
      const formData = new FormData()
      formData.append('image', e.detail.blob, 'profile.jpg')
      formData.append('csrfmiddlewaretoken', this.$refs.token.value)
      const url = this.$refs.saveURL.value
      fetch(url, {
        method: 'POST',
        body: formData,
      })
      .then(res => res.json())
      .then(json => {
        if (json.messages.length > 0) {
          fire('messaging:new', {messages: json.messages})
        }
        this.loading = false
        this.$refs.mainProfileImage.src = json.data.image
        fire('profileimage:update', {src: json.data.image})
      })
      .catch(err => this.loading = false)
    }
  }
}