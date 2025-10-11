from src.monitor import monitor_health, monitor_predict
import time
import os

# Вычисляет 95-й перцентиль времени ответа
def calc_p95(latencies):
    if not latencies:
        return None
    lat_sorted = sorted(latencies)
    k = int(len(lat_sorted) * 0.95)
    return lat_sorted[min(k, len(lat_sorted)-1)]

# Вычисляет процент неудачных запросов
def calc_error_rate(status_codes):
    errors = sum(1 for code in status_codes if code is None or code >= 400)
    return errors / len(status_codes) if status_codes else None

# Вычисляет количество последовательных ошибок
def calc_consecutive_failures(status_codes):
    count = 0
    for code in reversed(status_codes):
        if code is None or code >= 400:
            count += 1
        else:
            break
    return count

def main():
    '''
    Запуск мониторинга.

    '''
    api_url = 'http://localhost:8000'
    img_path = 'img.jpg'

    health_result = monitor_health(api_url)
    print(health_result)

    predict_result = monitor_predict(api_url, img_path)
    print(predict_result)

    # Проверка метрик
    iterations = 20

    # Метрики для health
    latencies_health = []
    status_codes_health = []

    # Метрики для predict
    latencies_predict = []
    status_codes_predict = []

    for i in range(iterations):
        # Мониторинг /health
        h_res = monitor_health(api_url)
        print("[health]", h_res)
        latencies_health.append(h_res["latency"])
        status_codes_health.append(h_res["status_code"])

        # Мониторинг /predict
        p_res = monitor_predict(api_url, img_path)
        print("[predict]", p_res)
        latencies_predict.append(p_res["latency"])
        status_codes_predict.append(p_res["status_code"])

        time.sleep(1)  # задержка между итерациями

    # Рассчитываем метрики
    print("\n----- Метрики /health -----")
    print("P95 latency:", calc_p95(latencies_health))
    print("Error rate:", calc_error_rate(status_codes_health))
    print("Consecutive failures:", calc_consecutive_failures(status_codes_health))

    print("\n----- Метрики /predict -----")
    print("P95 latency:", calc_p95(latencies_predict))
    print("Error rate:", calc_error_rate(status_codes_predict))
    print("Consecutive failures:", calc_consecutive_failures(status_codes_predict))

if __name__ == "__main__":
    main()