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

public class Client {
    public static void main(String[] args) {
        // 创建一个 RestTemplate 实例
        RestTemplate restTemplate = new RestTemplate();

        // 创建多个 DetectOriginalPhoto 对象
        DetectOriginalPhoto photo1 = new DetectOriginalPhoto("src/main/algorithm/test/case1/3-DK324+390-535GD P_1.JPG", "3-DK324+390-535GD P_1.JPG");

        // 创建多个 ProjectStandard 对象并添加到列表中
        List<ProjectStandard> standards1 = new ArrayList<>();
        standards1.add(new ProjectStandard(324390f, 324450f, 0f, 0.3f));
        standards1.add(new ProjectStandard(324450f, 324504f, 0.333f, 0.4f));
        standards1.add(new ProjectStandard(324504f, 324535f, 0.25f, 0.5f));
        

        // 创建多个 APhotoWithStandards 对象
        APhotoWithStandards aPhotoWithStandards1 = new APhotoWithStandards(photo1, standards1);

        // 创建一个包含多个 APhotoWithStandards 对象的列表
        List<APhotoWithStandards> photoWithStandardsList = new ArrayList<>();
        photoWithStandardsList.add(aPhotoWithStandards1);

        // 设置请求头
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // 创建一个 HttpEntity 包装请求体
        HttpEntity<List<APhotoWithStandards>> requestEntity = new HttpEntity<>(photoWithStandardsList, headers);

        // 发送 POST 请求到指定的 URL，并接收响应
        String url = "http://10.214.211.209:8080/api/detect";
        try {
            String response = restTemplate.postForObject(url, requestEntity, String.class);
            System.out.println("Response: " + response);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
