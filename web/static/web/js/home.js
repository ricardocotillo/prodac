function homeSliderData() {
  return {
    slide: 0,
    init() {
      setInterval(() => this.slide = this.slide === 0 ? 1 : 0, 4000)
    }
  }
}