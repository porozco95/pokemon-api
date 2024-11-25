pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'porozco95/pokemon-api'
        DOCKER_TAG = 'latest'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Clonando el repositorio...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Construyendo la imagen Docker...'
                sh '/usr/local/bin/docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Subiendo la imagen a Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                        echo $DOCKER_PASSWORD | /usr/local/bin/docker login -u $DOCKER_USERNAME --password-stdin
                        /usr/local/bin/docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                    '''
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                echo 'Desplegando el contenedor...'
                sh '''
                    /usr/local/bin/docker stop pokemon-api || true
                    /usr/local/bin/docker rm pokemon-api || true
                    /usr/local/bin/docker run -d --name pokemon-api -p 8000:8000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline ejecutado correctamente.'
        }
        failure {
            echo 'Hubo un error en el pipeline.'
        }
    }
}