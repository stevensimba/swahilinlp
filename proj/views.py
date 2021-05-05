from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    pred = 0
    if request.method == "POST":
       swa_input =  request.POST.get("swa-input")

       if swa_input == "steve":
           pred = 0
       else:
            pred = 1
       # make a prediction and send the output in Json format
       return JsonResponse({"prediction": pred}, status=200)
    return render(request, "home.html")


import  pandas  as  pd  
import  pickle
from  sklearn.feature_extraction.text  import  CountVectorizer
from  sklearn.feature_extraction.text  import  TfidfTransformer
from  sklearn.feature_extraction.text  import  TfidfVectorizer
from  sklearn.naive_bayes  import  MultinomialNB
tfidf  =  TfidfVectorizer(sublinear_tf=True,  min_df=5,  norm='l2',  ngram_range=(1,  1))
import  joblib


df  =  pd.read_csv('./proj/data.csv')
df  =  df[pd.notnull(df['content'])]
df['category_id']  =  df['category'].factorize()[0]
from  io  import  StringIO
category_id_df  =  df[['category',  'category_id']].drop_duplicates().sort_values('category_id')
category_to_id  =  dict(category_id_df.values)
id_to_category  =  dict(category_id_df[['category_id',  'category']].values)
#  Features  and  Labels
features  =  tfidf.fit_transform(df.content).toarray()
labels  =  df.category_id
from  sklearn.model_selection  import  train_test_split


def  predict(request):
  #  LSV_swahili_model  =  open('LSV_Swahili_model.pkl','rb')
  pred  =  0
  text  =  ""
  habari = ["Maswala ya Kiuchumi", "Habari za Kitaifa", "Jarida la Michezo", "Dira za Kimataifa", "Raha na Burudani", "Mambo ya Afya"]

  nb_swahili_model  =  open('./proj/nb1_Swahili_model.pkl','rb')
  model  =  joblib.load(nb_swahili_model)

  if  request.method  ==  'POST':
    message  =  request.POST.get('swa-input')
    data  =  [message]

    vect  =  tfidf.transform(data).toarray()
    
    my_prediction  =  model.predict(vect).tolist()[0]

    return  JsonResponse({"prediction":  my_prediction,  "message":  habari[my_prediction]})
    #  my_prediction=  id_to_category[my_prediction[0]]
  return  render(request, 'index.html')
