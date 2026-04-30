package com.internship.tool.controller;

import com.internship.tool.service.AiServiceClient;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/ai")
@CrossOrigin(origins = "http://localhost:5173")
public class AiController {

    private final AiServiceClient aiServiceClient;

    public AiController(AiServiceClient aiServiceClient) {
        this.aiServiceClient = aiServiceClient;
    }

    @PostMapping("/generate")
    public ResponseEntity<?> generate(@RequestBody Map<String, String> request) {

        String prompt = request.get("prompt");

        if (prompt == null || prompt.trim().isEmpty()) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", "Prompt is required"));
        }

        if (prompt.length() > 500) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", "Prompt too long"));
        }

        String response = aiServiceClient.generateResponse(prompt);

        if (response == null) {
            return ResponseEntity.status(500)
                    .body(Map.of("error", "AI service unavailable"));
        }

        // return raw JSON string from Flask
        return ResponseEntity.ok(response);
    }
}