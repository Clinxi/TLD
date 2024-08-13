package org.zjuvipa.entity;

public class DetectOriginalPhoto {
    private String originalPhotoAddress;
    private String originalPhotoName;

    // 构造函数
    public DetectOriginalPhoto(String originalPhotoAddress, String originalPhotoName) {
        this.originalPhotoAddress = originalPhotoAddress;
        this.originalPhotoName = originalPhotoName;
    }

    // Getter 和 Setter 方法
    public String getOriginalPhotoAddress() {
        return originalPhotoAddress;
    }

    public void setOriginalPhotoAddress(String originalPhotoAddress) {
        this.originalPhotoAddress = originalPhotoAddress;
    }

    public String getOriginalPhotoName() {
        return originalPhotoName;
    }

    public void setOriginalPhotoName(String originalPhotoName) {
        this.originalPhotoName = originalPhotoName;
    }

    @Override
    public String toString() {
        return "DetectOriginalPhoto{" +
                "originalPhotoAddress='" + originalPhotoAddress + '\'' +
                ", originalPhotoName='" + originalPhotoName + '\'' +
                '}';
    }
}
