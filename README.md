# Project Setup

1. **Create Virtual Environment:**
   - Set up a virtual environment by running the following command:
     ```
     python -m venv env
     ```

2. **Activate Virtual Environment:**
   - Activate the virtual environment using:
     ```
     env\Scripts\activate
     ```

3. **Navigate to Backend Directory:**
   - Change to the backend directory:
     ```
     cd ./backend
     ```

4. **Upgrade Pip (if necessary):**
   - Ensure you have the latest version of pip:
     ```
     python.exe -m pip install --upgrade pip
     ```

5. **Install Dependencies:**
   - Install the required packages:
     ```
     pip install djangorestframework-simplejwt
     pip install pillow
     pip install django-cors-headers
     pip install psycopg2
     ```

6. **Database Migration:**
   - Make migrations using the following command:
     ```
     python manage.py makemigrations
     ```

7. **Apply Migrations:**
   - Migrate the database:
     ```
     python manage.py migrate
     ```

8. **Run the Development Server:**
   - Ensure you are in the backend folder and execute the following command, replacing `<localserver:port>` with your desired local server and port:
     ```
     python manage.py runserver <localserver:port>
     ```
