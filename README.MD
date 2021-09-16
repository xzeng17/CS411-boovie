Virtual environment for flask:      
$ python3 -m venv venv      

Activate the environment:       
bash: $ . venv/bin/activate       
windows: > venv\Scripts\activate     

Run Locally:   
pip install -r requirements.txt          
bash: $ export FLASK_APP=flaskr && export FLASK_ENV=development && flask run      
windows: > $env:FLASK_APP = "flaskr";$env:FLASK_ENV = "development";flask run        

Backend:        
Staging: https://boovie-staging.herokuapp.com/      
Production: https://boovie-production.herokuapp.com/        