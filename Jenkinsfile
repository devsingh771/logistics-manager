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
                sh 'docker build -t logilink-app:v2.0 .'
            }
        }
        stage('Deployment') {
            steps {
                sh 'docker compose down || true'
                sh 'docker compose up -d'
            }
        }
    }
}