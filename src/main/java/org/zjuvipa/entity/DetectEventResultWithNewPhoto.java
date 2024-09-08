package org.zjuvipa.entity;

import java.util.List;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class DetectEventResultWithNewPhoto {
    private String newPhotoAddress;
    private String newPhotoName;
    private List<DiseaseInformation> diseaseInformationList;


    // 默认构造函数（Jackson 需要）
    public DetectEventResultWithNewPhoto() {}
    
    // 构造函数
    public DetectEventResultWithNewPhoto(String newPhotoAddress, String newPhotoName, List<DiseaseInformation> diseaseInformationList) {
        this.newPhotoAddress = newPhotoAddress;
        this.newPhotoName = newPhotoName;
        this.diseaseInformationList = diseaseInformationList;
    }

    // Getter 和 Setter 方法
    public String getNewPhotoAddress() {
        return newPhotoAddress;
    }

    public void setNewPhotoAddress(String newPhotoAddress) {
        this.newPhotoAddress = newPhotoAddress;
    }

    public String getNewPhotoName() {
        return newPhotoName;
    }

    public void setNewPhotoName(String newPhotoName) {
        this.newPhotoName = newPhotoName;
    }

    public List<DiseaseInformation> getDiseaseInformationList() {
        return diseaseInformationList;
    }

    public void setDiseaseInformationList(List<DiseaseInformation> diseaseInformationList) {
        this.diseaseInformationList = diseaseInformationList;
    }

    @Override
    public String toString() {
        return "DetectEventResultWithNewPhoto{" +
                "newPhotoAddress='" + newPhotoAddress + '\'' +
                ", newPhotoName='" + newPhotoName + '\'' +
                ", diseaseInformationList=" + diseaseInformationList +
                '}';
    }
}
