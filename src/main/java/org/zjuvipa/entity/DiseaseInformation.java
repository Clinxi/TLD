package org.zjuvipa.entity;

public class DiseaseInformation {
    private float diseaseStart;
    private float diseaseEnd;
    private float diseaseDepth;
    private String diseaseType;

    // 默认构造函数（Jackson 需要）
    public DiseaseInformation() {}
    
    // 构造函数
    public DiseaseInformation(float diseaseStart,float diseaseEnd, float diseaseDepth, String diseaseType) {
        this.diseaseStart = diseaseStart;
        this.diseaseEnd = diseaseEnd;
        this.diseaseDepth = diseaseDepth;
        this.diseaseType = diseaseType;
    }

    // Getter 和 Setter 方法
    public float getDiseaseStart() {
        return diseaseStart;
        print()
    }

    public void setDiseaseEnd(float diseaseEnd) {
        this.diseaseEnd = diseaseEnd;
    }

    // Getter 和 Setter 方法
    public float getDiseaseEnd() {
        return diseaseEnd;
    }

    public void setDiseaseStart(float diseaseStart) {
        this.diseaseStart = diseaseStart;
    }

    public float getDiseaseDepth() {
        return diseaseDepth;
    }

    public void setDiseaseDepth(float diseaseDepth) {
        this.diseaseDepth = diseaseDepth;
    }

    public String getDiseaseType() {
        return diseaseType;
    }

    public void setDiseaseType(String diseaseType) {
        this.diseaseType = diseaseType;
    }

    @Override
    public String toString() {
        return "DiseaseInformation{" +
                "diseaseStart=" + diseaseStart +
                ", diseaseEnd=" + diseaseEnd +
                ", diseaseDepth=" + diseaseDepth +
                ", diseaseType='" + diseaseType + '\'' +
                '}';
    }
}
