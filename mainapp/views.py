from django.shortcuts import render,HttpResponse
import pandas as pd
from .models import *
import os,pickle
from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(max_depth=2, random_state=0)

# Create your views here.
def home(request):
    return render(request,'mainapp/navigation.html')

def input_(request):
    return render(request,'mainapp/input.html')

def faqpage_(request):
    return render(request,'mainapp/faqpage.html')


def process_input(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        age = int(request.GET.get('age'))
        weight = float(request.GET.get('weight'))
        height = float(request.GET.get('height'))
        gender = request.GET.get('gender')
        a_l = int(request.GET.get('a_l'))
        disease = request.GET.get("disease")
        
        
        d = {}
        l = [1.2,1.3,1.5,1.7,1.9]
        for i,j in zip(range(1,6),l):
            d[i] = j

        df = pd.DataFrame({
        'name': [name],
        'age':[age],
        'weight(kg)':[weight],
        'height(m)':[height],
        'gender':[gender],
        'activity_level':d[a_l]
        })
        
        df['BMI'] = round(df['weight(kg)'] / (df['height(m)'] * df['height(m)']),2)
        if gender=='M':
            BMR = round((66 + (13.7*df.loc[0,'weight(kg)']) + (5*(df.loc[0,'height(m)']*100)) - (6.8*df.loc[0,'age'])),2)
        elif gender=='F':
            BMR = round((655 + (9.6*df.loc[0,'weight(kg)']) + (1.7*(df.loc[0,'height(m)']*100)) - (4.7*df.loc[0,'age'])),2)
        df['BMR'] = [BMR]
        df['calories_to_maintain_weight'] = df.BMR*df.activity_level
        #print(df)

        obj = records_users(name=name,age=age, weight=weight, height=height, gender=gender, a_l=d[a_l],bmi = df.loc[0,'BMI'] , bmr = df.loc[0,'BMR'] , ctmw = df.loc[0,'calories_to_maintain_weight'])
        obj.save()

 
        #with open('mainapp/model/dumped_model.pkl', 'rb') as fid:
        #    clf = pickle.load(fid)

        maindf = pd.read_csv('mainapp/model/Dataset.csv')
        X = maindf[['calories_to_maintain_weight']]
        y = maindf['Label']

        clf.fit(X, y)

        with open('mainapp/model/label_dict.pickle', 'rb') as handle:
            b = pickle.load(handle)

        pred = clf.predict([[float(df.loc[0,'calories_to_maintain_weight'])]])
        pred = b[pred[0]]
        tag_bmi = int(pred[0])
        file_to_open = [pred[1:]][0]
        print(tag_bmi,file_to_open)

        lab = {7:'Under weight' , 8 : 'Normal ', 9: 'Over weight'}

        tag_bmi = lab[tag_bmi]
        dfd = pd.read_excel('mainapp/model/36_Diet_Plans_renamed_r/'+pred+'.xlsx')
        dfd = dfd.fillna('')
        format_dict = {'Calories':"{:.5}",'Carbs(g)':"{:.5}",'Fats(g)':"{:.5}",'Proteins(g)':"{:.5}"}
        list=['Breakfast',"Lunch","Dinner","Mid morning snacks","Snacks"]
        style1 = dfd.style.apply(lambda x:['background: #64DF31' if x in list else ('background:orange' if x=="Total" or x=="Total:" or x=="Total " else'background: white') for x in dfd.Calories_required],axis=0).format(format_dict).hide_index().set_table_styles([{'selector': 'th,td', 'props': [('font-size', '12pt'),('border-style','solid'),('border-width','1px')]}])
        dfd = style1.render()        

        if disease=='None':
            return render(request,'mainapp/display_outputs.html',{'bmi':df.loc[0,'BMI'] , 'bmr':df.loc[0,'BMR'] , 'ctm':df.loc[0,'calories_to_maintain_weight'] , 'dfd':dfd ,'tag_bmi':tag_bmi})
        else:
            dfd = ''
            name_of_file_disease = []
            for i in os.listdir('mainapp/model/chronic_disease_diet_plans'):
                if file_to_open in i:
                    name_of_file_disease.append(i)
            print('>>>>>',name_of_file_disease)
            for i in name_of_file_disease:
                print(disease.lower() , i.lower())
                if disease.lower() in i.lower():
                    dfd2 = pd.read_excel('mainapp/model/chronic_disease_diet_plans/'+i)
                    dfd2 = dfd2.fillna('')
                    
                    list=['Breakfast',"Lunch","Dinner","Mid morning snacks","Snacks"]
                    style1 = dfd2.style.apply(lambda x:['background: #64DF31' if x in list else ('background:orange' if x=="Total" or x=="Total:" or x=="Total " else'background: white') for x in dfd2.Calories_required],axis=0).format(format_dict).hide_index().set_table_styles([{'selector': 'th,td', 'props': [('font-size', '12pt'),('border-style','solid'),('border-width','1px')]}])
                    dfd2 = style1.render()


            heading_dict = {
              'Diabetes' : f'Diet Plan for Diabetes for {file_to_open} calories',
              'Blood'    : f'Diet Plan for Blood Pressure for {file_to_open} calories',
              'Uric'    : f'Diet Plan for Uric Acid for {file_to_open} calories',
              'Asthama'    : f'Diet Plan for Asthama for {file_to_open} calories',
              'Heart'    : f'Diet Plan for Heart for {file_to_open} calories',
            }


    return render(request,'mainapp/display_outputs.html',{'bmi':df.loc[0,'BMI'] , 'bmr':df.loc[0,'BMR'] , 'ctm':df.loc[0,'calories_to_maintain_weight'] , 'dfd':dfd ,'tag_bmi':tag_bmi,'dfd2':dfd2,'heading':heading_dict[disease] })

def about(request):
    return render(request,f'mainapp/aboutpage.html')


def faq(request):
    return render(request,f'mainapp/faqpage.html')



def experts(request):
    return render(request,'mainapp/expertpage.html')



def nutrition(request):
    return render(request, 'mainapp/nutrition.html')

def food(request):
    return render(request, 'mainapp/foodpage.html')
from sqlalchemy import create_engine
def search(request):
    if request.method=="GET":
        query = request.GET.get('results')
        df = pd.read_excel('mainapp/model/new.xlsx')
        try:
            engine = create_engine('sqlite:///save_pandas.sqlite3', echo=True)
            sqlite_connection = engine.connect()
            #df.to_sql('database', sqlite_connection, if_exists='fail')
        except:
            pass
        data = df.query('English=="{}" or Urdu=="{}" or Scientific=="{}"'.format(query,query,query))
        if len(data)>0:
            return render(request, 'mainapp/results_n.html',{"data":data.to_html()})
        else:
            data = "<h1>Oops! No record found</h1>"
            return render(request, 'mainapp/results_n.html',{"data":data})
