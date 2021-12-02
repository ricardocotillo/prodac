function multiDatePickerData(value=null) {
  return {
    fp: null,
    opened: false,
    value: '',
    dates: [],
    init() {
      const config = {
        dateFormat: 'Y-m-d',
        mode: 'multiple',
        onChange: this.onChange()
      }
      this.fp = flatpickr(this.$refs.action, config)
      if (value) {
        this.value = value
        this.dates = value.split(',')
        this.fp.setDate(this.dates.join(', '))
      }
    },
    remove(i) {
      this.dates.splice(i, 1)
      this.value = this.dates.join(', ')
      this.fp.setDate(this.value)
    },
    onChange() {
      const self = this
      return function(selectedDates, dateStr, instance) {
        self.value = dateStr
        self.dates = dateStr.split(', ')
      }
    }
  }
}

function quillData(value=null) {
  return {
    value,
    quill: null,
    init() {
      const editor = this.$refs.editor
      const toolbarOptions = [
        ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
        ['blockquote', 'code-block', 'link'],
      
        [{ 'header': 1 }, { 'header': 2 }],               // custom button values
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
        [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
        [{ 'direction': 'rtl' }],                         // text direction
      
        // [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
        [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
      
        [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
        [{ 'color': '#8BB53C' }],
        [{ 'font': [] }],
        [{ 'align': ['center', 'right', 'justify', false] }],
      
        ['clean']                                         // remove formatting button
      ];
      this.quill = new Quill(editor, {
        theme: 'snow',
        modules: {
          toolbar: toolbarOptions,
        },
      })
      this.quill.on('text-change', (delta, oldDelta, source) => {
        this.value = this.quill.root.innerHTML
      });
    }
  }
}

function cropperWidgetData(value=null) {
  return {
    ...fileWidgetData(value),
    width: 500,
    height: 500,
    initialValue: value,
    init() {
      this.width = this.$refs.imageInput.dataset.width ?? this.width
      this.height = this.$refs.imageInput.dataset.height ?? this.height
      this.width = Number(this.width)
      this.height = Number(this.height)
      window.addEventListener(`image:cropped:${this.width}:${this.height}`, e => {
        this.src = e.detail.dataURL
        if (this.width > 500) {
          fire('background:update', {dataURL: this.src})
        } else {
          fire('logo:update', {dataURL: this.src})
        }
      })
      window.addEventListener(`image:cancel:${this.width}:${this.height}`, () => {
        this.$refs.imageInput.value = ''
        this.src = this.initialValue
        if (this.width > 500) {
          fire('background:update', {dataURL: null})
        } else {
          fire('logo:update', {dataURL: null})
        }
      })
    },
    changeImage(e) {
      this.src = e.detail.result
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
          fire('modal:open', {result, width: this.width, height: this.height})
        }
        reader.readAsDataURL(input.files[0]);
      }
    }
  }
}