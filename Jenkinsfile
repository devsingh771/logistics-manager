pipeline {
    agent any
    stages {
        stage('Initialize') {
            steps {
                echo 'Starting LogiLink Logistics Deployment...'
            }
        }
        stage('Build Service') {
            steps {
               sh 'docker build --no-cache -t logilink-app:v2.0 .'
            }
        }
        stage('Deployment') {
            steps {
                sh 'docker compose down --remove-orphans || true'
                // --no-build ensures it uses the image you made in the 'Build Service' stage
                sh 'docker compose up -d --no-build'
            }
        }
    }
}
