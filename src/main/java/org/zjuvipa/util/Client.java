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

import com.fasterxml.jackson.databind.ObjectMapper;

public class Client {
    public static void main(String[] args) {
        RestTemplate restTemplate = new RestTemplate();

        DetectOriginalPhoto photo1 = new DetectOriginalPhoto(123,"src/main/algorithm/test/case1/3-DK324+390-535GD P_1.JPG", "3-DK324+390-535GD P_1.JPG",123,"abdc");

        List<ProjectStandard> standards1 = new ArrayList<>();
        standards1.add(new ProjectStandard(123213,324390f, 324450f, 0f, 0.3f,123213));
        standards1.add(new ProjectStandard(123213,324450f, 324504f, 0.333f, 0.4f,123213));
        standards1.add(new ProjectStandard(123213,324504f, 324535f, 0.25f, 0.5f,123213));

        APhotoWithStandards aPhotoWithStandards1 = new APhotoWithStandards(photo1, standards1);

        List<APhotoWithStandards> photoWithStandardsList = new ArrayList<>();
        photoWithStandardsList.add(aPhotoWithStandards1);

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
