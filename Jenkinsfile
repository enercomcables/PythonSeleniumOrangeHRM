
pipeline {
    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
        buildDiscarder(logRotator(
            numToKeepStr: '20'
        ))
    }

    parameters {
        choice(
            name: 'TEST_MARKER',
            choices: ['all', 'smoke', 'regression'],
            description: 'Select the test group'
        )
    }

    environment {
        HEADLESS = 'true'
        BROWSER = 'chrome'
        BASE_URL = 'https://opensource-demo.orangehrmlive.com/'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Execute Tests') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'orangehrm-test-credentials',
                        usernameVariable: 'ORANGEHRM_USERNAME',
                        passwordVariable: 'ORANGEHRM_PASSWORD'
                    )
                ]) {
                    sh '''
                        mkdir -p reports logs screenshots

                        if [ "$TEST_MARKER" = "all" ]; then
                            .venv/bin/python -m pytest \
                                -v \
                                --html=reports/report.html \
                                --self-contained-html
                        else
                            .venv/bin/python -m pytest \
                                -v \
                                -m "$TEST_MARKER" \
                                --html=reports/report.html \
                                --self-contained-html
                        fi
                    '''
                }
            }
        }
    }

    post {
        always {
            publishHTML(target: [
                reportName: 'Pytest HTML Report',
                reportDir: 'reports',
                reportFiles: 'report.html',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: true
            ])

            archiveArtifacts(
                artifacts: 'reports/**,logs/**,screenshots/**',
                allowEmptyArchive: true
            )

            cleanWs()
        }
    }
}
