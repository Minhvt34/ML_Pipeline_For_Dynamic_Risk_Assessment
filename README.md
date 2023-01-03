# Build an ML Pipeline For Dynamic Risk Assessment
This repo is created to build a completed Machine Learning pipeline from Data Ingestion, Training, scoring, and deploying, plus Process Automation

## Project Overview

- [Getting started](#project-overview)
   * [Prerequisites](#prerequisites)
   * [The workspace locations](#the-workspace-locations)
   * [Dependencies](#dependencies)
- [Data Ingestion](#data-ingestion)
- [Training, Scoring, and Deploying](#training-scoring-and-deploying)
- [Diagnostics](#diagnostics)
- [Reporting](#reporting)
- [Process Automation](#process-automation)
- [Optional process](#optional-process)
- [Usage](#usage)

## Getting started
### Prerequisites
- Python 3.x
- The Workspace: Linux environment

### The workspace locations
```bash
# workspace

* [ingesteddata/](./workspace/ingesteddata/)                   #Contains the compiled datasets after ingestion script
* [model/](./workspace/model/)                                 #Contains ML models that creates for production
* [practicedata/](./workspace/practicedata/)                   #Contains data for practice
* [practicemodels/](./workspace/practicemodels/)               #Contains practicemodels that creates as practice
* [production_deployment/](./workspace/production_deployment/) #Contains final, deployed ML models
* [sourcedata/](./workspace/sourcedata/)                       #Contains data for training practice
* [testdata/](./workspace/testdata/)                           #Contains data for testing practice
* [training.py](./workspace/training.py)                       #a Python script meant to train an ML model
* [scoring.py](./workspace/scoring.py)                         #a Python script meant to score an ML model
* [deployment.py](./workspace/deployment.py)                   #a Python script meant to deploy a trained ML model
* [ingestion.py](./workspace/ingestion.py)                     #a Python script meant to ingest new data
* [diagnostics.py](./workspace/diagnostics.py)                 #a Python script meant to measure model and data diagnostics
* [reporting.py](./workspace/reporting.py)                     #a Python script meant to generate reports about model metrics
* [app.py](./workspace/app.py)                                 #a Python script meant to contain API endpoints
* [wsgi.py](./workspace/wsgi.py)                               #a Python script to help with API deployment
* [apicalls.py](./workspace/apicalls.py)                       #a Python script meant to call your API endpoints
* [fullprocess.py](./workspace/fullprocess.py)                 #a Python script meant to determine whether a model needs to be re-deployed, and to call all other Python scripts when needed
* [pretty_confusion_matrix.py](./workspace/pretty_confusion_matrix.py)        #a Python script meant to calculate, and save confusion matrix 
* [config.py](./workspace/config.py)                           #a Python script meant to read 'config.json' ans define config macros
* [config.json](./workspace/config.json)                       #a config file contains data, and model directions
* [requirements.txt](./workspace/requirements.txt)             #contains requirements packages
```

### Dependencies
All dependencies is listed in the ```requirements.txt``` file.

## Data Ingestion
- Automatically detect all the csv files in the directory specified in the input folder path - used for training. Then, combining all these in a single dataframe and de-dupe the dataframe to ensure that it contains unique rows.

## Training, Scoring, and Deploying
1. **Model training:**  Train an ML model that predicts attrition risk.
2. **Model Scoring:** Scoring model performance by calculating F1 score of the trained model on a testing data.
3. **Model deploying:** Normally copy the trained model (pickle file), model score (txt file) and a recored data of the ingested data to a production deployment direction.

## Diagnostics
1. **Missing data:** Detect missing data (NA values), count the number of NA values in each column in the dataset and calculate what percent of each column consists of NA values.

2. **Timing:** Time measurement for data ingestion, and model training.

3. **Dependencies:** Check whether the module dependencies are up-to-date, output results as a table with three columns: the first column will show the name of a Python module that you're using; the second column will show the currently installed version of that Python module, and the third column will show the most recent available version of that Python module.

## Reporting
1. **Generating Plots:** Plot confusion matrix on obtained predicted values and actual values for the data.

2. **Flask API setup:** Create API to easily access ML diagnostics and results with four endpoints: one for model predictions, one for model scoring, one for summary statistics, and one for other diagnostics.

## Process Automation
- Automate the ML model scoring and mornitoring process.
- Check for the criteria that will require mode re-deployment, and re-deploying models as necessary.

1. **Checking and Reading New Data:** check whether any new data exists that need to be ingested (new file (if exists) appears in `input_folder_path`)
2. **Deciding whether to proceed (first time):** If previous step is no new data, there will be no need to check for model drift, if not, need to continue to next step.

3. **Checking for Model Drift:** Evaluating model performance on new data, and comparing with model prediction on previous data (based on recored model score). If the score id lower, compares to precious one, the model drift has occured. Otherwise, it has not.

4. **Deciding whether to proceed (second time):** If in the step 3, there is no model drift, it means that the current model is working well. Otherwise, we need to move to next step.

5. **Re-training:** Train a new model using the most recent data which is obtained from the previous "Checking and Reading new data" step. Using `training.py` to complete this step, and a model trained on the most recent data will be saved in the workspace.

6. **Re-deployment:** Run script `deployment.py` to deploy the new trained model.

7. **Diagnostics and Reporting:** Use script `reporting.py` and `apicalls.py` on the most recently deployed model.

## Process Automation
- **Cron job for the Full Pipeline:** Write a crontab file that runs the `fullprocess.py` script one time every, say, `X` min.

## Optional process
1. **PDF reports**
In Step 4 "Reporting", you set up a script that generates a plot of a confusion matrix. Instead of outputting just that raw plot, set up a script that generates a pdf file that contains the plot as well as summary statistics and other diagnostics. This enables more complete, quicker reporting that will really make your project stand out.

In order to accomplish this suggestion, you'll need to add to your reporting.py Python script. You may also need to install modules that enable PDF creation, such as the reportlab module. There are many things you could include in a PDF report about your model: you could include the confusion matrix you generate in reporting.py, you could include all of the outputs of API endpoints you created in app.py, and you could also include the model's F1 score (stored in latestscore.txt) and the files that you ingested to train the model (stored in ingestedfiles.txt).

2. **Time Trends**
Give your scripts the ability to store diagnostics from previous iterations of your model, and generate reports about time trends. For example, show how the percent of NA elements has gone up or down over many weeks or months, or show whether the timing of ingestion and training has increased or decreased.

You could accomplish this suggestion in several different ways. For example, you could create a directory called /olddiagnostics/, and create a script that copied all of your diagnostics outputs to that folder. You could also add timestamps to the filenames of your output files like ingestedfiles.txt and latestscore.txt.

3. **Database setup**
Instead of writing results and files to .txt and .csv files, write your datasets and records to SQL databases. This will lead to increased performance and reliability.

In order to accomplish this suggestion, you'll have to set up SQL databases in your workspace. You can accomplish this within Python by installing and using the mysql-connector-python module. You could create a new Python script called dbsetup.py that used this module to set up databases. You could set up a database that stored information about ingested files, another one to store information about model scores, and another one to store information about model diagnostics. Then, you would have to alter ingestion.py, scoring.py, and diagnostics.py so that they wrote to these databases every time they were run.

## Usage

### 1- Edit config.json file to use practice data

```bash
"input_folder_path": "practicedata",
"output_folder_path": "ingesteddata", 
"test_data_path": "testdata", 
"output_model_path": "practicemodels", 
"prod_deployment_path": "production_deployment"
```

### 2- Run data ingestion
```python
cd src
python ingestion.py
```
Artifacts output:
```
data/ingesteddata/finaldata.csv
data/ingesteddata/ingestedfiles.txt
```

### 3- Model training
```python
python training.py
```
Artifacts output:
```
models/practicemodels/trainedmodel.pkl
```

###  4- Model scoring 
```python
python scoring.py
```
Artifacts output: 
```
models/practicemodels/latestscore.txt
``` 

### 5- Model deployment
```python
python deployment.py
```
Artifacts output:
```
models/prod_deployment_path/ingestedfiles.txt
models/prod_deployment_path/trainedmodel.pkl
models/prod_deployment_path/latestscore.txt
``` 

### 6- Run diagnostics
```python
python diagnostics.py
```

### 7- Run reporting
```python
python reporting.py
```
Artifacts output:
```
models/practicemodels/confusionmatrix.png
models/practicemodels/summary_report.pdf
```

### 8- Run Flask App
```python
python app.py
```

### 9- Run API endpoints
```python
python apicalls.py
```
Artifacts output:
```
models/practicemodels/apireturns.txt
```

### 11- Edit config.json file to use production data

```bash
"input_folder_path": "sourcedata",
"output_folder_path": "ingesteddata", 
"test_data_path": "testdata", 
"output_model_path": "models", 
"prod_deployment_path": "production_deployment"
```

### 10- Full process automation
```python
python fullprocess.py
```
### 11- Cron job

Start cron service
```bash
sudo service cron start
```

Edit crontab file
```bash
sudo crontab -e
```
   - Select **option 3** to edit file using vim text editor
   - Press **i** to insert a cron job
   - Write the cron job in ```cronjob.txt``` which runs ```fullprocces.py``` every 10 mins
   - Save after editing, press **esc key**, then type **:wq** and press enter
  
View crontab file
```bash
sudo crontab -l
```

## Resources

- Flask
  - https://pythonbasics.org/flask-http-methods/
  - https://www.sqlshack.com/create-rest-apis-in-python-using-flask/
  - https://medium.com/@shanakachathuranga/end-to-end-machine-learning-pipeline-with-mlops-tools-mlflow-dvc-flask-heroku-evidentlyai-github-c38b5233778c

- Reportlab
  - https://www.youtube.com/playlist?list=PLOGAj7tCqHx-IDg2x6cWzqN0um8Z4plQT
  - https://www.reportlab.com/docs/reportlab-userguide.pdf