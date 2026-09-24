#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
#include <queue.h>

QueueHandle_t msgQueue;
const char msgA[] = "Task one is working";
const char msgB[] = "Task two is working";

void TaskConsumer(void *pv) {
  const char *msg;
  for (;;) {
    if (uxQueueMessagesWaiting(msgQueue) > 0) {
      if (xQueueReceive(msgQueue, &msg, 0) == pdTRUE) {
        Serial.println(msg);
      }
    }
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}
void TaskProducerA(void *pv) {
  const char *msg = msgA;
  for (;;) {
    xQueueSend(msgQueue, &msg, 0);
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}
void TaskProducerB(void *pv) {
  const char *msg = msgB;
  for (;;) {
    xQueueSend(msgQueue, &msg, 0);
    vTaskDelay(pdMS_TO_TICKS(1500));
  }
}
void setup() {
  Serial.begin(9600);
  msgQueue = xQueueCreate(5, sizeof(const char *));

  xTaskCreate(TaskConsumer,  "Consumer", 128, NULL, 1, NULL);
  xTaskCreate(TaskProducerA, "ProdA",    96,  NULL, 2, NULL);
  xTaskCreate(TaskProducerB, "ProdB",    96,  NULL, 2, NULL);
}
void loop() {}