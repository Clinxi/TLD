package org.zjuvipa.util;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.zjuvipa.entity.DetectEventResultWithNewPhoto;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.util.List;

public class PythonCallerUtil {

    public static List<DetectEventResultWithNewPhoto> callPythonDetection(String photosWithStandardsJson) throws IOException, InterruptedException {
        // 获取当前项目的根目录
        String projectRoot = Paths.get("").toAbsolutePath().toString();
        // 构建 Python 脚本的绝对路径
        String scriptPath = Paths.get(projectRoot, "src", "main", "algorithm", "main", "main.py").toString();
        System.out.println("script path is"+scriptPath);
        // 使用 ProcessBuilder 来执行 Python 脚本
//         String pythonInterpreter = "D:/Anaconda/envs/TLD/python.exe";
        ProcessBuilder processBuilder = new ProcessBuilder("python", scriptPath);
        processBuilder.environment().put("PYTHONPATH", projectRoot);
        System.out.println("root path  is"+projectRoot);
        processBuilder.directory(new File(projectRoot));  // 设置工作目录为项目的根目录
        processBuilder.redirectErrorStream(true); // 将错误流合并到标准输出流

        // 启动进程
        Process process = processBuilder.start();
        // 在传输数据之前打印 JSON
//         System.out.println("Sending JSON to Python script: " + photosWithStandardsJson);
        // 向Python脚本传递输入
        process.getOutputStream().write(photosWithStandardsJson.getBytes());
        process.getOutputStream().flush();
        process.getOutputStream().close();

        // 读取 Python 脚本的输出
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        StringBuilder output = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            if (line.trim().startsWith("[{")) {
                output.append(line);
//             } else {
                // 跳过以 "YOLO"、"image" 或 "Speed" 开头的行
//                 if (line.trim().startsWith("YOLO") || line.trim().startsWith("image") || line.trim().startsWith("Speed")||line.trim().startsWith("Local")||line.trim().startsWith("Global")) {
//                     System.out.println("Python Script is running");
//                     continue;
//                 }
//                 if (line.trim().isEmpty()) {
//                             continue;
//                 }
//                 else{
//                     System.out.println("Python Script Output: " + line);
//                     }
//                 }
            }

            else{
            System.out.println("Python Script Output: " + line);
                                }
                            }
        int exitCode = process.waitFor();
        if (exitCode != 0) {
            throw new RuntimeException("Python script exited with error code: " + exitCode + "\nScript Output:\n" + output.toString());
        }
        // 将 Python 输出的 JSON 字符串转换为 Java 对象
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.readValue(output.toString(), objectMapper.getTypeFactory().constructCollectionType(List.class, DetectEventResultWithNewPhoto.class));
    }
}



// 原始版本
// package org.zjuvipa.util;
//
// import com.fasterxml.jackson.databind.ObjectMapper;
// import org.zjuvipa.entity.DetectEventResultWithNewPhoto;
//
// import java.io.BufferedReader;
// import java.io.IOException;
// import java.io.InputStreamReader;
// import java.util.List;
//
// public class PythonCallerUtil {
//
//     public static List<DetectEventResultWithNewPhoto> callPythonDetection(String photosWithStandardsJson) throws IOException, InterruptedException {
//         // 构建命令
//         String scriptPath = "src/main/algorithm/main/main.py";
//
//         ProcessBuilder processBuilder = new ProcessBuilder("python", scriptPath);
//
//         // 启动进程
//         Process process = processBuilder.start();
//
//         // 向Python脚本传递输入
//         process.getOutputStream().write(photosWithStandardsJson.getBytes());
//         process.getOutputStream().flush();
//         process.getOutputStream().close();
//
//         BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
//         StringBuilder output = new StringBuilder();
//         String line;
//         while ((line = reader.readLine()) != null) {
//             if (line.trim().startsWith("[{") ){
//                 output.append(line);
//             }
//         }
//         // while ((line = reader.readLine()) != null) {
//         //     if (line.trim().startsWith("{") && line.trim().endsWith("}")) { // 过滤有效的 JSON 输出
//         //         output.append(line);
//         //     }
//         // }
//
//         int exitCode = process.waitFor();
//         if (exitCode != 0) {
//             throw new RuntimeException("Python script exited with error code: " + exitCode);
//         }
//
//         // 将 Python 输出的 JSON 字符串转换为 Java 对象
//         ObjectMapper objectMapper = new ObjectMapper();
//         return objectMapper.readValue(output.toString(), objectMapper.getTypeFactory().constructCollectionType(List.class, DetectEventResultWithNewPhoto.class));
//         }
//
// //     public static void main(String[] args) {
// //         // 假设有JSON数据传递给Python脚本
// //         try {
// //        /*      String photosWithStandardsJson = "[{\"detectOriginalPhoto\"}:{\"detectOriginalPhotoId:"}]" */
// //             String photosWithStandardsJson = "[{\"detectOriginalPhoto\":{\"originalPhotoAddress\":\"/path/to/photo1\",\"originalPhotoName\":\"photo1.jpg\"},\"projectStandards\":[{\"startingMileage\":0.0,\"endingMileage\":10.0,\"standardSteelBarSpacing\":0.0,\"standardThickness\":5.0}]}]";
// //             List<DetectEventResultWithNewPhoto> results = callPythonDetection(photosWithStandardsJson);
// //             results.forEach(System.out::println);
// //         } catch (IOException | InterruptedException e) {
// //             e.printStackTrace();
// //         }
// //     }
// }