// package org.zjuvipa.service;

// import org.springframework.context.annotation.Bean;
// import org.springframework.context.annotation.Configuration;
// import org.springframework.http.HttpEntity;
// import org.springframework.http.HttpHeaders;
// import org.springframework.http.MediaType;
// import org.springframework.http.ResponseEntity;
// import org.springframework.stereotype.Service;
// import org.springframework.util.LinkedMultiValueMap;
// import org.springframework.util.MultiValueMap;
// import org.springframework.web.client.RestTemplate;
// import org.zjuvipa.entity.DetectEventResultWithNewPhoto;
// import org.zjuvipa.entity.DetectOriginalPhoto;
// import org.zjuvipa.entity.ProjectStandard;

// import java.util.Arrays;
// import java.util.Collections;
// import java.util.List;

// @Service
// public class MyService {
//     private final RestTemplate restTemplate;

//     public MyService(RestTemplate restTemplate) {
//         this.restTemplate = restTemplate;
//     }

//     public List<DetectEventResultWithNewPhoto> sendDataAndFile(List<DetectOriginalPhoto> detectOriginalPhotoList, List<ProjectStandard> projectStandardList, String url) {
//         HttpHeaders headers = new HttpHeaders();
//         headers.setContentType(MediaType.APPLICATION_JSON);

//         MultiValueMap<String, Object> parts = new LinkedMultiValueMap<>();
//         parts.add("detectOriginalphotoList", detectOriginalPhotoList);
//         parts.add("projectStandardList", projectStandardList);
//         parts.add("url", url);

//         HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(parts, headers);

//         ResponseEntity<DetectEventResultWithNewPhoto[]> responseEntity = restTemplate.postForEntity(url, requestEntity, DetectEventResultWithNewPhoto[].class);

//         return Arrays.asList(responseEntity.getBody());
//     }
// }
