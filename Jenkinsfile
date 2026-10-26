
pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Code checked out from GitHub'
            }
        }

        stage('Setup Python') {
            steps {
                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat '"%PYTHON%" -m pytest -v'
            }
        }
    }
}
