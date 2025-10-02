pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'mlops-new-447207'
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
    }
    
    /* Stages to create:
    - GitHub Repo Cloning
    - Venv creation
    - DVC Pull
    - Push image into Cloud: GCP
    - Deploy to Kubernetes
    */

    stages{

        stage("Cloning from Github...."){
            steps{
                script{
                    echo 'Cloning from Github...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/data-guru0/MLOPS-COURSE-PROJECT-2.git']])
                }
            }
        }
        

        /* Create Variable: VENV_DIR */
        stage("Making a virtual environment...."){
            steps{
                script{
                    echo 'Making a virtual environment...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install  dvc
                    '''
                }
            }
        }

        /* Pull the project from DVC Bucket to project directory */
        /* Credential id name for this 'gcp-key' in
                Dashboard > Manage Jenkins > Credentials
                Want to save this with variable name 'GOOGLE_APPLICATION_CREDENTIALS' */
        stage('DVC Pull'){
            steps{
                withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
                    script{
                        echo 'DVC Pul....'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }
    }
}