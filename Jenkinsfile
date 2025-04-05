pipeline {
    agent any

    environment {
        // Таймауты (в секундах)
        QEMU_START_TIMEOUT = '120'
        TEST_TIMEOUT = '300'
        
        // Пути к тестам
        AUTOTESTS_PATH = 'lab4/openbmc_auth_tests.py'
        WEBUI_TESTS_PATH = 'lab5/test_redfish.py'
    }

    stages {
        // Этап 1: Подготовка среды (без sudo)
        stage('Setup') {
            steps {
                script {
                    // Проверяем, что QEMU и Python уже установлены в образе
                    sh '''
                    pip install --user pytest selenium requests
                    '''
                }
            }
        }

        // Этап 2: Запуск QEMU
        stage('Start QEMU') {
            steps {
                script {
                    sh '''
                    chmod +x qemu_start.sh
                    ./qemu_start.sh > qemu.log 2>&1 &
                    '''
                    
                    sh """
                    timeout ${env.QEMU_START_TIMEOUT} bash -c 'while ! nc -z localhost 2443; do sleep 5; echo "Waiting for QEMU..."; done'
                    """
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'qemu.log', allowEmptyArchive: true
                }
            }
        }

        // Этап 3: Запуск автотестов
        stage('Run Autotests') {
            steps {
                script {
                    sh """
                    timeout ${env.TEST_TIMEOUT} pytest -v ${env.AUTOTESTS_PATH} --junitxml=autotest-results.xml
                    """
                }
            }
            post {
                always {
                    junit 'autotest-results.xml'
                }
            }
        }

        // Этап 4: Запуск WebUI тестов (без chromedriver)
        stage('Run WebUI Tests') {
            steps {
                script {
                    // Используем webdriver-manager для автоматического управления драйвером
                    sh """
                    python3 -m pip install webdriver-manager
                    timeout ${env.TEST_TIMEOUT} pytest -v ${env.WEBUI_TESTS_PATH} \
                        --html=webui-report.html \
                        --self-contained-html
                    """
                }
            }
            post {
                always {
                    publishHTML target: [
                        reportDir: '.',
                        reportFiles: 'webui-report.html',
                        reportName: 'WebUI Test Report'
                    ]
                }
            }
        }
    }

    post {
        always {
            sh 'pkill -f qemu-system-arm || true'
            sh 'rm -f qemu.log || true'
        }
    }
}
