package org.zjuvipa.entity;

public class DetectOriginalPhoto {
    private Integer detectOriginalPhotoId;
    private String originalPhotoAddress;
    private String originalPhotoName;
    private Integer detectEventId;
    private String remark;
    // 构造函数
    public DetectOriginalPhoto(Integer detectOriginalPhotoId,String originalPhotoAddress, String originalPhotoName,Integer detectEventId,String remark) {
        this.detectOriginalPhotoId = detectOriginalPhotoId;
        this.originalPhotoAddress = originalPhotoAddress;
        this.originalPhotoName = originalPhotoName;
        this.detectEventId = detectEventId;
        this.remark = remark;
    }

    // Getter 和 Setter 方法
    public Integer getDetectOriginalPhotoId() {
        return detectOriginalPhotoId;
    }

    public void setDetectOriginalPhotoId(Integer detectOriginalPhotoId) {
        this.detectOriginalPhotoId = detectOriginalPhotoId;
    }

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

    public Integer getDetectEventId() {
        return detectEventId;
    }

    public void setDetectEventId(Integer detectEventId) {
        this.detectEventId = detectEventId;
    }

    public String getRemark() {
        return remark;
    }

    public void setRemark(String remark) {
        this.remark = remark == null ? null : remark.trim();
    }
    @Override
    public String toString() {
        return "DetectOriginalPhoto{" +"detectOriginalPhotoId="+detectOriginalPhotoId+ '\''+
        ", originalPhotoAddress='" + originalPhotoAddress + '\'' +
                ", originalPhotoName='" + originalPhotoName + '\'' +
                ", detectEventId='" + detectEventId + '\'' +
                ", remark='" + remark + '\'' +
                '}';
    }
}
