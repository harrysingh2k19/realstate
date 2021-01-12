from django.db import models
from django.contrib.auth.models import User

class model_states(models.Model):
    name = models.CharField(max_length=12)
    def __str__(self):
        return self.name

class model_status(models.Model):
    name = models.CharField(max_length=12, primary_key=True)
    def __str__(self):
        return self.name

class model_requests(models.Model):
    name = models.CharField(max_length=12, primary_key=True)
    def __str__(self):
        return self.name

class model_admin(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    def __str__(self):
        return str(self.user)


class model_info(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    request_type = models.ForeignKey(model_requests, on_delete=models.CASCADE)
    request_desc = models.TextField()
    request_city = models.CharField(max_length =40, null =True)
    request_pincode = models.IntegerField( null =True)
    request_date = models.DateTimeField(auto_now_add=True,)
    request_states = models.ForeignKey(model_states, on_delete= models.CASCADE)
    request_ccode = models.CharField(max_length =13,null =True)
    request_number = models.CharField(max_length =13,null =True)
    request_status = models.ForeignKey(model_status, on_delete= models.CASCADE, default ='Pending')
    request_remark = models.TextField(null=True)
    request_assigned = models.ForeignKey(model_admin, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.request_desc


class model_assign(models.Model):
    request_status = models.ForeignKey(model_status, on_delete= models.CASCADE, default ='Pending')
    request_remark = models.TextField(null=True)
