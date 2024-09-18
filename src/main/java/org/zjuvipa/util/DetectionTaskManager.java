package org.zjuvipa.util;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.zjuvipa.entity.DetectEventResultWithNewPhoto;
import org.zjuvipa.entity.APhotoWithStandards;

import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.UUID;

public class DetectionTaskManager {
    // 任务队列
    private static final BlockingQueue<String> taskQueue = new LinkedBlockingQueue<>();
    // 任务状态和结果存储
    private static final ConcurrentHashMap<String, String> taskStatus = new ConcurrentHashMap<>();
    private static final ConcurrentHashMap<String, List<DetectEventResultWithNewPhoto>> taskResults = new ConcurrentHashMap<>();
    // 错误信息存储
    private static final ConcurrentHashMap<String, String> taskErrors = new ConcurrentHashMap<>();
    // 任务输入数据存储
    private static final ConcurrentHashMap<String, String> taskDataMap = new ConcurrentHashMap<>();

    // 启动任务执行线程
    static {
        new Thread(() -> {
            while (true) {
                try {
                    String taskId = taskQueue.take(); // 取出队列中的任务
                    taskStatus.put(taskId, "IN_PROGRESS");

                    // 获取任务的 JSON 数据
                    String jsonData = taskDataMap.get(taskId);

                    // 调用 Python 脚本
                    List<DetectEventResultWithNewPhoto> result = PythonCallerUtil.callPythonDetection(jsonData);

                    taskResults.put(taskId, result);
                    taskStatus.put(taskId, "COMPLETED");
                } catch (Exception e) {
                    // 如果发生异常，存储错误信息并更新任务状态
                    String taskId = "UNKNOWN";
                    if (!taskQueue.isEmpty()) {
                        taskId = taskQueue.poll();
                    }
                    taskStatus.put(taskId, "FAILED");
                    taskErrors.put(taskId, e.getMessage());
                }
            }
        }).start();
    }

    // 创建新任务
    public static String createTask(List<APhotoWithStandards> dataList) {
        String taskId = UUID.randomUUID().toString();
        taskStatus.put(taskId, "WAITING");

        try {
            // 将 List<APhotoWithStandards> 序列化为 JSON
            ObjectMapper objectMapper = new ObjectMapper();
            String jsonData = objectMapper.writeValueAsString(dataList);

            // 存储 JSON 数据到任务数据映射
            taskDataMap.put(taskId, jsonData);
        } catch (Exception e) {
            taskStatus.put(taskId, "FAILED");
            taskErrors.put(taskId, "Error serializing input data: " + e.getMessage());
            System.out.println("Task " + taskId + " has FAILED with error: " + e.getMessage());
            return taskId;
        }

        // 将任务 ID 添加到任务队列
        taskQueue.add(taskId);
        return taskId;
    }

    // 获取任务状态
    public static String getTaskStatus(String taskId) {
        String status = taskStatus.getOrDefault(taskId, "NOT_FOUND");
        if ("FAILED".equals(status)) {
            return "Error: " + taskErrors.get(taskId);
        }
        return status;
    }

    // 获取任务结果
    public static List<DetectEventResultWithNewPhoto> getTaskResult(String taskId) {
        return taskResults.get(taskId);
    }
}
