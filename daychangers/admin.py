from django.contrib import admin
from .models import Orderbook
from .models import Stockspecific
from .models import Margin
from .models import Stocksearch
from .models import Addedscript
from .models import Ordernumber
from .models import Pendingorder

admin.site.register(Orderbook)
admin.site.register(Stockspecific)
admin.site.register(Margin)
admin.site.register(Stocksearch)
admin.site.register(Addedscript)
admin.site.register(Ordernumber)
admin.site.register(Pendingorder)