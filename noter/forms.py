from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = "Username", max_length=30)
    password = forms.CharField(label = "Password", widget = forms.PasswordInput)


class RegisterForm(forms.Form):
    firstname = forms.CharField(label = "First Name", max_length=50)
    lastname = forms.CharField(label = "Last Name", max_length=50)
    username = forms.CharField(label = "Username", max_length=30)
    email = forms.CharField(label = "Email", max_length=50, widget = forms.EmailInput)
    password1 = forms.CharField(label = "Password", max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(label = "Confirm Password", max_length=50, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords doesn't match.")


class NotebookEditForm(forms.Form):
    name = forms.CharField(label = "Notebook name", max_length=30)
    desc = forms.CharField(label = "Notebook description", max_length=300)


class NoteEditForm(forms.Form):
    title = forms.CharField(label = "Note title", max_length=200, required=False)
    text = forms.CharField(label = "Note text", widget=forms.Textarea, required = False)


class EditUserForm(forms.Form):
    firstname = forms.CharField(label = "First Name", max_length=50)
    lastname = forms.CharField(label = "Last Name", max_length=50)
    username = forms.CharField(label = "Username", max_length=30)
    email = forms.CharField(label = "Email", max_length=50, widget = forms.EmailInput)