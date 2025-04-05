pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/yourusername/your-repo.git'
            }
        }
        
        stage('Start QEMU') {
            steps {
                script {
                    sh 'chmod +x qemu_start.sh'
                    sh './qemu_start.sh &'
                    // Ожидание старта QEMU
                    sleep(time: 120, unit: 'SECONDS')
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'romulus/*.mtd', allowEmptyArchive: true
                }
            }
        }

        stage('Run Auth Tests') {
            steps {
                dir('lab4') {
                    sh 'pytest -v --junitxml=auth-results.xml openbmc_auth_tests.py'
                }
            }
            post {
                always {
                    junit 'lab4/auth-results.xml'
                }
            }
        }

        stage('Run WebUI Tests') {
            steps {
                dir('lab5') {
                    sh 'pytest -v --junitxml=webui-results.xml test_redfish.py'
                }
            }
            post {
                always {
                    junit 'lab5/webui-results.xml'
                }
            }
        }

        stage('Load Testing') {
            steps {
                script {
                    // Пример с использованием Apache Bench
                    sh 'apt-get update && apt-get install -y apache2-utils'
                    sh '''
                        ab -n 1000 -c 10 https://localhost:2443/redfish/v1/ > load-test-results.txt
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'load-test-results.txt', allowEmptyArchive: true
                }
            }
        }
    }
}
