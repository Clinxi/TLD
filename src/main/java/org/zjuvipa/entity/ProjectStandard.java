package org.zjuvipa.entity;

public class ProjectStandard {
    private Integer projectStandardId;
    private float startingMileage;
    private float endingMileage;
    private float standardSteelBarSpacing;
    private float standardThickness;
    private Integer projectId;
    // 构造函数
    public ProjectStandard(Integer projectStandardId,float startingMileage, float endingMileage, float standardSteelBarSpacing, float standardThickness,Integer projectId) {
        this.projectStandardId =projectStandardId;
        this.startingMileage = startingMileage;
        this.endingMileage = endingMileage;
        this.standardSteelBarSpacing = standardSteelBarSpacing;
        this.standardThickness = standardThickness;
        this.projectId = projectId;
    }

    // Getter 和 Setter 方法
    public Integer getProjectStandardId() {
        return projectStandardId;
    }

    public void setProjectStandardId(Integer projectStandardId) {
        this.projectStandardId = projectStandardId;
    }
    public float getStartingMileage() {
        return startingMileage;
    }

    public void setStartingMileage(float startingMileage) {
        this.startingMileage = startingMileage;
    }

    public float getEndingMileage() {
        return endingMileage;
    }

    public void setEndingMileage(float endingMileage) {
        this.endingMileage = endingMileage;
    }

    public float getStandardSteelBarSpacing() {
        return standardSteelBarSpacing;
    }

    public void setStandardSteelBarSpacing(float standardSteelBarSpacing) {
        this.standardSteelBarSpacing = standardSteelBarSpacing;
    }

    public float getStandardThickness() {
        return standardThickness;
    }

    public void setStandardThickness(float standardThickness) {
        this.standardThickness = standardThickness;
    }
    public Integer getProjectId() {
        return projectId;
    }
    public void setProjectId(Integer projectId) {
            this.projectId = projectId;
        }

    @Override
    public String toString() {
        return "ProjectStandard{" +
                "projectStandardId="+projectStandardId+
                ",startingMileage=" + startingMileage +
                ", endingMileage=" + endingMileage +
                ", standardSteelBarSpacing=" + standardSteelBarSpacing +
                ", standardThickness=" + standardThickness +
                ", projectId=" + projectId +
                '}';
    }
}
