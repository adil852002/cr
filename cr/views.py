from django.shortcuts import render,redirect
from django.views.generic import View
from cr.forms import EmployeeForm,RegistrationForm,LoginForm
from cr.models import Employees
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Invalid Session")
            return redirect("login")
        else:
            return fn(request,*args,**kwargs)
        
    return wrapper
# Create your views here.
class Index(View):
    def get(self,request,*args,**kwargs):
        return render (request,"index.html")

@method_decorator(signin_required,name="dispatch")
class EmployeeCreateView(View):

    def get(self,request,*args,**kwargs):
        form=EmployeeForm()
        return render(request,"emp_add.html",{"forms":form})
    
    def post(self,request,*args,**kwargs):
        form=EmployeeForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Employee has been added successfully.....")
            # Employees.objects.create(**form.cleaned_data)
            print("valid")
            return render(request,"emp_add.html",{"form":form})

        else:
             messages.error(request,"Failed to add an employee")
             return render(request,"emp_add.html",{"form":form})
           

@method_decorator(signin_required,"dispatch")       
class EmployeeListView(View):
    def get (self,request,*args,**kwargs):
        if request.user.is_authenticated:
            qs=Employees.objects.all()
            department=Employees.objects.all().values_list("department",flat=True).distinct()
            print(department)
            if "department" in request.GET:
                dept=request.GET.get("department")
                qs=qs.filter(department__iexact=dept)

            return render(request,"emp_list.html",{"data":qs,"department":department})
       
    def post (self,request,*args,**kwargs):
        name=request.POST.get("name")
        print(name)
        qs=Employees.objects.filter(name__icontains=name)
        return render(request,"emp_list.html",{"data":qs})


@method_decorator(signin_required,"dispatch")       
class EmployeeDetailView(View):
    def get (self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        return render(request,"emp_details.html",{"data":qs})

@method_decorator(signin_required,"dispatch")          
class EmployeeDeleteView(View):
    def get (self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Employees.objects.get(id=id).delete()
        messages.success(request,"employee has been deleted")
        return redirect("emp_all")

@method_decorator(signin_required,"dispatch")         
class EmployeeUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        form=EmployeeForm(instance=qs)
        return render(request,"emp_add.html",{"forms":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        form=EmployeeForm(request.POST,files=request.FILES,instance=qs)
        if form.is_valid():
            form.save()
            messages.success(request,"employee has been updated successfully")
            # Employees.objects.create(**form.cleaned_data)
            print("valid")
            return redirect('emp_all')

        else:
            messages.error(request,"failed to display employee")
            return render(request,"emp_add.html",{"form":form})
        
        
class SingpuView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"EMPLOYEE CREATED")
            return render(request,"register.html",{"form":form})
        else:
            messages.error(request,"failed to create")
            return render(request,"register.html",{"form":form})
        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
        
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            usr_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(usr_name,pwd)
            user_obj=authenticate(request,username=usr_name,password=pwd)
            if user_obj:
                print("User is Valid")
                login(request,user_obj)
                return redirect("emp_all")
            messages.error(request,"invalid!!!")
            return render(request,"login.html",{"form":form})

@method_decorator(signin_required,"dispatch")              
class SingOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("login")
            