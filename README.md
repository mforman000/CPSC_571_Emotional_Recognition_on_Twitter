# CPSC_571_Emotional_Recognition_on_Twitter 

## Matthew Forman, Firoz Lahkani, Rohan Chaudhary

Please install the following python libraries:

```
pip install wordcloud

pip install scikit-learn
```

In order to run our program, ensure you have Django installed on your system. To do so you can run:

```
pip install django
```
If you run into an issue where django cannpt be found into you may need to install load a django virtual environmen into this folder. To do so you can run:

```
python -m venv django-env

source django-env/bin/activate
```

Now you can try installing. 

If these are already installed or once you have already installed the above libraries please navigate into the TweetRecognition directory.

```
cd TweetRecognition
```

Now you can run the server using the following command:

```
python manage.py runserver
```

Once you've run this command you can navigate to http://127.0.0.1:8000/

From here you can Toggle through the drop down to view different results for datasets that we have run our model on. 

