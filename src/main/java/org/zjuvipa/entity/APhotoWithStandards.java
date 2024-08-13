package org.zjuvipa.entity;

import java.util.List;
import org.zjuvipa.entity.DetectOriginalPhoto;
import org.zjuvipa.entity.ProjectStandard;

public class APhotoWithStandards {
    private DetectOriginalPhoto detectOriginalPhoto;
    private List<ProjectStandard> projectStandards;

    public APhotoWithStandards() {} 
    // 构造函数
    public APhotoWithStandards(DetectOriginalPhoto detectOriginalPhoto, List<ProjectStandard> projectStandards) {
        this.detectOriginalPhoto = detectOriginalPhoto;
        this.projectStandards = projectStandards;
    }

    // Getter 和 Setter 方法
    public DetectOriginalPhoto getDetectOriginalPhoto() {
        return detectOriginalPhoto;
    }

    public void setDetectOriginalPhoto(DetectOriginalPhoto detectOriginalPhoto) {
        this.detectOriginalPhoto = detectOriginalPhoto;
    }

    public List<ProjectStandard> getProjectStandards() {
        return projectStandards;
    }

    public void setProjectStandards(List<ProjectStandard> projectStandards) {
        this.projectStandards = projectStandards;
    }

    @Override
    public String toString() {
        return "APhotoWithStandards{" +
                "detectOriginalPhoto=" + detectOriginalPhoto +
                ", projectStandards=" + projectStandards +
                '}';
    }
}
