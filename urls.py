from django.urls import path, include
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('', views.home_page, name="home"),
    path('user_signup/', views.user_signup, name="user_signup"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_dashboard/', views.user_dashboard, name="user_dashboard"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('apply_nomination/', views.apply_nomination, name="apply_nomination"),
    path('show_candidate/', views.show_candidate, name="show_candidate"),
    path('show_upcoming_vote/', views.show_upcoming_vote, name="show_upcoming_vote"),
    path('my_details/', views.my_details, name="my_details"),
    path('next_vote_venu/', views.next_vote_venu, name="next_vote_venu"),
    path('check_notification/', views.check_notification, name="check_notification"),
    path('contact_admin/', views.contact_admin, name="contact_admin"),
    path('election_commisoner/', views.election_commisoner, name="election_commisoner"),
    path('delete_voter/', views.delete_voter, name="delete_voter"),
    path('delete_voter_id/<int:voter_id>/', views.delete_voter_id, name="delete_voter_id"),
    path('delete_candidate_id/<int:candidate_id>/', views.delete_candidate_id, name="delete_candidate_id"),
    path('add_candidate/', views.add_candidate, name="add_candidate"),
    path('delete_candidate/', views.delete_candidate, name="delete_candidate"),
    path('shedule_for_vote/', views.shedule_for_vote, name="shedule_for_vote"),
    path('show_election_result/', views.show_election_result, name="show_election_result"),


    # email verification
    path('activate/<uidb64>/<token>/', views.activate, name= "activate"),
    path('reset/password/', PasswordResetView.as_view(template_name = 'authentication/resetpassword.html'), name='password_reset'),
    path('reset/password/done/', PasswordResetDoneView.as_view(template_name = 'authentication/reset_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = 'authentication/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name = 'authentication/password_reset_complete.html' ), name='password_reset_complete'),
]
