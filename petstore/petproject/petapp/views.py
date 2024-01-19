from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView
from .models import pet,customer,cart,order,orderdetail
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from datetime import date
# Create your views here.
class PetListView(ListView):
    model = pet
    template_name="petlist.html"
    context_object_name="petobj"

    def get_context_data(self,**kwargs):
        data = self.request.session['username']
        obj = customer.objects.get(email=data)
        context = super().get_context_data(**kwargs)
        context['session'] = obj.firstname

        return context


class PetListViewCM(ListView):
    queryset = pet.pets.get_pet_age()
    template_name="petlist.html"
    context_object_name="petobj"

class PetDetailView(DetailView):
    model = pet
    template_name="petdetail.html"
    context_object_name="i"
def search(request):
    if request.method == "POST":
        sq = request.POST.get('searchquery')
        print(sq)
        result = pet.pets.filter(Q(breed__icontains=sq)|Q(name__icontains=sq)|Q(species__icontains=sq)|Q(gender__iexact=sq)|Q(price__icontains=sq)) #custommanager object is pets (it is inherited custommanager class)
        return render(request,"petlist.html",{'petobj':result})
def registeration(request):
    if request.method == "GET":
        return render(request,"registration.html")
    elif request.method=="POST":
        fn=request.POST.get("fn") # left side attribute and right side variable jo html page pe diye input type database fetch
        ln=request.POST.get("ln")
        email=request.POST.get("email")
        phoneno=request.POST.get("phone")
        password=request.POST.get("pass")
        password = make_password(password) #encrypted password
        customerobj=customer(firstname=fn,lastname=ln,email=email,phoneno=phoneno,password=password)
        customerobj.save()

        return HttpResponse("Customer registration Successfully")
def login(request):
    if request.method=="GET":
        return render(request,"login.html")
    elif request.method=="POST":
        cust= customer.objects.filter(email = request.POST.get("email")) # filter method to check multiple records 

        if cust:
            custobj= customer.objects.get(email=request.POST.get("email"))
            passfe= request.POST.get("pass") #frontend password fetch
            flag = check_password(passfe,custobj.password) #nonencrypted password 1st argument custobj database mai se fetch krte hai oh 2nd argument that is encrypted password
          
            if flag:
                
                request.session['username']=request.POST.get("email")#session kb create hoga jb flag ki username password correct hogi tb
                session= request.session['username']

                return redirect('../petlist/')
                #return render(request,"petlist.html",{'session':session })
               
                #session = request.session['username']
         
            else:
                return HttpResponse("Wrong Username or password")
            
            
def addtocart(request):
    productid = request.POST['pid']
    pobj = pet.pets.get(id=productid)
    usersession = request.session['username']
    cobj = customer.objects.get(email = usersession)# get method single record fetch
    flag = cart.objects.filter(customerid = cobj.id,productid=pobj.id) # multiple record fetch
    if flag:
        cartobj=cart.objects.get(customerid=cobj.id,productid=pobj.id)
        cartobj.quantity = cartobj.quantity+1
        cartobj.totalamount = cartobj.quantity*pobj.price
        cartobj.save()
    else:
        cartobj = cart(quantity=1,totalamount=pobj.price,customerid=cobj,productid=pobj)
        cartobj.save()
    cartobjdisplay = cart.objects.filter(customerid = cobj.id)
    return render(request,"cart.html", {'session':cobj.firstname,'petobj':cartobjdisplay})

def viewcart(request):
    usersession = request.session['username']
    customerobj =  customer.objects.get(email=usersession)
    cartobj = cart.objects.filter(customerid = customerobj.id)
    return render(request,'cart.html',{'petobj':cartobj,'session':customerobj.firstname})

def changequantity(request):
    usersession = request.session['username']
    customerobj = customer.objects.get(email=usersession)
    pid = request.POST.get("pid")
    bq = request.POST['buttonquantity']
    if bq == '+':
        cartobj = cart.objects.get(customerid = customerobj.id,productid=pid)
        cartobj.quantity = cartobj.quantity+1
        cartobj.totalamount= cartobj.quantity*cartobj.productid.price
        cartobj.save()
    else:
        cartobj = cart.objects.get(customerid = customerobj.id,productid=pid)
        cartobj.quantity = cartobj.quantity-1
        cartobj.totalamount= cartobj.quantity*cartobj.productid.price
        cartobj.save()
        if cartobj.quantity==0:
            cartobj.delete()
    cartobj = cart.objects.filter(customerid = customerobj.id)
    return render(request,'cart.html',{'petobj':cartobj,'session':customerobj.firstname})

def summarypage(request):
    usersession = request.session['username']
    customerobj = customer.objects.get(email=usersession)
    cartobj = cart.objects.filter(customerid = customerobj.id)
    totalbill = 0;
    for i in cartobj:
        totalbill=i.totalamount+totalbill
    print(type(cartobj))
    return render(request,"summary.html",{'session':customerobj.firstname,'cartobj':cartobj,'totalbill':totalbill})

def payment(request):
    return render(request,"payment.html")

def placeolder(request):
    usersession = request.session['username']
    customerobj = customer.objects.get(email=usersession)
    name = request.POST.get('name') # left side name is attribute and right side variable database fetch
    address = request.POST.get('address')
    phoneno = int(request.POST.get('phoneno'))
    city = request.POST.get('city')
    state = request.POST.get('state')
    pincode = int(request.POST.get('pincode'))
    totalbillamount= float(request.POST.get('totalbillamount'))

    orderobj = order(name=name,address = address,phoneno=phoneno,city=city,state=state,pincode=pincode,totalbillamount=totalbillamount )
    orderobj.save()

    dateobj = date.today()
    print(dateobj)
    datedata = str(dateobj).replace('-','') #date datatype hai date type is converted to string format use str .replace - part replace with no character
    orderno =str(orderobj.id) + datedata #combiniation of id or date to generate order number
    orderobj.ordernumber = orderno
    orderobj.save()
    cartobj = cart.objects.filter(customerid = customerobj.id)
    
    #for i in cartobj: # cartobj is a set of records to iterate each and every record, i in cartobj to fetch first record cartobj
        #orderdetailobj = orderdetail(ordernumber = orderno, productid = i.productid,customerid=i.customerid,quantity=i.quantity,totalprice=i.totalamount)
       # orderdetailobj.save()
        #i.delete()
    totalbill=0
    for i in cartobj:
        totalbill=i.totalamount+totalbill
    return render(request,'payment.html',{'orderobj':orderobj,'cartobj':cartobj,'totalbill':totalbill,'session':usersession})

def logout(request):
    request.session['username']=''
    # del(request.session['username'] )
    return redirect('../login/')

def paymentsuccess(request,tid,orderid):
    print(tid)
    usersession = request.session['username']
    customerobj = customer.objects.get(email=usersession)
    cartobj = cart.objects.filter(customerid = customerobj.id)

    orderobj = order.objects.get(ordernumber = orderid)
    paymentobj = payment(transactionid = tid, paymentstatus='paid',customerid=customerobj,oid = orderobj)
    paymentobj.save()
    for i in cartobj:
        orderdetailobj = orderdetail(paymentid = paymentobj,ordernumber = orderid, productid = i.productid,customerid = i.customerid,quantity = i.quantity,totalprice = i.totalamount)
        orderdetailobj.save()
        i.delete()
    
    return render(request,'paysuccess.html')
    



