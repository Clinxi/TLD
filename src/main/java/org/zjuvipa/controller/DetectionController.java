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
@RequestMapping("/api")
public class DetectionController {

    @PostMapping("/detect")
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
