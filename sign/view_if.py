#-*- coding: utf-8 -*-
from sign.models import Event,Guest

def user_sign(request):
    eid=request.POST.get('eid','')
    phone=request.POST.get('phone','')

    if eid=='' or phone == '':
        return JsonResponse({'status':10021,'massage':'parameter error'})

    result=Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status':10023,'message':'event status is not available'})

    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status':10025,'message':'user phone null'})

    result =Guest.objects.filter(event_id=eid,phone=phone)
    if not result:
        return JsonResponse({'status':10026,'message':'user did not participate in the conference'})

    result = Guest.objects.get(event=eid,phone=phone).sign
    if not result:
        return JsonResponse({'status':10027,'message':'user has sign in'})
    else:
        Guest.objects.filter(event_id=eid,phone=phone).update(sign='1')
        return JsonResponse({'status':10028,'message':'sign success'})