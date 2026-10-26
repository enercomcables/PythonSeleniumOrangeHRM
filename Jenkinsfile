
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Code checked out from GitHub'
            }
        }

        stage('Setup Python') {
            steps {
                bat 'python --version'
                bat 'python -m pip --version'
                bat '"C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python314\\python.exe" --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat 'python -m pytest -v'
            }
        }
    }
}
