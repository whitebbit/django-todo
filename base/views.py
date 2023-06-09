from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.


class LoginViews(LoginView):
    template_name = "base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True
    
    def get_success_url(self) -> str:
        return reverse_lazy("tasks")
    

class RegisterView(FormView):
    template_name = "base/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("tasks")

    def form_valid(self, form: Any) -> HttpResponse:
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect("tasks")
        return super(RegisterView, self).get(request, *args, **kwargs)    


class TaskList(LoginRequiredMixin, ListView):
    model = Task 
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()
        
        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["tasks"] = context["tasks"].filter(
                title__icontains=search_input)
        
        return context
    
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/task.html"
    
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description"]
    success_url = reverse_lazy("tasks")
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        if not form.is_valid():
            redirect("tasks")
        return super(TaskCreate, self).form_valid(form)
    
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ["title", "description"]
    success_url = reverse_lazy("tasks")
    
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")
    
def change_task_state(request, pk):
    task = Task.objects.get(id=pk)
    task.complete = not task.complete
    task.save()
    return redirect("tasks")
    