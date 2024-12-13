from django.shortcuts import redirect, render
from .models import Province, District, Sector, Cell, Village
from .forms import ProvinceForm, DistrictForm, SectorForm, CellForm, VillageForm
#from .models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')
def password_reset(request):
    return render(request, 'password_reset.html')
def password_update(request):
    return render(request, 'password_update.html')
def password_reset_confirm(request):
    return render(request, 'password_reset_confirm.html')
def login_otp_verification(request):
    return render(request, 'login_otp_verification.html')
def register_otp_verification(request):
    return render(request, 'reg_otp_verification.html')
def administration_dashboard(request):
    return render(request, 'admin_dashboard.html')
def sedo_cell_dashboard(request):
    return render(request, 'sedo_cell_dashboard.html')
def sedo_sec_dashboard(request):
    return render(request, 'sedo_sec_dashboard.html')
def sedo_dist_dashboard(request):
    return render(request, 'sedo_dist_dashboard.html')
def wasac_dashboard(request):
    return render(request, 'wasac_dashboard.html')

def user_dashboard(request):
    return render(request, 'user_dashboard.html')


# adding Rwanda administrative data

def add_province(request):
    if request.method == 'POST':
        form = ProvinceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_provinces')
    else:
        form = ProvinceForm()
    return render(request, 'add_edit_province.html', {'form': form})

def add_district(request, province_id, ):  # Replace province_id with the actual parameter
    if request.method == 'POST':
        form = DistrictForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_districts')
    else:
        form = DistrictForm()
    return render(request, 'add_edit_district.html', {'form': form})

def add_sector(request, district_id, ):  # Replace district_id with the actual parameter_list):
    if request.method == 'POST':
        form = SectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_sectors')
    else:
        form = SectorForm()
    return render(request, 'add_edit_sector.html', {'form': form})

def add_cell(request, sector_id, ):  # Replace sector_id with the actual parameter
    if request.method == 'POST':
        form = CellForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_cells')
    else:
        form = CellForm()
    return render(request, 'add_edit_cell.html', {'form': form})

def add_village(request, cell_id, ):  # Replace cell_id with the actual parameter(parameter_list):
    if request.method == 'POST':
        form = VillageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_villages')
    else:
        form = VillageForm()
    return render(request, 'add_edit_village.html', {'form': form})

# Listing data
# Province Views
def list_provinces(request):
    provinces = Province.objects.all()
    return render(request, 'list_provinces.html', {'provinces': provinces})

def list_districts(request):
    districts = District.objects.all()
    return render(request, 'list_districts.html',{'districts': districts})
def list_sectors(request, district_id, ):  # Replace district_id with the actual parameter
    sectors = Sector.objects.filter(district=district_id)
    return render(request, 'list_sectors.html', {'sectors': sectors})
def list_cells(request, sector_id, ):  # Replace sector_id with the actual parameter
    cells = Cell.objects.filter(sector=sector_id)
    return render(request, 'list_cells.html', {'cells': cells})
def list_villages(request, cell_id, ):  # Replace cell_id with the actual parameter
    villages = Village.objects.filter(cell=cell_id)
    return render(request, 'list_villages.html', {'villages': villages})


"""
# Dashboard for Admin
@login_required
def admin_dashboard(request):
    # Filter out users who have not verified their location
    unverified_users = User.objects.filter(location_verified=False)
    return render(request, 'admin_dashboard.html', {'users': unverified_users})

# Dashboard for Sedo Cell
@login_required
def sedo_cell_dashboard(request):
    return render(request, 'sedo_cell_dashboard.html')

# Dashboard for Sedo Sector
@login_required
def sedo_sec_dashboard(request):
    return render(request, 'sedo_sec_dashboard.html')

# Dashboard for Sedo District
@login_required
def sedo_dist_dashboard(request):
    return render(request, 'sedo_dist_dashboard.html')

# Dashboard for WASAC Manager
@login_required
def wasac_dashboard(request):
    return render(request, 'wasac_dashboard.html')

# Dashboard for General User
@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

# Location Verification Page
@login_required
def location_verification(request):
    return render(request, 'location_verification.html')

# Function to check if the user is an admin
def is_admin(user):
    return user.user_profile == 'admin'

# Verify Location by Admin
@login_required
@user_passes_test(is_admin)
def verify_location(request, user_id):
    # Get the user to be verified
    user = get_object_or_404(User, id=user_id)
    
    # Example of location check before verification
    if not user.province or not user.district:
        messages.error(request, 'User location is incomplete and cannot be verified.')
        return redirect('admin_dashboard')
    
    # Update location_verified to True
    user.location_verified = True
    user.save()
    
    # Provide a success message to the admin
    messages.success(request, f'Location for {user.names} has been successfully verified.')
    return redirect('admin_dashboard')
"""