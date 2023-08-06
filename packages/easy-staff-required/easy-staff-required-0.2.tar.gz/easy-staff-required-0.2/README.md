# Easy Staff Required

A simple Django decorator to restrict view access to staff users.

## Installation

Install the package using pip:

```bash
pip install django-staff-required
```

## Usage

After installing the package, you can use the `@staff_required` decorator in your Django views to restrict access to staff users. Here's an example:

```python
from django.shortcuts import render
from django_staff_required import staff_required

@staff_required
def my_view(request):
    return render(request, "my_template.html")
```

The @staff_required decorator checks if the user is authenticated and has the is_staff attribute set to True. If the user is not a staff member, a PermissionDenied exception is raised.

You can also use the @staff_required decorator in combination with Django's built-in @login_required decorator:

```python
from django.contrib.auth.decorators import login_required
from django_staff_required import staff_required

@login_required
@staff_required
def my_view(request):
    return render(request, "my_template.html")
```