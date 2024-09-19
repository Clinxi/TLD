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


import java.util.List;
import java.io.IOException;

@RestController
public class DetectionController {

    // 创建检测任务
    @PostMapping("/api/detect")
    public ResponseEntity<String> createDetectionTask(@RequestBody List<APhotoWithStandards> data) {
        System.out.println("Received a request to create a detection task.");
        String taskId = DetectionTaskManager.createTask(data);
        System.out.println("Task created with ID: " + taskId);
        return ResponseEntity.ok(taskId);
    }


    // 查询任务状态和结果
    @GetMapping("/api/detect/status")
    public ResponseEntity<?> getTaskStatus(@RequestParam String taskId) {
        System.out.println("Received a request to check the status of task ID: " + taskId);
        String status = DetectionTaskManager.getTaskStatus(taskId);
        if (status.startsWith("Error:")) {
            System.out.println("Task " + taskId + " failed with error: " + status);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(status);
        } else if ("COMPLETED".equals(status)) {
            System.out.println("Task " + taskId + " completed successfully.");
            List<DetectEventResultWithNewPhoto> results = DetectionTaskManager.getTaskResult(taskId);
            return ResponseEntity.ok(results);
        } else {
            System.out.println("Task " + taskId + " is currently: " + status);
            return ResponseEntity.ok(status);
        }
    }
}


//原始代码
// @RestController
// public class DetectionController {
//
//     @PostMapping("/api/detect")
//     public ResponseEntity<List<DetectEventResultWithNewPhoto>> detect(@RequestBody List<APhotoWithStandards> data) {
//         try {
//             // 将接收到的数据转换为 JSON 字符串
//             ObjectMapper objectMapper = new ObjectMapper();
//             String photosWithStandardsJson = objectMapper.writeValueAsString(data);
//             System.out.println("Converted JSON: " + photosWithStandardsJson);
//
//             // 调用 Python 脚本
//             List<DetectEventResultWithNewPhoto> results = PythonCallerUtil.callPythonDetection(photosWithStandardsJson);
//             System.out.println("Detection results: " + results);
//
//             // 返回结果，确保结果非空
//             if (results != null && !results.isEmpty()) {
//                 return ResponseEntity.ok(results);
//             } else {
//                 return ResponseEntity.status(HttpStatus.NO_CONTENT).body(results);
//             }
//         } catch (Exception e) {
//             e.printStackTrace();
//             return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(null);
//         }
//     }
// }
