from .. import admin, db
from flask_admin.contrib.sqla import ModelView
from .models import *

# register models to admin view

admin.add_view(ModelView(Events, db.session))
admin.add_view(ModelView(Feeds, db.session))