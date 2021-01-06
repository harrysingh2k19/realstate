from django.contrib import admin
from .models import model_info,model_admin,model_states,model_status,model_requests,model_assign

# Register your models here.
admin.site.register(model_info)
admin.site.register(model_admin)
admin.site.register(model_states)
admin.site.register(model_status)
admin.site.register(model_requests)
admin.site.register(model_assign)
