package org.zjuvipa.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.zjuvipa.entity.DetectEventResultWithNewPhoto;
import org.zjuvipa.entity.APhotoWithStandards;
import org.zjuvipa.util.PythonCallerUtil;

import java.util.List;

@RestController
// @RequestMapping("/api")
public class DetectionController {

//     @PostMapping("/detect")
    public ResponseEntity<?> detectImages(@RequestBody List<APhotoWithStandards> photoWithStandardsList) {
        try {
            // 解析请求数据

            // 转换数据为 JSON 字符串
            String photosWithStandardsJson = new ObjectMapper().writeValueAsString(photoWithStandardsList);

            // 调用 Python 检测脚本
            List<DetectEventResultWithNewPhoto> results = PythonCallerUtil.callPythonDetection(photosWithStandardsJson);

            // 返回检测结果
            return ResponseEntity.ok(results);
        } catch (Exception e) {
            // 处理异常情况
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error occurred: " + e.getMessage());
        }
    }
}

// @RestController
// @RequestMapping("/api")
// public class DetectionController {
//
//     private final TaskQueueManager taskQueueManager = new TaskQueueManager();
//
//     @PostMapping("/detect")
//     public ResponseEntity<?> submitDetectionTask(@RequestBody List<APhotoWithStandards> data) {
//         String taskId = taskQueueManager.submitTask(data);
//         return ResponseEntity.ok(Map.of("taskId", taskId));
//     }
//
//     @GetMapping("/status/{taskId}")
//     public ResponseEntity<?> getTaskStatus(@PathVariable String taskId) {
//         DetectionTask task = taskQueueManager.getTask(taskId);
//         if (task == null) {
//             return ResponseEntity.status(HttpStatus.NOT_FOUND).body("任务不存在");
//         }
//         if ("完成".equals(task.getStatus())) {
//             return ResponseEntity.ok(Map.of("status", task.getStatus(), "result", task.getResult()));
//         }
//         return ResponseEntity.ok(Map.of("status", task.getStatus()));
//     }
// }

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
