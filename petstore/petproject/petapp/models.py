from django.db import models

# Create your models here.
class custommanager(models.Manager):
    def get_pet_age(self):
        #return super().get_queryset().filter(age=1) # age =1 this pet only fetch
        return super().get_queryset().filter(species='Cat')
        #return super().get_queryset().order_by('age')

class pet(models.Model):
    gender =(("Male","male"),("Female","female"))
    image = models.ImageField(upload_to="media")
    name = models.CharField(max_length=200)
    species = models.CharField(max_length=200)
    breed = models.CharField(max_length=200)
    age=models.CharField(max_length=200)
    gender = models.CharField(max_length=200,choices=gender)
    description= models.CharField(max_length=500)
    price = models.FloatField()
    slug = models.SlugField(default='',null=False)

    pets = custommanager()
   
class meta:
    db_table = "pets"
    
class customer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    phoneno = models.BigIntegerField()
    password = models.CharField(max_length=200)

class Meta:
    db_table = "customer"

class cart(models.Model):
    productid = models.ForeignKey(pet,on_delete = models.CASCADE)
    customerid = models.ForeignKey(customer,on_delete=models.CASCADE)
    quantity= models.IntegerField()
    totalamount = models.FloatField()

class Meta:
    db_table = "cart"