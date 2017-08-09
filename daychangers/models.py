from django.db import models
from django.contrib.auth.models import Permission, User

# Create your models here.
class Orderbook(models.Model):
	client_id=models.CharField(max_length=100)
	symbol = models.CharField(max_length=250)
	price =models.DecimalField(max_digits=7, decimal_places=2)
	quantity = models.IntegerField()
	date =models.DateTimeField()
	trade_type=models.CharField(max_length=250)
	orderno=models.IntegerField()
	ordertype=models.CharField(max_length=100)
	status=models.CharField(max_length=100)
	
	def __str__(self):
		return  self.client_id
		
class Pendingorder(models.Model):
	client_id=models.CharField(max_length=100)
	symbol = models.CharField(max_length=250)
	price =models.DecimalField(max_digits=7, decimal_places=2)
	quantity = models.IntegerField()
	date =models.DateTimeField()
	trade_type=models.CharField(max_length=250)
	orderno=models.IntegerField()
	ordertype=models.CharField(max_length=100)
	status=models.CharField(max_length=100)		

	def __str__(self):
		return  self.client_id		

class Stockspecific(models.Model):
	orderdetail = models.ForeignKey(Orderbook,null=True)
	symbol = models.CharField(max_length=250)
	price =models.DecimalField(max_digits=7, decimal_places=2)
	quantity = models.IntegerField(null=True)	
	total=models.IntegerField(null=True)

	def __str__(self):
		return  self.symbol

class Margin(models.Model):
	user=models.CharField(max_length=100)
	funds=models.DecimalField(max_digits=9, decimal_places=2)
	holdings=models.DecimalField(max_digits=9, decimal_places=2)

	def __str__(self):
		return  self.user
		
class Stocksearch(models.Model):
	name=models.CharField(max_length=20)

class Ordernumber(models.Model):
	number=models.IntegerField()

	def __str__(self):
		return  str(self.number)

class Addedscript(models.Model):
	user=models.CharField(max_length=100)
	name=models.CharField(max_length=20,null=True)
	ltp=models.DecimalField(max_digits=9, decimal_places=2)

	def __str__(self):
		return  self.name