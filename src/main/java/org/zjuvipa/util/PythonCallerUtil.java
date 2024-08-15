package org.zjuvipa.util;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.zjuvipa.entity.DetectEventResultWithNewPhoto;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;

public class PythonCallerUtil {

    public static List<DetectEventResultWithNewPhoto> callPythonDetection(String photosWithStandardsJson) throws IOException, InterruptedException {
        // 构建命令
        String scriptPath = "src/main/algorithm/main/main.py";
        
        ProcessBuilder processBuilder = new ProcessBuilder("python", scriptPath);

        // 启动进程
        Process process = processBuilder.start();

        // 向Python脚本传递输入
        process.getOutputStream().write(photosWithStandardsJson.getBytes());
        process.getOutputStream().flush();
        process.getOutputStream().close();

        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        StringBuilder output = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            if (line.trim().startsWith("[{") ){
                output.append(line);
            }   
        }
        // while ((line = reader.readLine()) != null) {
        //     if (line.trim().startsWith("{") && line.trim().endsWith("}")) { // 过滤有效的 JSON 输出
        //         output.append(line);
        //     }
        // }
        
        int exitCode = process.waitFor();
        if (exitCode != 0) {
            throw new RuntimeException("Python script exited with error code: " + exitCode);
        }

        // 将 Python 输出的 JSON 字符串转换为 Java 对象
        ObjectMapper objectMapper = new ObjectMapper();
        return objectMapper.readValue(output.toString(), objectMapper.getTypeFactory().constructCollectionType(List.class, DetectEventResultWithNewPhoto.class));
    }

    public static void main(String[] args) {
        // 假设有JSON数据传递给Python脚本
        try {
            String photosWithStandardsJson = "[{\"detectOriginalPhoto\":{\"originalPhotoAddress\":\"/path/to/photo1\",\"originalPhotoName\":\"photo1.jpg\"},\"projectStandards\":[{\"startingMileage\":0.0,\"endingMileage\":10.0,\"standardSteelBarSpacing\":0.0,\"standardThickness\":5.0}]}]";
            List<DetectEventResultWithNewPhoto> results = callPythonDetection(photosWithStandardsJson);
            results.forEach(System.out::println);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
