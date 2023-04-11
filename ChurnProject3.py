import gradio as gr
import pickle
import pandas as pd
import numpy as np
import joblib
from PIL import Image


num_imputer = joblib.load('numerical_imputer.joblib')
cat_imputer = joblib.load('categorical_imputer.joblib')
encoder = joblib.load('encoder.joblib')
scaler = joblib.load('scaler.joblib')
model = joblib.load('Final_model.joblib')


# Create a function that applies the ML pipeline and makes predictions
def predict(gender,SeniorCitizen,Partner,Dependents, tenure, PhoneService,MultipleLines,
                       InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,
                       Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges):



    # Create a dataframe with the input data
     input_df = pd.DataFrame({
        'gender': [gender],
        'SeniorCitizen': [SeniorCitizen],
        'Partner': [Partner],
        'Dependents': [Dependents],
        'tenure': [tenure],
        'PhoneService': [PhoneService],
        'MultipleLines': [MultipleLines],
        'InternetService': [InternetService],
        'OnlineSecurity': [OnlineSecurity],
        'OnlineBackup': [OnlineBackup],
        'DeviceProtection': [DeviceProtection],
        'TechSupport': [TechSupport],
        'StreamingTV': [StreamingTV],
        'StreamingMovies': [StreamingMovies],
        'Contract': [Contract],
        'PaperlessBilling': [PaperlessBilling],
        'PaymentMethod': [PaymentMethod],
        'MonthlyCharges': [MonthlyCharges],
        'TotalCharges': [TotalCharges]

 })

# Selecting categorical and numerical columns separately
     cat_columns = [col for col in input_df.columns if input_df[col].dtype == 'object']
     num_columns = [col for col in input_df.columns if input_df[col].dtype != 'object']

    # Apply the imputers on the input data
     input_df_imputed_cat = cat_imputer.transform(input_df[cat_columns])
     input_df_imputed_num = num_imputer.transform(input_df[num_columns])

    # Encode the categorical columns
     input_encoded_df = pd.DataFrame(encoder.transform(input_df_imputed_cat).toarray(),
                                   columns=encoder.get_feature_names_out(cat_columns))

    # Scale the numerical columns
     input_df_scaled = scaler.transform(input_df_imputed_num)
     input_scaled_df = pd.DataFrame(input_df_scaled , columns = num_columns)


    #joining the cat encoded and num scaled
     final_df = pd.concat([input_encoded_df, input_scaled_df], axis=1)

     final_df = final_df.reindex(columns=['SeniorCitizen','tenure','MonthlyCharges','TotalCharges',
     'gender_Female','gender_Male','Partner_No','Partner_Yes','Dependents_No','Dependents_Yes','PhoneService_No',
     'PhoneService_Yes','MultipleLines_No','MultipleLines_Yes','InternetService_DSL','InternetService_Fiber optic',
     'InternetService_No','OnlineSecurity_No','OnlineSecurity_Yes','OnlineBackup_No','OnlineBackup_Yes','DeviceProtection_No',
     'DeviceProtection_Yes','TechSupport_No','TechSupport_Yes','StreamingTV_No','StreamingTV_Yes','StreamingMovies_No',
     'StreamingMovies_Yes','Contract_Month-to-month','Contract_One year','Contract_Two year','PaperlessBilling_No',
     'PaperlessBilling_Yes','PaymentMethod_Bank transfer (automatic)','PaymentMethod_Credit card (automatic)','PaymentMethod_Electronic check',
     'PaymentMethod_Mailed check'])

    # Make predictions using the model
     predictions = model.predict(final_df)

     # Make predictions using the model
     #predictions = model.predict(final_df)

     # Convert the numpy array to an integer
     #prediction_label = int(predictions.item())

     prediction_label = "Beware!!! This customer is likely to Churn" if predictions.item() == "Yes" else "This customer is Not likely churn"


     return prediction_label

     #return predictions

input_interface=[]
with gr.Blocks(css=".gradio-container {background-color: powderblue}") as app:
    img = gr.Image("C:/Users/user/Documents/AZUBI PROGRAM/CAREER ACELERATOR/LP4-buiding an app/Gradio/lp4_part2-1/telecom churn.png").style(height='13')

    Title=gr.Label('CUSTOMER CHURN PREDICTION APP')

    with gr.Row():
        Title
    with gr.Row():
        img

#with gr.Blocks() as app:
#    with gr.Blocks(css=".gradio-interface-container {background-color: powderblue}"):
        #with gr.Row():
        #    gr.Label('Customer Churn Prediction Model')
    with gr.Row():
        gr.Markdown("This app predicts whether a customer will leave your company or not. Enter the details of the customer below to see the result")

    #with gr.Row():
        #gr.Label('This app predicts whether a customer will leave your company or not. Enter the details of the customer below to see the result')


    with gr.Row():
        with gr.Column(scale=3, min_width=600):

            input_interface = [
                gr.components.Radio(['male', 'female'], label='Select your gender'),
                gr.components.Number(label="Are you a Seniorcitizen; No=0 and Yes=1"),
                gr.components.Radio(['Yes', 'No'], label='Do you have Partner'),
                gr.components.Dropdown(['No', 'Yes'], label='Do you have any Dependents? '),
                gr.components.Number(label='Lenght of tenure (no. of months with Telco)'),
                gr.components.Radio(['No', 'Yes'], label='Do you have PhoneService? '),
                gr.components.Radio(['No', 'Yes'], label='Do you have MultipleLines'),
                gr.components.Radio(['DSL', 'Fiber optic', 'No'], label='Do you have InternetService'),
                gr.components.Radio(['No', 'Yes'], label='Do you have OnlineSecurity?'),
                gr.components.Radio(['No', 'Yes'], label='Do you have OnlineBackup?'),
                gr.components.Radio(['No', 'Yes'], label='Do you have DeviceProtection?'),
                gr.components.Radio(['No', 'Yes'], label='Do you have TechSupport?'),
                gr.components.Radio(['No', 'Yes'], label='Do you have StreamingTV?'),
                gr.components.Radio(['No', 'Yes'], label='Do you have StreamingMovies?'),
                gr.components.Dropdown(['Month-to-month', 'One year', 'Two year'], label='which Contract do you use?'),
                gr.components.Radio(['Yes', 'No'], label='Do you prefer PaperlessBilling?'),
                gr.components.Dropdown(['Electronic check', 'Mailed check', 'Bank transfer (automatic)',
                                        'Credit card (automatic)'], label='Which PaymentMethod do you prefer?'),
                gr.components.Number(label="Enter monthly charges"),
                gr.components.Number(label="Enter total charges")
            ]

    with gr.Row():
        submit_btn = gr.Button('Submit')

        predict_btn = gr.Button('Predict')

# Define the output interfaces
    output_interface = gr.Label(label="churn")

    predict_btn.click(fn=predict, inputs=input_interface, outputs=output_interface)




app.launch(share=True)
