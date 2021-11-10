function orgFormData() {
  return {
    loading: false,
    firstFill: true,
    init() {
      const name = this.$refs.id_name.querySelector('#id_name')
      const slug = this.$refs.id_slug.querySelector('#id_slug')
      name.addEventListener('input', e => {
        const v = e.target.value
        const s = getSlug(v, {
          lang: 'es'
        })
        slug.value = s
      })
    },
    onSubmit() {},
  }
}