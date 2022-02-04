from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pickle

@csrf_exempt
def home(request):
    return render(request,"home.html")
def result(request):
    cs = float(request.POST['cs'])
    mip = float(request.POST['mip'])
    numunits = float(request.POST['numunits'])
    oclv = float(request.POST['oclv'])
    or_upb = float(request.POST['or_upb'])
    olv = float(request.POST['olv'])
    or_irate = float(request.POST['or_irate'])
    or_lterm = float(request.POST['or_lterm'])
    or_diratio=float(request.POST['or_diratio'])
    hm_flag = float(request.POST['hm_flag'])
    deli = float(request.POST['del'])
    hm_flag_NA=0
    hm_flag_N=0
    hm_flag_Y=0
    if(hm_flag==1):
        hm_flag_NA=1
    if(hm_flag==0):
        hm_flag_N=1
    if(hm_flag==2):
        hm_flag_Y=1
    deli_N=0
    deli_Y=0
    if(deli==0):
        deli_N=1
    if(deli==1):
        deli_Y=1
    if(cs>=0 and cs<500):
        cs_range=0
    if(cs>=500 and cs<550):
        cs_range=1
    if(cs>=550 and cs<600):
        cs_range=2
    if(cs>=600 and cs<650):
        cs_range=3
    if(cs>=650 and cs<700):
        cs_range=4
    if(cs>=700 and cs<750):
        cs_range=5
    if(cs>=750 and cs<800):
        cs_range=6
    if(cs>=800 and cs<=850):
        cs_range=7

    if(olv>=0 and olv<40):
        olv_range=0
    if(olv>=40 and olv<75):
        olv_range=1
    if(olv>=75 and olv<=100):
        olv_range=2

    test_point=[[cs, mip, numunits, oclv, or_diratio, or_upb, olv, or_irate, or_lterm, hm_flag_N, hm_flag_NA, hm_flag_Y, deli_N, deli_Y, cs_range, olv_range]]
    import pandas as pd

    test_point=pd.DataFrame(test_point)
    loaded_scale = pickle.load(open("scaler1.pkl", "rb"))
    test_point=loaded_scale.transform(test_point)
    test_point=pd.DataFrame(test_point)
    loaded_model = pickle.load(open("model1.pkl", "rb"))
    result = loaded_model.predict(test_point)
    alt1 = 'There will be no Prepayment'
    alt2 = 'There will be Prepayment'
    pred1={'prediction': alt1}
    pred2={'prediction': alt2}
    if result[0] == 0:
        return render(request,"result.html", pred1)
    else:
        return render(request,"result.html", pred2)
    return render(request,"result.html")
