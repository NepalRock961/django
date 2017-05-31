from django.shortcuts import render, redirect
from django.http import HttpResponse
from todos.models import Todo
from django.utils import timezone
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):
    items = []
    filter = None

    # Get only the user-specific todo items.
    if request.user.is_authenticated:
        filter = request.GET.get('filter')
        print('Filter = ', filter)

        items = filter_results(request.user, filter)

    return render(request, 'index.html', {
        'items': items,
        'filter': filter
    })


def filter_results(user, filter):
    # If filter is completed
    if filter == 'completed':
        return Todo.objects.filter(
            user=user,
            completed=True
        ).order_by('-created_at')

    # Else If filter is pending
    elif filter == 'pending':
        return Todo.objects.filter(
            user=user,
            completed=False
        ).order_by('-created_at')

    # Otherwise
    else:
        return Todo.objects.filter(user=user).order_by('-created_at')


@login_required
def create(request):
    return render(request, 'form.html', {
        'form_type': 'create'
    })


@login_required
def save(request):
    # Get the form data from the request.
    title = request.POST.get('title')
    description = request.POST.get('description')

    # Get hidden form data.
    form_type = request.POST.get('form_type')
    id = request.POST.get('id')

    print('Form type received:', form_type)
    print('Form todo id received:', id)

    # Validation logic
    if title is None or title.strip() == '':
        messages.error(request, 'Item not saved. Please provide the title.')
        return redirect(request.META.get('HTTP_REFERER'))

    if form_type == 'create':
        # Create a new todo item with the data.
        todo = Todo.objects.create(
            title=title,
            description=description,
            created_at=timezone.now(),
            user=request.user
        )
        print('New Todo created: ', todo.__dict__)
    elif form_type == 'edit' and id.isdigit():
        todo = Todo.objects.get(pk=id)
        print('Got todo item: ', todo.__dict__)

        # Save logic
        todo.title = title
        todo.description = description

        todo.save()
        print('Todo updated: ', todo.__dict__)

    # Add save success message
    messages.info(request, 'Todo Item Saved.')
    # Redirect back to index page
    return redirect('index')


@login_required
def edit(request, id):
    print('Received Id: ' + str(id))

    # Fetch todo item by id
    todo = Todo.objects.get(pk=id)
    print('Got todo item: ', todo.__dict__)

    # Check if the logged in user is the creator user of todo.
    if request.user.id != todo.user.id:
        messages.error(
            request, 'You are not authorized to edit this todo item.')
        return redirect('index')

    return render(request, 'form.html', {
        'form_type': 'edit',
        'todo': todo
    })


@login_required
def delete(request, id):
    # Fetch todo item by id
    todo = Todo.objects.get(pk=id)
    print('Got todo item: ', todo.__dict__)

    # Check if the logged in user is the creator user of todo.
    if request.user.id == todo.user.id:
        messages.info(request, 'Todo Item has been deleted.')
        todo.delete()
        return redirect('index')

    messages.error(request, 'You are not authorized to delete this todo item.')
    return redirect('index')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def login(request):
    

    return render(request, 'login.html')
def signup(request):

    return render(request, 'signup.html')
def submission(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')


    if User.objects.filter(username=username).exists():
        messages.error(request, 'username{} already exists.'.format(username))
        return redirect_back(request)

    if User.objects.filter(email=email).exists():
        messages.error(request, 'email {} already exists.'.format(email))
        return redirect_back(request)

    user= User.objects.create_user(username=username, 
        password=password, 
        email=email, 
        first_name=first_name, 
        last_name=last_name
        )

    messages.info(request, 'user created')

    return redirect('login')



def submit(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    print('Recived username and password')
    print('Logging in')

    user = auth.authenticate(request,
        username=username,
        password=password
        )

    if not user:
        print('login failed')
        messages.error(request,'Login Failed. Try again')
        return redirect(request.META.get('HTTP_REFERER'))

    auth.login(request, user)
    print('Login sucessful')

    messages.info(request,'login sucessful')

    return redirect('index')
