import sys
import json
from barDetect import BarInfor, BarDetectResult

class DiseaseInformation:
    def __init__(self, diseaseStart, diseaseEnd, diseaseDepth, diseaseType):
        self.diseaseStart = diseaseStart
        self.diseaseEnd = diseaseEnd
        self.diseaseDepth = diseaseDepth
        self.diseaseType = diseaseType

    def __str__(self):
        return f"DiseaseInformation(diseaseStart={self.diseaseStart},diseaseEnd={self.diseaseEnd}, diseaseDepth={self.diseaseDepth}, diseaseType='{self.diseaseType}')"
    def to_dict(self):
        return {
            "diseaseStart": self.diseaseStart,
            "diseaseEnd": self.diseaseEnd,
            "diseaseDepth": self.diseaseDepth,
            "diseaseType": self.diseaseType
        }
        

class DetectOriginalPhoto:
    def __init__(self, originalPhotoAddress, originalPhotoName):
        self.originalPhotoAddress = originalPhotoAddress
        self.originalPhotoName = originalPhotoName

    def __repr__(self):
        return f"DetectOriginalPhoto(originalPhotoAddress='{self.originalPhotoAddress}', originalPhotoName='{self.originalPhotoName}')"

class ProjectStandard:
    def __init__(self, startingMileage, endingMileage, standardSteelBarSpacing, standardThickness):
        self.startingMileage = startingMileage
        self.endingMileage = endingMileage
        self.standardSteelBarSpacing = standardSteelBarSpacing
        self.standardThickness = standardThickness

    def __repr__(self):
        return (f"ProjectStandard(startingMileage={self.startingMileage}, "
                f"endingMileage={self.endingMileage}, "
                f"standardSteelBarSpacing={'素混凝土' if self.standardSteelBarSpacing == 0 else self.standardSteelBarSpacing}, "
                f"standardThickness={self.standardThickness})")


class DetectEventResultWithNewPhoto:
    def __init__(self, newPhotoAddress=None, newPhotoName=None, diseaseInformationList=None):
        self.newPhotoAddress = newPhotoAddress
        self.newPhotoName = newPhotoName
        self.diseaseInformationList = diseaseInformationList if diseaseInformationList is not None else []

    def getNewPhotoAddress(self):
        return self.newPhotoAddress

    def setNewPhotoAddress(self, newPhotoAddress):
        self.newPhotoAddress = newPhotoAddress

    def getNewPhotoName(self):
        return self.newPhotoName

    def setNewPhotoName(self, newPhotoName):
        self.newPhotoName = newPhotoName

    def getDiseaseInformationList(self):
        return self.diseaseInformationList
    
    def setDiseaseInformationList(self, diseaseInformationList):
        self.diseaseInformationList = diseaseInformationList

    def __str__(self):
        return (f"DetectEventResultWithNewPhoto(newPhotoAddress='{self.newPhotoAddress}', "
                f"newPhotoName='{self.newPhotoName}', "
                f"diseaseInformationList={self.diseaseInformationList})")
        
    def to_dict(self):
        return {
            "newPhotoAddress": self.newPhotoAddress,
            "newPhotoName": self.newPhotoName,
            "diseaseInformationList": [diseaseInfo.to_dict() for diseaseInfo in self.diseaseInformationList]
        }

class APhotoWithStandards:
    def __init__(self, detectOriginalPhoto, projectStandards):
        self.detectOriginalPhoto = DetectOriginalPhoto(**detectOriginalPhoto)
        self.projectStandards = [ProjectStandard(**ps) for ps in projectStandards]

    def __repr__(self):
        return f"APhotoWithStandards(detectOriginalPhoto={self.detectOriginalPhoto}, projectStandards={self.projectStandards})"


# this is there the algorithm exists
def perform_detection(photo_with_standards_list):
    results = []
    disease_info_1 = DiseaseInformation(1.0, 10.5, 2.0, "Leaf Spot")
    disease_info_2 = DiseaseInformation(1.0, 15.0, 3.5, "Powdery Mildew")
    disease_information_list = [disease_info_1, disease_info_2]
    for photo_with_standards in photo_with_standards_list:
        photo = photo_with_standards.detectOriginalPhoto
        # 这里可以根据需要使用 projectStandards 列表进行额外的计算或检测
        result = DetectEventResultWithNewPhoto(
            newPhotoAddress=photo.originalPhotoAddress,
            newPhotoName=photo.originalPhotoName,
            diseaseInformationList=disease_information_list
        )
        results.append(result)
    return results

def main(photos_with_standards_json):
    photo_with_standards_data = json.loads(photos_with_standards_json)
    photo_with_standards_list = [APhotoWithStandards(**pws) for pws in photo_with_standards_data]
    
    results = perform_detection(photo_with_standards_list)
    return [result.to_dict() for result in results]



if __name__ == "__main__":
    # 从标准输入读取 JSON 字符串
    
    input_json = sys.stdin.read()
    
    # # 调用 main 函数处理输入数据并输出结果
    output = main(input_json)
    print(json.dumps(output))


