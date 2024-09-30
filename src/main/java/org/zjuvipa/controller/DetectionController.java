package org.zjuvipa.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.zjuvipa.entity.APhotoWithStandards;
import org.zjuvipa.entity.DetectEventResultWithNewPhoto;
import org.zjuvipa.util.DetectionTaskManager;
import org.zjuvipa.util.PythonCallerUtil;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.lang.System;
import java.io.PrintStream;



import java.util.List;
import java.io.IOException;

// @RestController
// public class DetectionController {
//
//     // 创建检测任务
//     @PostMapping("/api/detect")
//     public ResponseEntity<String> createDetectionTask(@RequestBody List<APhotoWithStandards> data) {
//         System.out.println("Received a request to create a detection task.");
//         String taskId = DetectionTaskManager.createTask(data);
//         System.out.println("Task created with ID: " + taskId);
//         return ResponseEntity.ok(taskId);
//     }
//
//
//     // 查询任务状态和结果
//     @GetMapping("/api/detect/status")
//     public ResponseEntity<?> getTaskStatus(@RequestParam String taskId) {
//         System.out.println("Received a request to check the status of task ID: " + taskId);
//         String status = DetectionTaskManager.getTaskStatus(taskId);
//         if (status.startsWith("Error:")) {
//             System.out.println("Task " + taskId + " failed with error: " + status);
//             return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(status);
//         } else if ("COMPLETED".equals(status)) {
//             System.out.println("Task " + taskId + " completed successfully.");
//             List<DetectEventResultWithNewPhoto> results = DetectionTaskManager.getTaskResult(taskId);
//             return ResponseEntity.ok(results);
//         } else {
//             System.out.println("Task " + taskId + " is currently: " + status);
//             return ResponseEntity.ok(status);
//         }
//     }
// }


// // 过渡版本（response 为脚本检测结果）
// @RestController
// public class DetectionController {
//
//     // 创建检测任务
//     @PostMapping("/api/detect")
//     public ResponseEntity<String> createDetectionTask(@RequestBody List<APhotoWithStandards> data) {
//         System.out.println("Received a request to create a detection task.");
//         String taskId = DetectionTaskManager.createTask(data);  // 创建任务并返回任务ID
//         System.out.println("Task created with ID: " + taskId);
//         return ResponseEntity.ok(taskId);  // 返回任务ID
//     }
//
//     // 查询任务状态和结果
//     @GetMapping("/api/detect/status")
//     public ResponseEntity<?> getTaskStatus(@RequestParam String taskId) {
//         System.out.println("Received a request to check the status of task ID: " + taskId);
//         String status = DetectionTaskManager.getTaskStatus(taskId);  // 获取任务状态
//         if (status.startsWith("Error:")) {
//             System.out.println("Task " + taskId + " failed with error: " + status);
//             return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(status);  // 如果任务失败，返回错误信息
//         } else if ("COMPLETED".equals(status)) {
//             System.out.println("Task " + taskId + " completed successfully.");
//             List<DetectEventResultWithNewPhoto> results = DetectionTaskManager.getTaskResult(taskId);  // 获取任务结果
//             System.out.println("Response " + results);
//             return ResponseEntity.ok(results);  // 返回检测结果
//         } else {
//             System.out.println("Task " + taskId + " is currently: " + status);
//             return ResponseEntity.ok(status);  // 返回任务当前状态
//         }
//     }
// }


// // //原始代码 直接返回reponse
@RestController
public class DetectionController {

    @PostMapping("/api/detect")

    public ResponseEntity<String> detect(@RequestBody List<APhotoWithStandards> data) {
        long startTime = System.currentTimeMillis();  // 记录开始时间
        try {
            // 将接收到的数据转换为 JSON 字符串
            ObjectMapper objectMapper = new ObjectMapper();
            String photosWithStandardsJson = objectMapper.writeValueAsString(data);
            System.out.println("Converted JSON: " + photosWithStandardsJson);

            // 调用 Python 脚本
            List<DetectEventResultWithNewPhoto> hander_results = PythonCallerUtil.callPythonDetection(photosWithStandardsJson);
//             System.out.println("Detection results: " + results);
            // 将 List<DetectEventResultWithNewPhoto> 转换为 JSON 字符串
            String jsonResults = objectMapper.writeValueAsString(hander_results);
            System.setOut(new PrintStream(System.out, true, "UTF-8"));
            // 打印转换后的 JSON 字符串
            System.out.println("jsonResults 的类型: " + jsonResults.getClass().getName());
            System.out.println("Detection results in JSON: " + jsonResults);

            // 返回结果，确保结果非空
            if (hander_results != null && !hander_results.isEmpty()) {
                long endTime = System.currentTimeMillis();  // 记录结束时间
                long executionTime = endTime - startTime;  // 计算执行时间
                System.out.println("Execution time: " + executionTime + " ms");  // 输出执行时间
                return ResponseEntity.ok(jsonResults);
            } else {
                long endTime = System.currentTimeMillis();  // 记录结束时间
                long executionTime = endTime - startTime;  // 计算执行时间
                System.out.println("Execution time: " + executionTime + " ms");  // 输出执行时间
                return ResponseEntity.status(HttpStatus.NO_CONTENT).body(jsonResults);
            }

        } catch (Exception e) {
            long endTime = System.currentTimeMillis();  // 记录结束时间
            long executionTime = endTime - startTime;  // 计算执行时间
            System.out.println("Execution time: " + executionTime + " ms");  // 输出执行时间
            e.printStackTrace();
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
        }
    }
}
