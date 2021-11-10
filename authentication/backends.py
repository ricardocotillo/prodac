from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from organizations.backends.defaults import InvitationBackend
from django.utils.translation import gettext as _

class AppInvitationBackend(InvitationBackend):

    def activate_view(self, request, user_id, token):
        """
        View function that activates the given User by setting `is_active` to
        true if the provided information is verified.
        """
        try:
            user = self.user_model.objects.get(id=user_id, is_active=False)
        except self.user_model.DoesNotExist:
            raise Http404(_("Your URL may have expired."))

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise Http404(_("Your URL may have expired."))
        form = self.get_form(data=request.POST or None, files=request.FILES or None, instance=user)
        if form.is_valid():
            form.instance.is_active = True
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            self.activate_organizations(user)
            login(request, user)
            return redirect('dashboard')
        return render(request, self.registration_form_template, {"form": form})