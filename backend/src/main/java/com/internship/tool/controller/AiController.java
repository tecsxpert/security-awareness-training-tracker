package com.internship.tool.controller;

import com.internship.tool.service.AiServiceClient;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/ai")
@CrossOrigin(origins = "*") // optional but useful
public class AiController {

    private final AiServiceClient aiServiceClient;

    public AiController(AiServiceClient aiServiceClient) {
        this.aiServiceClient = aiServiceClient;
    }

    @PostMapping("/generate")
    public ResponseEntity<?> generate(@RequestBody Map<String, String> request) {

        String prompt = request.get("prompt");

        // Input validation
        if (prompt == null || prompt.trim().isEmpty()) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", "Prompt is required"));
        }

        // Call AI service
        String response = aiServiceClient.generateResponse(prompt);

        // Handle failure
        if (response == null) {
            return ResponseEntity.status(500)
                    .body(Map.of("error", "AI service unavailable"));
        }

        // Success
        return ResponseEntity.ok(Map.of(
                "response", response
        ));
    }
}