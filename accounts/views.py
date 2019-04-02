from django.contrib.auth import authenticate, login, get_user_model, logout as salir
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, Http404
from django.utils.http import is_safe_url
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .token import activation_token
from .forms import LoginForm, RegisterForm
from .models import User


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_mail_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/home/")
        else:
            print("error")

    return render(request, "accounts/login.html", context)


def home(request):
    return render(request, "accounts/home.html", {})


#User = get_user_model()
def pagina_registro(request):

    form = RegisterForm(request.POST or None)
    context ={
        "form": form,
    }
    if form.is_valid():
        #instance = form.save(commit=False)
        form.active = True
        form.save()
        #site = get_current_site(request)
        #mail_subject = "Cofirmación de cuenta"
        #message = render_to_string('accounts/email_confirmacion.html', {
        #    'user': instance,
        #    'domain': site.domain,
        #    'uid': instance.id,
        #    'token': activation_token.make_token(instance)
        #})
        #to_email = form.cleaned_data.get('email')
        #to_list = [to_email]
        #from_email= settings.EMAIL_HOST_USER
        #send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
        return HttpResponse("<h1>Gracias por registrarte. Se te envio un correo de confirmación.</h1>")

    return render(request, "accounts/registro.html", context)


def activate(request, uid, token):
    try:
        user = get_object_or_404(User, pk=uid)
    except:
        raise Http404("No se encontro el usuario")

    if user is not None and activation_token.check_token(user, token):
        user.active = True
        user.save()
        return HttpResponse("<h1>Usuario activado, ahora puede iniciar sesión <a href='/test/home'>Login</a> </h1>")
    else:
        return HttpResponse("<h1>Link de activación invalido</h1>")


def logout(request):

    if request.method == 'POST':
        salir(request)
        return redirect('/')
