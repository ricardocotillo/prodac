import uuid
def make_file_path(instance, filename):
    # eg: filename = 'my uploaded file.jpg'
    ext = filename.split('.')[-1]  #eg: '.jpg'
    uid = uuid.uuid4().hex[:10]    #eg: '567ae32f97'

    # eg: 'my-uploaded-file'
    new_name = '-'.join(filename.replace('.%s' % ext, '').split())

    # eg: 'my-uploaded-file_64c942aa64.jpg'
    renamed_filename = '%(new_name)s_%(uid)s.%(ext)s' % {'new_name': new_name, 'uid': uid, 'ext': ext}

    # eg: 'images/2017/01/29/my-uploaded-file_64c942aa64.jpg'
    return '/'.join([instance.__class__.__name__.lower(), renamed_filename])