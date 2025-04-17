from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SensorData
from django.contrib.auth.decorators import login_required
from .forms import SensorDataForm  # import SensorDataForm


#@csrf_exempt
#def receive_sensor_data(request):
    #""" รับข้อมูลจากเซ็นเซอร์ที่ส่งมาจากบอร์ด (ผ่าน HTTP POST) """
    #if request.method == "POST":
        #try:
            #data = json.loads(request.body.decode("utf-8"))  # แปลง JSON เป็น Python Dict
            #user_id = data.get("user_id")  # รับ user_id จาก request
            #heart_rate = data.get("heart_rate")
            #skin_temperature = data.get("skin_temperature")
            #ambient_temperature = data.get("ambient_temperature")
            #humidity = data.get("humidity")
            #skin_resistance = data.get("skin_resistance")
#
            ## ตรวจสอบว่าผู้ใช้มีอยู่ในระบบหรือไม่
            ##from django.contrib.auth import get_user_model
            ##User = get_user_model()
            ##user = User.objects.get(id=user_id)
#
            ## บันทึกข้อมูลลงฐานข้อมูล
            #sensor_data = SensorData.objects.create(
                #user=user,
                #heart_rate=heart_rate,
                #skin_temperature=skin_temperature,
                #ambient_temperature=ambient_temperature,
                #humidity=humidity,
                #skin_resistance=skin_resistance,
            #)
#
            #return JsonResponse({"message": "Sensor data received successfully!"}, status=201)
#
        #except Exception as e:
            #return JsonResponse({"error": str(e)}, status=400)
#
    #return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def receive_sensor_data(request):
    if request.method == "POST":
        form = SensorDataForm(request.POST)
        if form.is_valid():
            # ตั้งค่า user เป็นผู้ใช้ที่ล็อกอินอยู่
            sensor_data = form.save(commit=False)
            sensor_data.user = request.user  # ตั้งค่า user เป็นผู้ใช้ที่ล็อกอิน
            sensor_data.save()  # บันทึกข้อมูล
            return redirect('sensor:display_data')  # เปลี่ยนไปที่หน้ารายการข้อมูล
    else:
        form = SensorDataForm()

    return render(request, 'sensor_data_form.html', {'form': form})


@login_required
def display_data(request):
    """ แสดงข้อมูลเซ็นเซอร์ของผู้ใช้ """
    sensor_data = SensorData.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "sensor/display_data.html", {"sensor_data": sensor_data})