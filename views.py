from http.client import HTTPResponse
from turtle import position
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . models import Chairman_Vote_Data, Member_Vote_Data, Vote_Shedule, Voter_Registration, Nomination_paper, Nomination_list, Vote_Shedule
from . forms import VoterRegForm, LoginForm, Nomination_list_Form, VoteSheduleForm
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.models import Group
from . models import User
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserChangeForm
user_model = get_user_model()
# Create your views here.
def home_page(request):
    return render(request, 'myapp/home_page.html')

def user_signup(request):
    form = VoterRegForm()
    if request.method == "POST":
        form = VoterRegForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # email = form.cleaned_data['email']
            # user = form.save(commit=False)
            # user.is_active = False
            # user.save()
            # current_site = get_current_site(request)
            # mail_subject = 'Activate your account'
            # message = render_to_string('myapp/account.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            # send_mail = form.cleaned_data.get('email')
            # print(message)
            # print(send_mail)
            # email = EmailMessage(mail_subject, message, to=[send_mail])
            # print(email)
            # email.send()
            # form.save()
            # messages.success(request, 'Successfully created account')
            # messages.success(request, 'Activate your account from email')
            return HttpResponseRedirect('/user_login/')
    return render(request, 'myapp/user_signup.html', {'form': form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = LoginForm(data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['Voter_Id']
                psw = fm.cleaned_data['password']
                user = authenticate(username=uname, password=psw)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login Successfull!!')
                    if request.user.is_superuser:
                        return HttpResponseRedirect('/election_commisoner/')
                    return HttpResponseRedirect('/user_dashboard/')
            else:
                messages.warning(request, 'wrong user!!!!!!!!!!!!')
                return HttpResponseRedirect('/user_signup/')
        else:
            fm = LoginForm()
        return render(request, 'myapp/login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/user_dashboard/')

def user_dashboard(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/election_commisoner/')
    users = Voter_Registration.objects.get(username = request.user)
    print(users.profile_pic)
    return render(request, 'myapp/user_dashboard.html', {'user': users})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/user_login/')

def apply_nomination(request):
    users = Voter_Registration.objects.get(username = request.user)
    chairmans_lists = Nomination_paper.objects.filter(position = 'Chairman')
    members_lists = Nomination_paper.objects.filter(position = 'Member')
    if request.method == 'POST':
        all_datas = Nomination_paper.objects.all()
        count = 0
        icon_name = None
        icon_image = None
        candidate_name = request.user.first_name + " " + request.user.last_name
        position = None
        for data in all_datas:
            choice = request.POST.get(f'{data.name}')
            if choice:
                count = count + 1
                icon_name = data.name
                icon_image = data.paper_img
                position = data.position
        if count > 1:
            messages.info(request, 'You select multiple option choice only one!!!!')
            return HttpResponseRedirect('/apply_nomination/')
        data = Nomination_list(
            candidate_name = candidate_name,
            icon_name = icon_name,
            ballot_paper_img = icon_image,
            position = position
        )
        check = Nomination_list.objects.filter(icon_name= icon_name)
        for c in check:
            messages.warning(request, 'this icon is already taken, try another')
            return HttpResponseRedirect('/apply_nomination/')

        check = Nomination_list.objects.filter(candidate_name= candidate_name)
        for c in check:
            messages.warning(request, 'You are already registered for a candidate, try next year')
            return HttpResponseRedirect('/apply_nomination/')
        data.save()
        messages.success(request, 'Your Nomination is Confirm')
        return HttpResponseRedirect('/apply_nomination/')
    return render(request, 'myapp/apply_nomination.html', {'user': users, 'chairmans': chairmans_lists, 'members': members_lists})

def show_candidate(request):
    users = Voter_Registration.objects.get(username = request.user)
    nomination_lists = Nomination_list.objects.all()
    return render(request, 'myapp/show_candidate.html', {'user': users, 'nomination_lists': nomination_lists})
def show_upcoming_vote(request):
    users = Voter_Registration.objects.get(username = request.user)
    dov = Vote_Shedule.objects.get(id= 1)
    today = date.today()

    return render(request, 'myapp/show_upcoming_vote.html', {'user': users, 'dov': dov})

def my_details(request):
    users = Voter_Registration.objects.get(username = request.user)
    return render(request, 'myapp/my_details.html', {'user': users})

def next_vote_venu(request):
    users = Voter_Registration.objects.get(username = request.user)
    chairmans = Nomination_list.objects.filter(position= 'Chairman')
    members = Nomination_list.objects.filter(position= 'Member')
    if request.method == 'POST':
        chairman_list = Nomination_list.objects.filter(position = 'Chairman')
        count = 0
        voter_id = ''
        voter_name = ''
        candidate_name = ''
        icon_name = ''
        ballot_paper_img = ''
        for chairman in chairman_list:
            choice = request.POST.get(f'{chairman.candidate_name}')
            if choice:
                count = count + 1
                voter_id = users.username
                voter_name = users.first_name + " " + users.last_name
                candidate_name = chairman.candidate_name
                icon_name = chairman.icon_name
                ballot_paper_img = chairman.ballot_paper_img
        if count >=2:
            messages.warning(request, 'you select more than one chairman, select only one !!!!!!')
            return HttpResponseRedirect('/next_vote_venu/')
        if voter_id == '':
            # return HttpResponseRedirect('/next_vote_venu/')
            pass
        else:
            data = Chairman_Vote_Data(
                voter_id = voter_id,
                voter_name = voter_name,
                candidate_name = candidate_name,
                icon_name = icon_name,
                ballot_paper_img = ballot_paper_img
            )
            checker = Chairman_Vote_Data.objects.filter(voter_id = voter_id)
            flag = True
            for check in checker:
                flag = False
            if flag == False:
                messages.warning(request, 'You are already voted for chairman cadidate, try for member....!')
                return HttpResponseRedirect('/next_vote_venu/')
            else:
                data.save()
                messages.success(request, 'Your vote is successfully taken.... try for member now.....')
                return HttpResponseRedirect('/next_vote_venu/')
        
        # member criteria
        member_list = Nomination_list.objects.filter(position = 'Member')
        count = 0
        voter_id = ''
        voter_name = ''
        candidate_name = ''
        icon_name = ''
        ballot_paper_img = ''
        for member in member_list:
            choice = request.POST.get(f'{member.candidate_name}')
            if choice:
                count = count + 1
                voter_id = users.username
                voter_name = users.first_name + " " + users.last_name
                candidate_name = member.candidate_name
                icon_name = member.icon_name
                ballot_paper_img = member.ballot_paper_img
        if count >=2:
            messages.warning(request, 'you select more than one member, select only one !!!!!!')
            return HttpResponseRedirect('/next_vote_venu/')
        if voter_id == '':
            # return HttpResponseRedirect('/next_vote_venu/')
            messages.warning(request, 'select one candidate !!!!!!')
            pass
        else:
            data = Member_Vote_Data(
                voter_id = voter_id,
                voter_name = voter_name,
                candidate_name = candidate_name,
                icon_name = icon_name,
                ballot_paper_img = ballot_paper_img
            )
            checker = Member_Vote_Data.objects.filter(voter_id = voter_id)
            flag = True
            for check in checker:
                flag = False
            if flag == False:
                messages.warning(request, 'You are already voted for member cadidate, try for chairman....!')
                return HttpResponseRedirect('/next_vote_venu/')
            else:
                data.save()
                messages.success(request, 'Your vote is successfully taken.... try for chairman now.....')
                return HttpResponseRedirect('/next_vote_venu/')
    return render(request, 'myapp/next_vote_venu.html', {'user': users, 'chairmans': chairmans, 'members': members})

def check_notification(request):
    users = Voter_Registration.objects.get(username = request.user)
    return render(request, 'myapp/check_notification.html', {'user': users})

def contact_admin(request):
    users = Voter_Registration.objects.get(username = request.user)
    return render(request, 'myapp/contact_admin.html', {'user': users})

def election_commisoner(request):
    return render(request, 'myapp/election_commisoner.html')

def delete_voter(request):
    voters = Voter_Registration.objects.all()
    return render(request, 'myapp/delete_voter.html', {'voters': voters})

def delete_voter_id(request, voter_id):
    voters = Voter_Registration.objects.get(id= voter_id)
    voters.delete()
    messages.success(request, 'This Voter is deleted successfully!!!!!!')
    return HttpResponseRedirect('/delete_voter/')

def add_candidate(request):
    form = Nomination_list_Form()
    return render(request, 'myapp/add_candidate.html', {'form': form})

def delete_candidate(request):
    candidates = Nomination_list.objects.all()
    return render(request, 'myapp/delete_candidate.html', {'candidates': candidates})

def delete_candidate_id(request, candidate_id):
    candidate = Nomination_list.objects.get(id= candidate_id)
    # candidate.delete()
    messages.success(request, 'This Candidate is deleted successfully!!!!!!')
    return HttpResponseRedirect('/delete_candidate/')

def shedule_for_vote(request):
    form = VoteSheduleForm()
    if request.method == 'POST':
        form = VoteSheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Date Added Successfully')
            return HttpResponseRedirect('/election_commisoner/')
    return render(request, 'myapp/shedule_for_vote.html', {'form': form})

def show_election_result(request):
    chairman_results = Chairman_Vote_Data.objects.all()
    chairman_candidates = Nomination_list.objects.filter(position= 'Chairman')
    member_results = Member_Vote_Data.objects.all()
    member_candidates = Nomination_list.objects.filter(position= 'Member')
    chairman_final_result = {}
    member_final_result = {}
    for chairman_candidate in chairman_candidates:
        count = 0
        for chairman_result in chairman_results:
            if(chairman_result.candidate_name == chairman_candidate.candidate_name):
                count = count + 1
        chairman_final_result[chairman_candidate] = count

    for member_candidate in member_candidates:
        count = 0
        for member_result in member_results:
            if(member_result.candidate_name == member_candidate.candidate_name):
                count = count + 1
        member_final_result[member_candidate] = count
    context = {
        'member_final_result': member_final_result,
        'chairman_final_result': chairman_final_result,
    }
    return render(request, 'myapp/show_election_result.html', context)


# activate your account

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = user_model._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account activated now you can login')
        return HttpResponseRedirect('/user_login/')
    else:
        messages.warning(request, 'activation link is invalid')
        return HttpResponseRedirect('/')