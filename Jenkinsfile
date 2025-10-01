pipeline {
    agent any

    stages {

        stage("Cloning from GitHub...."){
            steps{
                script{
                    echo 'Cloning from GitHub...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Luismbpr/0769_001_rcmndr_01.git']])
                }
            }
        }
    }
}