from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import JobApplication, Company, Status, JobType
from .forms import JobApplicationForm

class JobApplicationListView(LoginRequiredMixin, ListView):
    model = JobApplication
    template_name = 'jobapplication_list.html'
    context_object_name = 'applications'


    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user).select_related('company', 'status').order_by('-date_applied')


class JobApplicationDetailView(LoginRequiredMixin, DetailView):
    model = JobApplication
    template_name = 'jobapplication_detail.html'
    context_object_name = 'application'

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user).select_related(
            'company', 'status'
        )

class JobApplicationCreateView(LoginRequiredMixin, CreateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'jobapplication_form.html'
    success_url = reverse_lazy('jobapplication_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        company = form.cleaned_data['company']
        position = form.cleaned_data['position']

        # Check for duplicate
        if JobApplication.objects.filter(user=self.request.user, company=company, position=position).exists():
            messages.error(self.request, 'You have already applied for this position at this company.')
            return redirect('jobapplication_list')

        messages.success(self.request, 'Job application created successfully.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass user to form
        return kwargs

def job_application_detail(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    return render(request, 'jobapplication_detail.html', {'application': application})

class JobApplicationUpdateView(LoginRequiredMixin, UpdateView):
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'jobapplication_form.html'
    success_url = reverse_lazy('jobapplication_list')

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Job application updated successfully.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass user to form
        return kwargs

class JobApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = JobApplication
    success_url = reverse_lazy('jobapplication_list')
    template_name = 'jobapplication_confirm_delete.html'

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} is already taken!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'An account with email {email} is already registered!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User {username} has been registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'register.html')


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    applications = JobApplication.objects.filter(user=request.user)

    context = {
        'applications': applications,
        'applied': applications.filter(status__status='a').count(),
        'interview': applications.filter(status__status='i').count(),
        'offer': applications.filter(status__status='o').count(),
        'rejected': applications.filter(status__status='r').count(),
        'achieved': applications.filter(status__status='ach').count(),
    }

    return render(request, 'index.html', context)



class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    fields = ['name', 'email', 'phone_number', 'website', 'location', 'description']
    template_name = 'company_form.html'
    success_url = reverse_lazy('company_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Company created successfully!")
        return super().form_valid(form)

class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)

class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    fields = ['name', 'email', 'phone_number', 'website', 'location', 'description']
    template_name = 'company_form.html'
    success_url = reverse_lazy('company_list')

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)

class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'jobapplication_confirm_delete.html'
    success_url = reverse_lazy('company_list')

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)