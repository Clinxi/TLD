package org.zjuvipa.client;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.client.RestTemplate;
import org.zjuvipa.entity.APhotoWithStandards;
import org.zjuvipa.entity.DetectOriginalPhoto;
import org.zjuvipa.entity.ProjectStandard;

import java.util.ArrayList;
import java.util.List;

public class Client {
    public static void main(String[] args) {
        // 创建一个 RestTemplate 实例
        RestTemplate restTemplate = new RestTemplate();

        // 创建多个 DetectOriginalPhoto 对象
        DetectOriginalPhoto photo1 = new DetectOriginalPhoto("path/to/photo1.jpg", "photo1.jpg");
        DetectOriginalPhoto photo2 = new DetectOriginalPhoto("path/to/photo2.jpg", "photo2.jpg");
        DetectOriginalPhoto photo3 = new DetectOriginalPhoto("path/to/photo3.jpg", "photo3.jpg");

        // 创建多个 ProjectStandard 对象并添加到列表中
        List<ProjectStandard> standards1 = new ArrayList<>();
        standards1.add(new ProjectStandard(0.0f, 1.0f, 0.2f, 2.5f));
        standards1.add(new ProjectStandard(1.0f, 2.0f, 0.15f, 2.8f));

        List<ProjectStandard> standards2 = new ArrayList<>();
        standards2.add(new ProjectStandard(2.0f, 3.0f, 0.1f, 3.0f));
        standards2.add(new ProjectStandard(3.0f, 4.0f, 0.25f, 3.2f));

        List<ProjectStandard> standards3 = new ArrayList<>();
        standards3.add(new ProjectStandard(4.0f, 5.0f, 0.18f, 2.9f));
        standards3.add(new ProjectStandard(5.0f, 6.0f, 0.22f, 3.1f));

        // 创建多个 APhotoWithStandards 对象
        APhotoWithStandards aPhotoWithStandards1 = new APhotoWithStandards(photo1, standards1);
        APhotoWithStandards aPhotoWithStandards2 = new APhotoWithStandards(photo2, standards2);
        APhotoWithStandards aPhotoWithStandards3 = new APhotoWithStandards(photo3, standards3);

        // 创建一个包含多个 APhotoWithStandards 对象的列表
        List<APhotoWithStandards> photoWithStandardsList = new ArrayList<>();
        photoWithStandardsList.add(aPhotoWithStandards1);
        photoWithStandardsList.add(aPhotoWithStandards2);
        photoWithStandardsList.add(aPhotoWithStandards3);

        // 设置请求头
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // 创建一个 HttpEntity 包装请求体
        HttpEntity<List<APhotoWithStandards>> requestEntity = new HttpEntity<>(photoWithStandardsList, headers);

        // 发送 POST 请求到指定的 URL，并接收响应
        String url = "http://localhost:8080/api/detect";
        try {
            String response = restTemplate.postForObject(url, requestEntity, String.class);
            System.out.println("Response: " + response);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
