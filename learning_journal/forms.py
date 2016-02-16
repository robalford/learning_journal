from wtforms import Form, TextField, TextAreaField, validators, HiddenField

strip_filter = lambda x: x.strip() if x else None

class EntryCreateForm(Form):
    title = TextField(
        'Entry title',
        [validators.Length(min=1, max=255)],
        filters=[strip_filter])
    body = TextAreaField(
        'Entry body',
        [validators.Length(min=1)],
        filters=[strip_filter])
# use inheritance here?
class EntryEditForm(Form):
    id = HiddenField('Entry ID') # add validators?
    title = TextField(
        'Entry title',
        [validators.Length(min=1, max=255)],
        filters=[strip_filter])
    body = TextAreaField(
        'Entry body',
        [validators.Length(min=1)],
        filters=[strip_filter])