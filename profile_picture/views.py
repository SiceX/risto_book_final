from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView

from profile_picture.forms import EditPropicForm


def upload_file(request):
    if request.method == 'POST':
        form = EditPropicForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/home')
    else:
        form = EditPropicForm()
    return render(request, 'profile_picture/edit_propic.html', {'form': form})
