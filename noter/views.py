from django.shortcuts import render, redirect
from django.views import generic

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.db import IntegrityError

from django.urls import reverse

from .forms import LoginForm, RegisterForm, NotebookEditForm, NoteEditForm, EditUserForm

from .models import Notebook, Note

from .functions import smart_truncate

# Login page with all notebooks
@login_required
def index(request):
    user = request.user
    notebooks = Notebook.objects.all().filter(user = request.user)
    context = {'user': user, 'notebooks_list': notebooks}

    return render(request, 'noter/index.html', context)


# Login page
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print(username + ' ' + password)
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect(reverse("noter:index"))
            else:
                context = {'form': form, 'error': 'Username or password are incorrect'}
                return render(request, 'noter/login.html', context)

    else:
        form = LoginForm()

    return render(request, 'noter/login.html', {'form': form})


# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("noter:login"))


# Registration page
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1']
                )
                user.first_name = form.cleaned_data['firstname']
                user.last_name = form.cleaned_data['lastname']
                user.save()
            except IntegrityError:
                context = {'form': form, 'error': 'User with such username already exists.'}
                return render(request, 'noter/register.html', context)
    else:
        form = RegisterForm()

    return render(request, 'noter/register.html', {'form': form})



# Notebook page with notes in it
@login_required
def notebook_view(request, notebook_id):
    user = request.user
    notebook = Notebook.objects.filter(id = notebook_id)[0]
    if notebook.user != user:
        return redirect(reverse("noter:access_denied"))
    notes = Note.objects.filter(notebook = notebook)
    for note in notes:
        note.text = smart_truncate(note.text, 150)
    context = {
        'user': user,
        'notebook': notebook,
        'notes': notes
    }
    return render(request, 'noter/notebook.html', context)


# Notebook creation page
@login_required
def notebook_creation(request):
    user = request.user
    form = NotebookEditForm(request.POST)
    context = {
        'user': user,
        'form': form
    }
    if form.is_valid():
        notebook_name = form.cleaned_data['name']
        notebook_desc = form.cleaned_data['desc']
        notebook = Notebook(
            user = user,
            name = notebook_name,
            desc = notebook_desc
        )
        notebook.save()
        return redirect(reverse("noter:index"))

    return render(request, 'noter/notebook_creation.html', context)


# Notebook edit page
@login_required
def notebook_edit(request, notebook_id):
    user = request.user
    notebook = Notebook.objects.filter(id = notebook_id)[0]
    if notebook.user != user:
        return redirect(reverse("noter:access_denied"))
    form = NotebookEditForm(initial = {
        'name': notebook.name,
        'desc': notebook.desc
    })
    if request.method == "POST":
        form = NotebookEditForm(request.POST)
        if form.is_valid():
            notebook.name = form.cleaned_data['name']
            notebook.desc = form.cleaned_data['desc']
            notebook.save()
            return redirect(reverse("noter:notebook", kwargs={'notebook_id': notebook.id}))
    context = {
        "user": user,
        "notebook": notebook,
        "form": form
    }

    return render(request, 'noter/edit_notebook.html', context)


# Notebook delete view
@login_required
def notebook_delete(request, notebook_id):
    user = request.user
    notebook = Notebook.objects.filter(id = notebook_id)[0]
    if notebook.user != user:
        return redirect(reverse("noter:access_denied"))
    notes = Note.objects.filter(notebook = notebook)
    for note in notes:
        note.delete()

    notebook.delete()
    return redirect(reverse("noter:index"))


# Note page
@login_required
def note_view(request, note_id):
    user = request.user
    note = Note.objects.filter(id = note_id)[0]
    if note.notebook.user != user:
        return redirect(reverse("noter:access_denied"))
    form = NoteEditForm(initial = {
        'title': note.title,
        'text': note.text
    })
    if request.method == 'POST':
        form = NoteEditForm(request.POST)
        if form.is_valid():
            note.title = form.cleaned_data['title']
            note.text = form.cleaned_data['text']
            note.save()
            return redirect(reverse("noter:notebook", kwargs={'notebook_id': note.notebook.id}))
    context = {
        'user': user,
        'note': note,
        'form': form,
        'notebook': note.notebook
    }

    return render(request, 'noter/note.html', context)



# Note creation view
@login_required
def note_creation(request, notebook_id):
    user = request.user
    notebook = Notebook.objects.filter(id = notebook_id)[0]
    if notebook.user != user:
        return redirect(reverse("noter:access_denied"))
    note = Note(
        notebook = notebook
    )
    note.save()
    return redirect(reverse("noter:note", kwargs={'note_id': note.id}))

# Note delete view
@login_required
def note_delete(request, note_id):
    note = Note.objects.filter(id = note_id)[0]
    notebook = note.notebook
    note.delete()
    return redirect(reverse("noter:notebook", kwargs = {'notebook_id': notebook.id}))


# User settings view
@login_required
def user_settings(request):
    user = request.user
    form = EditUserForm(initial = {
        'username': user.username,
        'email': user.email,
        'lastname': user.last_name,
        'firstname': user.first_name
    })
    if request.method == "POST":
        form = EditUserForm(request.POST)
        if form.is_valid():
            try:
                user.username = form.cleaned_data['username']
                user.email = form.cleaned_data['email']
                user.last_name = form.cleaned_data['lastname']
                user.first_name = form.cleaned_data['firstname']
                user.save()
            except IntegrityError:
                context = {
                    'user': user,
                    'form': form,
                    'error': 'User with such username already exists.'
                    }
                return render(request, 'noter/user_settings.html', context)
            return redirect(reverse("noter:user_settings"))
    context = {
        'user': user,
        'form': form
    }
    return render(request, 'noter/user_settings.html', context)


# Access denied view
def access_denied(request):
    return render(request, 'noter/access_denied.html')