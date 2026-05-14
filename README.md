# WhatsApp Customer Churn Prediction Bot

A WhatsApp bot built with Flask and Twilio that predicts bank customer churn in real time using a trained Logistic Regression model.

---

## About the Project

This project is a WhatsApp bot that predicts whether a bank customer will churn or stay. It is built as a real world deployment extension of the Customer Churn Prediction project. A user simply sends 11 customer feature values as a WhatsApp message and the bot instantly replies with a prediction and confidence score.

```
Model       :  Logistic Regression
Dataset     :  Churn_Modelling.csv
Input       :  11 customer feature values via WhatsApp
Output      :  Churn prediction with confidence score
```

---

## Project Structure

```
WhatsApp Bot/
│
├── app.py                   # Main Flask app and WhatsApp webhook
├── preprocessing.py         # Parses and validates incoming message
├── train_and_save.py        # Trains the model and saves artifacts
│
├── artifacts/
│   ├── model.pkl            # Saved Logistic Regression model
│   └── scaler.pkl           # Saved StandardScaler
│
└── ngrok.exe                # Exposes local server to the internet
```

---

## How It Works

**Step 1: Model Training**
The Churn Modelling dataset was loaded and preprocessed by dropping irrelevant columns like RowNumber, CustomerId, and Surname. Geography and Gender were encoded using one-hot encoding and all features were scaled using StandardScaler. A Logistic Regression model was trained and both the model and scaler were saved as pickle files inside the artifacts folder.

**Step 2: Flask Server**
A Flask web server was created with two routes. A health check route at the root URL confirms the server is running. The main webhook route at /whatsapp receives incoming messages from Twilio, processes them, and returns a prediction.

**Step 3: WhatsApp Integration via Twilio**
Twilio was used to connect the Flask server to WhatsApp. When a user sends a message, Twilio forwards it to the Flask webhook. The bot parses the 11 feature values from the message, scales them, runs the prediction, and sends the result back to the user on WhatsApp.

**Step 4: Ngrok**
Ngrok was used to create a public URL that tunnels to the local Flask server so Twilio could reach the webhook from the internet.

---

## Input Format

Send 11 numbers in the following order as a WhatsApp message:

```
CreditScore, Age, Tenure, Balance, NumOfProducts,
HasCrCard, IsActiveMember, EstimatedSalary,
IsGermany(0/1), IsSpain(0/1), IsMale(0/1)
```

Example message:
```
619, 42, 2, 0.0, 1, 1, 1, 101348.88, 0, 0, 0
```

---

## Bot Response Format

```
🏦 Customer Churn Prediction
──────────────────
Result     :  Not Churned (Stay) ✅  or  Churned (Will Leave) ⚠️
Confidence :  87.34%
```

---

## Technologies Used

- Python 3
- Flask
- Twilio API
- Scikit-learn
- Joblib
- Ngrok

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/WhatsApp-Churn-Bot.git
   ```

2. Install required libraries:
   ```bash
   pip install flask twilio scikit-learn joblib pandas numpy
   ```

3. Train the model and save artifacts:
   ```bash
   python train_and_save.py
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```

5. In a separate terminal, start Ngrok to expose the server:
   ```bash
   ngrok http 5000
   ```

6. Copy the Ngrok public URL and set it as the WhatsApp webhook in your Twilio console:
   ```
   https://your-ngrok-url/whatsapp
   ```

7. Send a message to your Twilio WhatsApp number with the 11 feature values and receive a prediction instantly.

---

## 📝 License

This project is intended for **academic and non-commercial use only**.

---

## 📧 Author

**Fawad Saqib**
💬 Reach out via GitHub for feedback or collaboration!
