package org.zjuvipa.util;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.client.RestTemplate;
import org.zjuvipa.entity.APhotoWithStandards;
import org.zjuvipa.entity.DetectOriginalPhoto;
import org.zjuvipa.entity.ProjectStandard;

import java.util.ArrayList;
import java.util.List;

// 原始代码
import com.fasterxml.jackson.databind.ObjectMapper;

public class Client {
    public static void main(String[] args) {
        RestTemplate restTemplate = new RestTemplate();

        DetectOriginalPhoto photo1 = new DetectOriginalPhoto(123,"src/main/algorithm/test/add_test/6-DK627+515-647YY P_1.JPG", "6-DK627+515-647YY P_1.JPG",123,"abdc");
        List<ProjectStandard> standards1 = new ArrayList<>();
        standards1.add(new ProjectStandard(123213,627515f, 627640f, 25f, 40f,123213));
        standards1.add(new ProjectStandard(123213,627640f, 627647f, 20f, 45f,123213));

        DetectOriginalPhoto photo2 = new DetectOriginalPhoto(123,"src/main/algorithm/test/add_test/8-DK326+135-237 YY P_12.JPG", "8-DK326+135-237 YY P_12.JPG",123,"abdc");
        List<ProjectStandard> standards2 = new ArrayList<>();
        standards2.add(new ProjectStandard(123213,627515f, 627640f, 0f, 30f,123213));

        APhotoWithStandards data1 = new APhotoWithStandards(photo1, standards1);
        APhotoWithStandards data2 = new APhotoWithStandards(photo2, standards2);
        List<APhotoWithStandards> photoWithStandardsList = new ArrayList<>();

        photoWithStandardsList.add(data1);
        photoWithStandardsList.add(data2);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<List<APhotoWithStandards>> requestEntity = new HttpEntity<>(photoWithStandardsList, headers);

        // 打印发送的 JSON 数据
        try {
            ObjectMapper mapper = new ObjectMapper();
            String jsonString = mapper.writeValueAsString(photoWithStandardsList);
            System.out.println("Request JSON: " + jsonString);
        } catch (Exception e) {
            e.printStackTrace();
        }

        String url = "http://localhost:8899/api/detect";
        try {
            String response = restTemplate.postForObject(url, requestEntity, String.class);
            System.out.println("Response: " + response);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

// 增加ID代码

// public class Client {
//     public static void main(String[] args) {
//         // Create RestTemplate instance
//         RestTemplate restTemplate = new RestTemplate();
//
//         // Test POST request to create a new detection task
//         String postUrl = "http://localhost:8899/api/detect";
//         DetectOriginalPhoto photo = new DetectOriginalPhoto(123,"src/main/algorithm/test/case1/3-DK324+390-535GD P_1.JPG", "3-DK324+390-535GD P_1.JPG",123,"abdc");
//
//         List<ProjectStandard> standards = new ArrayList<>();
//         standards.add(new ProjectStandard(123213,324390f, 324450f, 0f, 0.3f,123213));
//         standards.add(new ProjectStandard(123213,324450f, 324504f, 0.333f, 0.4f,123213));
//         standards.add(new ProjectStandard(123213,324504f, 324535f, 0.25f, 0.5f,123213));
//
//         APhotoWithStandards data = new APhotoWithStandards(photo, standards);
//
//         // Set headers
//         HttpHeaders headers = new HttpHeaders();
//         headers.setContentType(MediaType.APPLICATION_JSON);
//
//         try {
//             // Create POST request
//             HttpEntity<APhotoWithStandards> request = new HttpEntity<>(data, headers);
//             String taskId = restTemplate.postForObject(postUrl, request, String.class);
//             System.out.println("Task ID: " + taskId);
//
//             // Poll the task status until it's completed or failed
//             String getUrl = "http://localhost:8899/api/detect/status?taskId=" + taskId;
//             String status;
//             do {
//                 // Wait for a few seconds before checking the status again
//                 Thread.sleep(2000*30*4); // 2*30*4 seconds delay
//                 status = restTemplate.getForObject(getUrl, String.class);
//                 System.out.println("Task Status: " + status);
//             } while (status.equals("IN_PROGRESS"));
//
//             // Check final status
//             if (status.startsWith("Error:")) {
//                 System.out.println("Task failed with error: " + status);
//             } else if (status.equals("COMPLETED")) {
//                 System.out.println("Task completed successfully.");
//             }
//
//         } catch (Exception e) {
//             e.printStackTrace();
//         }
//     }
// }


// 测试并发运行代码
// public class Client {
//     public static void main(String[] args) {
//         // Number of concurrent tasks to simulate
//         int numberOfConcurrentTasks = 5;
//
//         for (int i = 0; i < numberOfConcurrentTasks; i++) {
//             // Create and start a new thread for each task
//             new Thread(new TaskRunner(i)).start();
//         }
//     }
//
//     // Runnable class to handle task creation and status checking
//     static class TaskRunner implements Runnable {
//         private final int taskId;
//
//         public TaskRunner(int taskId) {
//             this.taskId = taskId;
//         }
//
//         @Override
//         public void run() {
//             RestTemplate restTemplate = new RestTemplate();
//             String postUrl = "http://localhost:8899/api/detect";
//             String getUrl;
//             String status;
//
//             // Prepare the data for the POST request
// //             DetectOriginalPhoto photo = new DetectOriginalPhoto(1, "path/to/photo", "photo" + taskId, 1, "test");
// //             List<ProjectStandard> standards = new ArrayList<>();
// //             APhotoWithStandards data = new APhotoWithStandards(photo, standards);
//             DetectOriginalPhoto photo = new DetectOriginalPhoto(123,"src/main/algorithm/test/case1/3-DK324+390-535GD P_1.JPG", "3-DK324+390-535GD P_1.JPG",123,"abdc");
//
//             List<ProjectStandard> standards = new ArrayList<>();
//             standards.add(new ProjectStandard(123213,324390f, 324450f, 0f, 0.3f,123213));
//             standards.add(new ProjectStandard(123213,324450f, 324504f, 0.333f, 0.4f,123213));
//             standards.add(new ProjectStandard(123213,324504f, 324535f, 0.25f, 0.5f,123213));
//
//             APhotoWithStandards data = new APhotoWithStandards(photo, standards);
//
//
//
//             // Set headers
//             HttpHeaders headers = new HttpHeaders();
//             headers.setContentType(MediaType.APPLICATION_JSON);
//
//             try {
//                 // Create a new detection task
//                 HttpEntity<APhotoWithStandards> request = new HttpEntity<>(data, headers);
//                 String taskID = restTemplate.postForObject(postUrl, request, String.class);
//                 System.out.println("Thread " + taskId + ": Created task with ID: " + taskID);
//
//                 // Poll the task status until it's completed or failed
//                 getUrl = "http://localhost:8899/api/detect/status?taskId=" + taskID;
//                 do {
//                     // Wait for a few seconds before checking the status again
//                     Thread.sleep(2000*30*5); // 2 seconds delay
//                     status = restTemplate.getForObject(getUrl, String.class);
//                     System.out.println("Thread " + taskId + ": Task Status: " + status);
//                 } while (status.equals("IN_PROGRESS"));
//
//                 // Check final status
//                 if (status.startsWith("Error:")) {
//                     System.out.println("Thread " + taskId + ": Task failed with error: " + status);
//                 } else if (status.equals("COMPLETED")) {
//                     System.out.println("Thread " + taskId + ": Task completed successfully.");
//                 }
//
//             } catch (Exception e) {
//                 System.out.println("Thread " + taskId + ": Exception occurred - " + e.getMessage());
//             }
//         }
//     }
// }

