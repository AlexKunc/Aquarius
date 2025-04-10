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
                    
                    def bmcReady = false
                    def timeout = 300 
                    def interval = 5 
                    def elapsed = 0
                    
                    while (!bmcReady && elapsed < timeout) {
                        try {
                            def response = sh(script: 'curl -s -o /dev/null -w "%{http_code}" http://localhost:2443 || true', returnStdout: true).trim()
                            if (response == "200") {
                                bmcReady = true
                                echo "OpenBMC доступен!"
                            } else {
                                echo "OpenBMC еще не готов (HTTP код: ${response}). Ждем..."
                                sleep(interval)
                                elapsed += interval
                            }
                        } catch (Exception e) {
                            echo "Ошибка проверки: ${e}. Ждем..."
                            sleep(interval)
                            elapsed += interval
                        }
                    }
                    
                    if (!bmcReady) {
                        error("Таймаут ожидания OpenBMC (${timeout} секунд)")
                    }
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

        
    }
}
