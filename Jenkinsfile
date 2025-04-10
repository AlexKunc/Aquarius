pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/AlexKunc/Aquarius.git'
            }
        }
        
        stage('Start QEMU') {
            steps {
                script {
                    sh 'chmod +x qemu_start.sh'
                    sh 'Xvfb :99 -screen 0 1024x768x24 &'  
                    sh './qemu_start.sh &'
                    // Ждем доступности BMC
                    sh 'sleep 2.5m'
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'romulus/*.mtd', allowEmptyArchive: true
                }
            }
        }


        stage('Check OpenBMC Availability') {
            steps {
                script {
                    sh '''
                    echo "Проверяем доступность OpenBMC..."
                    if curl -k https://localhost:2443; then
                        echo "OpenBMC доступен!"
                    else
                        echo "Ошибка: OpenBMC не отвечает на localhost:2443"
                        exit 1
                    fi
                    '''
                }
            }
        }
        
        stage('Run Auto Tests') {
            steps {
                dir('lab4') {
                    sh '/opt/venv/bin/pytest -v --junitxml=auth-results.xml openbmc_auth_tests.py'
                }
            }
            post {
                always {
                    junit 'lab4/auth-results.xml'
                    archiveArtifacts artifacts: 'lab4/auth-results.xml'
                }
            }
        }

        stage('Run WebUI Tests') {
            steps {
                dir('lab5') {
                    sh '/opt/venv/bin/pytest -v --junitxml=webui-results.xml test_redfish.py'
                }
            }
            post {
                always {
                    junit 'lab5/webui-results.xml'
                    archiveArtifacts artifacts: 'lab5/webui-results.xml'
                }
            }
        }
        
        stage('Run Load Tests - Low Load') {
            steps {
                dir('lab6') {
                    script {
                        sh '''
                        /opt/venv/bin/locust -f locustfile.py \
                            --headless \
                            --users 100 \
                            --spawn-rate 10 \
                            --run-time 30s \
                            --host=https://localhost:2443 \
                            --html load_test_report_low.html \
                            --csv load_test_low \
                            --only-summary
                        '''
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'lab6/load_test_report_low.html, lab6/load_test_low_*.csv'
                }
            }
        }

        stage('Run Load Tests - Medium Load') {
            steps {
                dir('lab6') {
                    script {
                        sh '''
                        /opt/venv/bin/locust -f locustfile.py \
                            --headless \
                            --users 300 \
                            --spawn-rate 10 \
                            --run-time 20s \
                            --host=https://localhost:2443 \
                            --html load_test_report_medium.html \
                            --csv load_test_medium \
                            --only-summary
                        '''
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'lab6/load_test_report_medium.html, lab6/load_test_medium_*.csv'
                }
            }
        }

        stage('Run Load Tests - High Load') {
            steps {
                dir('lab6') {
                    script {
                        sh '''
                        /opt/venv/bin/locust -f locustfile.py \
                            --headless \
                            --users 800 \
                            --spawn-rate 30 \
                            --run-time 20s \
                            --host=https://localhost:2443 \
                            --html load_test_report_high.html \
                            --csv load_test_high \
                            --only-summary
                        '''
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'lab6/load_test_report_high.html, lab6/load_test_high_*.csv'
                }
            }
        }
    }
}
