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
        // Этап 1: Подготовка среды
        stage('Setup') {
            steps {
                script {
                    // Установка зависимостей
                    sh '''
                    sudo apt-get update -qq
                    sudo apt-get install -y qemu-system-arm python3-pip
                    pip install pytest selenium requests
                    '''
                }
            }
        }

        // Этап 2: Запуск QEMU
        stage('Start QEMU') {
            steps {
                script {
                    // Даем права и запускаем QEMU в фоне
                    sh '''
                    chmod +x qemu_start.sh
                    ./qemu_start.sh > qemu.log 2>&1 &
                    '''
                    
                    // Ждем доступности порта 2443
                    sh """
                    timeout ${env.QEMU_START_TIMEOUT} bash -c 'while ! nc -z localhost 2443; do sleep 5; echo "Waiting for QEMU..."; done'
                    """
                }
            }
            post {
                always {
                    // Сохраняем логи QEMU
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

        // Этап 4: Запуск WebUI тестов
        stage('Run WebUI Tests') {
            steps {
                script {
                    // Установка ChromeDriver
                    sh '''
                    sudo apt-get install -y chromium-chromedriver
                    '''
                    
                    sh """
                    timeout ${env.TEST_TIMEOUT} pytest -v ${env.WEBUI_TESTS_PATH} --html=webui-report.html --self-contained-html
                    """
                }
            }
            post {
                always {
                    // Публикуем HTML отчет
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
            // Останавливаем QEMU после завершения тестов
            sh 'pkill -f qemu-system-arm || true'
            
            // Очистка (опционально)
            sh '''
            rm -f qemu.log
            '''
        }
    }
}