from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('login-otp-verification/', views.login_otp_verification, name='login_otp_verification'),
    path('register/', views.register, name='register'),
    path('registration-otp-verification/', views.register_otp_verification, name='register_otp_verification'),
    path('password-reset', views.password_reset, name='password_reset'),
    path('password-update', views.password_update, name='password_update'),

    # Dashboards urls

    path('administration_dashboard/', views.administration_dashboard, name='administration_dashboard'),
    path('sedo-cell-dashboard/', views.sedo_cell_dashboard, name='sedo_cell_dashboard'),
    path('sedo-sec-dashboard/', views.sedo_sec_dashboard, name='sedo_sec_dashboard'),
    path('sedo-dist-dashboard/', views.sedo_dist_dashboard, name='sedo_dist_dashboard'),
    path('wasac-dashboard/', views.wasac_dashboard, name='wasac_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),



    # Adding Rwanda administrative data

    path('add-province/', views.add_province, name='add_province'),
    path('add-district/', views.add_district, name='add_district'),
    path('add-sector/', views.add_sector, name='add_sector'),
    path('add-cell/', views.add_cell, name='add_cell'),
    path('add-village/', views.add_village, name='add_village'),

    # List Province, District, Sector, Cell, Village

    path('list-provinces/', views.list_provinces, name='list_provinces'),
    path('list-districts/', views.list_districts, name='list_districts'),
    path('list-sectors/', views.list_sectors, name='list_sectors'),
    path('list-cells/', views.list_cells, name='list_cells'),
    path('list-villages/', views.list_villages, name='list_villages'),
]
