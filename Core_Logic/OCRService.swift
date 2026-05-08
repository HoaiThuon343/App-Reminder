import Foundation
import UIKit
import Vision

class OCRService {
    
    // Hàm nhận vào ảnh UIImage và trả ra chuỗi Text
    static func extractText(from image: UIImage, completion: @escaping (String?) -> Void) {
        guard let cgImage = image.cgImage else {
            print("Lỗi: Không thể chuyển đổi định dạng ảnh.")
            completion(nil)
            return
        }
        
        let request = VNRecognizeTextRequest { (request, error) in
            if let error = error {
                print("Lỗi OCR: \(error.localizedDescription)")
                completion(nil)
                return
            }
            
            guard let observations = request.results as? [VNRecognizedTextObservation] else {
                completion(nil)
                return
            }
            
            // Lọc và nối các chữ lại với nhau
            let recognizedStrings = observations.compactMap { observation in
                return observation.topCandidates(1).first?.string
            }
            
            let fullText = recognizedStrings.joined(separator: "\n")
            completion(fullText)
        }
        
        // Cấu hình tối ưu cho Tiếng Việt và độ chính xác cao
        request.recognitionLevel = .accurate
        request.recognitionLanguages = ["vi-VN", "en-US"]
        request.usesLanguageCorrection = true
        
        let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])
        
        // Chạy request trong luồng ngầm để không đơ App
        DispatchQueue.global(qos: .userInitiated).async {
            do {
                try requestHandler.perform([request])
            } catch {
                print("Lỗi khi chạy OCR Scanner: \(error)")
                completion(nil)
            }
        }
    }
}