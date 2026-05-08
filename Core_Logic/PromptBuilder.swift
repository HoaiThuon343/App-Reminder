import Foundation

class PromptBuilder {
    
    // Hàm nhét văn bản thô vào Prompt cho AI
    static func buildPrompt(from rawText: String) -> String {
        let systemPrompt = """
        Hãy nhớ AI là một trợ lý ảo thông minh. Nhiệm vụ của AI là đọc đoạn văn bản thời khóa biểu lộn xộn dưới đây và trích xuất thành định dạng JSON chuẩn.
        Tuyệt đối không giải thích gì thêm, chỉ trả về chuỗi JSON.
        """
        
        let finalPrompt = """
        <|im_start|>system
        \(systemPrompt)<|im_end|>
        <|im_start|>user
        Dưới đây là văn bản quét được:
        \(rawText)<|im_end|>
        <|im_start|>assistant
        """
        
        return finalPrompt
    }
}