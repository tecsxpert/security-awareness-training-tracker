package com.internship.tool.service;

import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class AiServiceClient {

    private final RestTemplate restTemplate;

    public AiServiceClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public String generateResponse(String prompt) {
        try {
            String url = System.getenv().getOrDefault(
                    "AI_SERVICE_URL",
                    "http://ai-service:5000"
            ) + "/ai/generate";

            System.out.println("👉 Calling AI at: " + url);

            Map<String, String> body = Map.of("prompt", prompt);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, String>> request =
                    new HttpEntity<>(body, headers);

            // 🔥 KEY CHANGE: use String instead of Map
            ResponseEntity<String> response = restTemplate.exchange(
                    url,
                    HttpMethod.POST,
                    request,
                    String.class
            );

            System.out.println("AI Raw Response: " + response.getBody());

            return response.getBody();  // return full JSON

        } catch (Exception e) {
            System.out.println("AI ERROR:");
            e.printStackTrace();
        }

        return null;
    }
}