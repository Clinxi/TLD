// import java.util.UUID;
//
// public class DetectionTask {
//     private String taskId;
//     private String status;  // 等待、执行中、完成
//     private List<APhotoWithStandards> inputData;
//     private List<DetectEventResultWithNewPhoto> result;
//
//     public DetectionTask(List<APhotoWithStandards> inputData) {
//         this.taskId = UUID.randomUUID().toString();
//         this.status = "等待";
//         this.inputData = inputData;
//     }
//
//     public String getTaskId() {
//         return taskId;
//     }
//
//     public String getStatus() {
//         return status;
//     }
//
//     public void setStatus(String status) {
//         this.status = status;
//     }
//
//     public List<APhotoWithStandards> getInputData() {
//         return inputData;
//     }
//
//     public List<DetectEventResultWithNewPhoto> getResult() {
//         return result;
//     }
//
//     public void setResult(List<DetectEventResultWithNewPhoto> result) {
//         this.result = result;
//     }
//
//     public void execute() {
//         this.status = "执行中";
//         try {
//             // 调用 Python 进行检测
//             this.result = PythonCallerUtil.callPythonDetection(inputData);
//             this.status = "完成";
//         } catch (Exception e) {
//             this.status = "错误";
//         }
//     }
// }
