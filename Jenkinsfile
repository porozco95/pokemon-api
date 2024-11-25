pipeline {
    agent any

    environment {
        IMAGE_NAME = "pokemon-api"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/porozco95/pokemon-api.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    sh 'docker run -d -p 8000:8000 $IMAGE_NAME'
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline completo."
        }
    }
}