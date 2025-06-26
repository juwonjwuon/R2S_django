# safety/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignUpForm
from .models import Equipment, ChecklistItem, CheckLog

import qrcode
import io
import base64

@login_required
def home(request):
    return render(request, 'safety/home.html')

@login_required
def equipment_list(request):
    equipments = Equipment.objects.all()
    context = {'equipments': equipments}
    return render(request, 'safety/equipment_list.html', context)

@login_required
def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    checklist_items = ChecklistItem.objects.filter(category=equipment.category).order_by('order')
    check_logs = CheckLog.objects.filter(equipment=equipment).order_by('-checked_at')
    
    context = {
        'equipment': equipment,
        'checklist_items': checklist_items,
        'check_logs': check_logs,
    }
    return render(request, 'safety/equipment_detail.html', context)

@login_required
def submit_checklist(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    
    if request.method == 'POST':
        checklist_items = ChecklistItem.objects.filter(category=equipment.category)
        
        for item in checklist_items:
            result_key = f'result_{item.pk}'
            notes_key = f'notes_{item.pk}'
            photo_key = f'photo_{item.pk}'
            
            result_value = request.POST.get(result_key)
            notes_value = request.POST.get(notes_key, '')
            photo_file = request.FILES.get(photo_key)
            
            if result_value:
                CheckLog.objects.create(
                    equipment=equipment,
                    item=item,
                    inspector=request.user,
                    result=result_value,
                    notes=notes_value,
                    photo=photo_file,
                )
        
        return redirect('equipment_detail', pk=equipment.pk)
    
    return redirect('equipment_detail', pk=equipment.pk)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'safety/signup.html', {'form': form})

@login_required
def delete_log(request, pk):
    log_to_delete = get_object_or_404(CheckLog, pk=pk)

    equipment_pk = log_to_delete.equipment.pk

    if request.method == 'POST':
        log_to_delete.delete()
        return redirect('equipment_detail', pk=equipment_pk)

    context = {'log': log_to_delete}
    return render(request, 'safety/log_confirm_delete.html', context)

@login_required
def qr_code_list(request):
    equipments = Equipment.objects.all()
    qr_codes_data = []

    for equipment in equipments:
        url = request.build_absolute_uri(f'/safety/equipment/{equipment.pk}/')

        qr_img = qrcode.make(url)
        buffer = io.BytesIO()
        qr_img.save(buffer, format='PNG')


        qr_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        qr_codes_data.append({
            'name': equipment.name,
            'id_str': f"ID: EQP-{equipment.pk:03d}", 
            'qr_image_b64': qr_b64,
        })

    context = {'qr_codes_data': qr_codes_data}
    return render(request, 'safety/qr_code_list.html', context)