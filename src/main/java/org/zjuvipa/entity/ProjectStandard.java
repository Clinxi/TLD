package org.zjuvipa.entity;

public class ProjectStandard {
    private float startingMileage;
    private float endingMileage;
    private float standardSteelBarSpacing;
    private float standardThickness;

    // 构造函数
    public ProjectStandard(float startingMileage, float endingMileage, float standardSteelBarSpacing, float standardThickness) {
        this.startingMileage = startingMileage;
        this.endingMileage = endingMileage;
        this.standardSteelBarSpacing = standardSteelBarSpacing;
        this.standardThickness = standardThickness;
    }

    // Getter 和 Setter 方法
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

    @Override
    public String toString() {
        return "ProjectStandard{" +
                "startingMileage=" + startingMileage +
                ", endingMileage=" + endingMileage +
                ", standardSteelBarSpacing=" + standardSteelBarSpacing +
                ", standardThickness=" + standardThickness +
                '}';
    }
}
