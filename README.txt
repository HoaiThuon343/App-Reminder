1. Mở Xcode, tạo một Project iOS App mới.

2. Kéo thả 2 file OCRService.swift và PromptBuilder.swift vào project.

3. Mở file Info.plist, thêm dòng Privacy - Camera Usage Description (Ghi chú: "App cần dùng Camera để quét Thời khóa biểu"). Nếu không làm bước này, App bật Camera lên sẽ bị văng (Crash) ngay lập tức!

4. Kéo file qwen2.5-1.5b-instruct.Q4_K_M.gguf  vào Project.

5. Cài thư viện llama.cpp qua Swift Package Manager để load file .gguf đó lên .