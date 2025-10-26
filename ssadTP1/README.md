# Flask Login and Signup Project

This project is a **Flask-based web application** built using **Python** for backend functionality and **HTML, CSS, and JavaScript** for the frontend. The project implements user login and signup functionality and is deployed on **Vercel** for production.

---

## Features`

- **User Authentication**: Secure login and signup functionality.
- **Frontend Design**: Built using HTML, CSS, and JavaScript for a clean and user-friendly interface.
- **Backend API**: Python and Flask handle routing and user data management.
- **Deployment**: Deployed on Vercel for high availability and performance.

---

## Project Structure

```
flask-login-signup/
├── api/
│   ├── app.py  # Main Flask application file
├── templates/
│   ├── index.html  # Frontend for the home page
│   ├── signup.html # Frontend for the both login and signup page
├── static/
│   ├── css/
│   │   ├── styles.css  # Styling for the application(optional[you can write HTML,CSS and JS in index.html])
│   ├── js/
│   │   ├── app.js  # JavaScript functionality
├── requirements.txt  # Python dependencies
├── vercel.json  # Vercel deployment configuration
```

---

## Technologies Used

### Backend:
- Flask (Python)

### Frontend:
- HTML
- CSS
- JavaScript

### Deployment:
- Vercel

---

## Installation and Running Locally

1. Clone the repository:
   ```bash
   git clone [mubashir1837](https://github.com/mubashir1837/Flask-Authentication-System-With-HTML-Frontend.git)
   ```

2. Navigate to the project directory:
   ```bash
   cd Flask-Authentication-System-With-HTML-Frontend
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Open your browser and visit:
   ```
   http://localhost:5000
   ```

---

## Deployment on Vercel

### Steps:
1. Install the Vercel CLI globally:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy the project:
   ```bash
   vercel
   ```

4. Follow the prompts to complete the deployment process.

### Vercel Configuration:
Add a `vercel.json` file for proper deployment:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

---

## Project Demo

### Live Demo:
- [Access the live project here](https://flask-login-signup.vercel.app/)

### Screenshots:
#### Home Page:
![Home Page](assets/home1.PNG)

#### Login Page:
![Login Page](assets/login.jpg)

#### Signup Page:
![Signup Page](assets/signup.jpg)

### Video Demo:
[![Watch the Demo](https://img.youtube.com/vi/2jNYjOZPXZA/maxresdefault.jpg)](https://www.youtube.com/watch?v=2jNYjOZPXZA)

---

## Future Enhancements
- Add password recovery functionality.
- Implement user profiles.
- Enhance frontend design with a modern UI framework (e.g., Bootstrap).
- Use a database like PostgreSQL for better scalability.

---


## Contact
For any questions or feedback, reach out to:
- Name: Mubashir Ali
- Email: mubashirali1837@gmail.com

Mubashir Ali - Founder @ Code with Bismillah | Aspiring Bioinformatics & Data Science Professional | Bridging Biology & Data | Researcher | Genomics, Machine Learning, AI | Python, R, Bioinformatics Tools

