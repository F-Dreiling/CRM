from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    # Load all Record entries
    records = Record.objects.all()

    # Check if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect('home')

def register_user(request):
    #Check if registering
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        #Check validity
        if form.is_valid():
            form.save()

            #Authenticate and log in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully created an account")
            return redirect('home')
        else:
            return render(request, 'register.html', {'form':form})
        
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
def customer_record(request, pk):
    # Check if logged in
    if request.user.is_authenticated:
        # Look up record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    
    else:
        messages.success(request, "You must be logged in to view this page")
        return redirect('home')
    
def delete_record(request, pk):
    # Check if logged in
    if request.user.is_authenticated:
        # Look up record to delete
        delete_record = Record.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, "Record has been deleted")
        return redirect('home')
    
    else:
        messages.success(request, "You must be logged in to do that")
        return redirect('home')
    
def add_record(request):
    #
    form = AddRecordForm(request.POST or None)

    # Check if logged in
    if request.user.is_authenticated:

        if request.method == 'POST':

            if form.is_valid():
                form.save()
                messages.success(request, "You have added the record")
                return redirect('home')
                
        return render(request, 'add_record.html', {'form':form})

    else:
        messages.success(request, "You must be logged in to do that")
        return redirect('home')
        
def edit_record(request, pk):
    # Check if logged in
    if request.user.is_authenticated:
        # Look up record to update
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated")
            return redirect('home')
        
        return render(request, 'edit_record.html', {'form':form, 'current_record':current_record})
    
    else:
        messages.success(request, "You must be logged in to do that")
        return redirect('home')