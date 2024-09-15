// import java.util.concurrent.*;
//
// public class TaskQueueManager {
//     private final BlockingQueue<DetectionTask> taskQueue = new LinkedBlockingQueue<>();
//     private final ExecutorService executorService = Executors.newFixedThreadPool(4);
//     private final ConcurrentHashMap<String, DetectionTask> taskMap = new ConcurrentHashMap<>();
//
//     public TaskQueueManager() {
//         // 启动后台线程处理任务队列
//         for (int i = 0; i < 4; i++) {
//             executorService.submit(this::processTaskQueue);
//         }
//     }
//
//     public String submitTask(List<APhotoWithStandards> inputData) {
//         DetectionTask task = new DetectionTask(inputData);
//         taskMap.put(task.getTaskId(), task);
//         taskQueue.offer(task);
//         return task.getTaskId();
//     }
//
//     private void processTaskQueue() {
//         while (true) {
//             try {
//                 DetectionTask task = taskQueue.take();
//                 task.execute();
//             } catch (InterruptedException e) {
//                 Thread.currentThread().interrupt();
//             }
//         }
//     }
//
//     public DetectionTask getTask(String taskId) {
//         return taskMap.get(taskId);
//     }
// }
