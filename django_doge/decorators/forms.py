def labels_as_placeholders(cls):
    base_init = cls.__init__

    def __init__(self, *args, **kwargs):
        base_init(self, *args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label

    cls.__init__ = __init__
    return cls
