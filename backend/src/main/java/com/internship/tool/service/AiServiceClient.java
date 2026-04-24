package com.internship.tool.service;

import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.ResourceAccessException;

import java.util.Map;

@Service
public class AiServiceClient {

    private final RestTemplate restTemplate;

    private static final String AI_URL = "http://localhost:5000/ai/generate";

    public AiServiceClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public String generateResponse(String prompt) {
        try {
            // Request body
            Map<String, String> body = Map.of("prompt", prompt);

            // Headers
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, String>> request =
                    new HttpEntity<>(body, headers);

            // API call
            ResponseEntity<Map> response = restTemplate.exchange(
                    AI_URL,
                    HttpMethod.POST,
                    request,
                    Map.class
            );

            if (response.getStatusCode().is2xxSuccessful()
                    && response.getBody() != null) {

                return (String) response.getBody().get("response");
            }

        } catch (ResourceAccessException e) {
            System.out.println("⏱ Timeout / Connection error: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("AI Service Error: " + e.getMessage());
        }

        return null; // as per task requirement
    }
}